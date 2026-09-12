import subprocess
import tempfile
from pathlib import Path


def run_tests(source_code: str, test_code: str) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        source_file = temp_path / "solution.py"
        test_file = temp_path / "test_solution.py"

        source_file.write_text(source_code, encoding="utf-8")
        test_file.write_text(test_code, encoding="utf-8")

        result = subprocess.run(
            [
                "pytest",
                str(test_file),
                "-q",
            ],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        return {
            "passed": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }