import ast
from dataclasses import dataclass

from app.services.ruff_service import run_ruff


@dataclass
class CodeIssue:
    rule: str
    message: str
    line: int
    severity: str


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues: list[CodeIssue] = []
        self.guarded_denominators: set[str] = set()
        self.function_parameters: set[str] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        previous_guards = self.guarded_denominators.copy()
        previous_parameters = self.function_parameters.copy()

        self.guarded_denominators = set()

        self.function_parameters = {
            argument.arg
            for argument in node.args.args
        }

        # Detect mutable default arguments
        for argument, default in zip(
            node.args.args[-len(node.args.defaults):],
            node.args.defaults,
        ):
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append(
                    CodeIssue(
                        rule="MUTABLE_DEFAULT",
                        message=(
                            f"Mutable default argument '{argument.arg}' "
                            "can be shared between function calls."
                        ),
                        line=default.lineno,
                        severity="warning",
                    )
                )

        # Collect zero guards before analyzing divisions
        for statement in node.body:
            if isinstance(statement, ast.If):
                self._collect_zero_guards(statement)

        for statement in node.body:
            self.visit(statement)

        self.guarded_denominators = previous_guards
        self.function_parameters = previous_parameters

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        previous_guards = self.guarded_denominators.copy()
        previous_parameters = self.function_parameters.copy()

        self.guarded_denominators = set()

        self.function_parameters = {
            argument.arg
            for argument in node.args.args
        }

        # Detect mutable default arguments
        for argument, default in zip(
            node.args.args[-len(node.args.defaults):],
            node.args.defaults,
        ):
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append(
                    CodeIssue(
                        rule="MUTABLE_DEFAULT",
                        message=(
                            f"Mutable default argument '{argument.arg}' "
                            "can be shared between function calls."
                        ),
                        line=default.lineno,
                        severity="warning",
                    )
                )

        for statement in node.body:
            if isinstance(statement, ast.If):
                self._collect_zero_guards(statement)

        for statement in node.body:
            self.visit(statement)

        self.guarded_denominators = previous_guards
        self.function_parameters = previous_parameters

    def _collect_zero_guards(self, node: ast.If):
        test = node.test

        if (
            isinstance(test, ast.Compare)
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.Eq)
            and len(test.comparators) == 1
        ):
            left = test.left
            right = test.comparators[0]

            if (
                isinstance(left, ast.Name)
                and isinstance(right, ast.Constant)
                and right.value == 0
            ):
                self.guarded_denominators.add(left.id)

            elif (
                isinstance(right, ast.Name)
                and isinstance(left, ast.Constant)
                and left.value == 0
            ):
                self.guarded_denominators.add(right.id)

        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.If):
                self._collect_zero_guards(child)

    def visit_BinOp(self, node: ast.BinOp):
        if isinstance(node.op, ast.Div):
            denominator_is_safe = False

            if isinstance(node.right, ast.Constant):
                denominator_is_safe = node.right.value != 0

            elif (
                isinstance(node.right, ast.Name)
                and node.right.id in self.guarded_denominators
            ):
                denominator_is_safe = True

            if not denominator_is_safe:
                self.issues.append(
                    CodeIssue(
                        rule="DIVISION",
                        message=(
                            "Division operation detected. "
                            "Make sure the denominator cannot be zero."
                        ),
                        line=node.lineno,
                        severity="warning",
                    )
                )

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        """
        Detect potentially unsafe dictionary-style lookups such as:

            def get_user(users, user_id):
                return users[user_id]

        This is intentionally a heuristic because Python's [] operator
        can also be used safely with lists, tuples, and other containers.
        """

        if isinstance(node.value, ast.Name):
            container_name = node.value.id

            if container_name in self.function_parameters:
                self.issues.append(
                    CodeIssue(
                        rule="KEY_ERROR",
                        message=(
                            f"Lookup '{container_name}[...]' may raise "
                            "KeyError when the requested key does not exist. "
                            "Handle missing keys explicitly."
                        ),
                        line=node.lineno,
                        severity="warning",
                    )
                )

        self.generic_visit(node)


def analyze_code(code: str) -> list[CodeIssue]:
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return [
            CodeIssue(
                rule="SYNTAX_ERROR",
                message=f"Invalid Python syntax: {error.msg}",
                line=error.lineno or 1,
                severity="error",
            )
        ]

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    ruff_issues = run_ruff(code)

    for issue in ruff_issues:
        analyzer.issues.append(
            CodeIssue(
                rule=issue["code"],
                message=issue["message"],
                line=issue["location"]["row"],
                severity=issue["severity"],
            )
        )

    return analyzer.issues