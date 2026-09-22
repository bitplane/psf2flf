import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize("status", [0, 1, 2, 5])
def test_coverage_preserves_pytest_exit_status(tmp_path, status):
    activate = tmp_path / ".venv/bin/activate"
    activate.parent.mkdir(parents=True)
    activate.write_text(f'pytest() {{ echo "test output"; return {status}; }}\n')
    script = Path("scripts/coverage.sh").resolve()
    result = subprocess.run(["bash", str(script), "psf2flf"], cwd=tmp_path, capture_output=True)
    assert result.returncode == status
    assert (tmp_path / "htmlcov/coverage_report.txt").read_text() == "test output\n"
