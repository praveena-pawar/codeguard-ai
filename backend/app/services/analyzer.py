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

    def visit_FunctionDef(self, node: ast.FunctionDef):
        previous_guards = self.guarded_denominators.copy()

        self.guarded_denominators = set()

        for statement in node.body:
            if isinstance(statement, ast.If):
                self._collect_zero_guards(statement)

        for statement in node.body:
            self.visit(statement)

        self.guarded_denominators = previous_guards

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        previous_guards = self.guarded_denominators.copy()

        self.guarded_denominators = set()

        for statement in node.body:
            if isinstance(statement, ast.If):
                self._collect_zero_guards(statement)

        for statement in node.body:
            self.visit(statement)

        self.guarded_denominators = previous_guards

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