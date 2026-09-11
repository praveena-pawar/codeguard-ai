import ast
from dataclasses import dataclass


@dataclass
class CodeIssue:
    rule: str
    message: str
    line: int
    severity: str


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues: list[CodeIssue] = []

    def visit_BinOp(self, node: ast.BinOp):
        if isinstance(node.op, ast.Div):
            self.issues.append(
                CodeIssue(
                    rule="DIVISION",
                    message="Division operation detected. Make sure the denominator cannot be zero.",
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

    return analyzer.issues