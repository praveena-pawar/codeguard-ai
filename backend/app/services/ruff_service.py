import json
import subprocess
import tempfile
from pathlib import Path


def run_ruff(code: str) -> list[dict]:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "code.py"
        file_path.write_text(code, encoding="utf-8")

        result = subprocess.run(
            [
                "ruff",
                "check",
                str(file_path),
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if not result.stdout.strip():
            return []

        return json.loads(result.stdout)