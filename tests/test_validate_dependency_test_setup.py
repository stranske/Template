"""The scaffold's dependency validator must work without product-specific files."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_dependency_test_setup.py"


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / SCRIPT.name)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def scaffold_copy(tmp_path: Path) -> Path:
    (tmp_path / "scripts").mkdir()
    for path in (SCRIPT, ROOT / "pyproject.toml", ROOT / "requirements.lock"):
        shutil.copy2(path, tmp_path / ("scripts" if path == SCRIPT else "") / path.name)
    return tmp_path


def test_shipped_validator_passes_on_scaffold() -> None:
    result = run_validator(ROOT)
    assert result.returncode == 0, result.stderr


def test_numeric_assertion_is_not_a_dependency_version(tmp_path: Path) -> None:
    root = scaffold_copy(tmp_path)
    (root / "tests").mkdir()
    (root / "tests" / "test_numbers.py").write_text("def test_numbers():\n    assert 2.0 == 2.0\n")
    result = run_validator(root)
    assert result.returncode == 0, result.stderr


def test_missing_declared_dependency_fails(tmp_path: Path) -> None:
    root = scaffold_copy(tmp_path)
    lock = root / "requirements.lock"
    lock.write_text(
        "".join(
            line
            for line in lock.read_text().splitlines(keepends=True)
            if not line.startswith("ruff==")
        )
    )
    result = run_validator(root)
    assert result.returncode == 1
    assert "dev: ruff is missing" in result.stderr


def test_direct_reference_with_extra_is_in_lock(tmp_path: Path) -> None:
    root = scaffold_copy(tmp_path)
    pyproject = root / "pyproject.toml"
    pyproject.write_text(
        pyproject.read_text().replace(
            "dev = [", 'dev = [\n    "demo[feature] @ https://example.invalid/demo.whl",', 1
        )
    )
    lock = root / "requirements.lock"
    lock.write_text(lock.read_text() + "\ndemo[feature] @ https://example.invalid/demo.whl\n")
    result = run_validator(root)
    assert result.returncode == 0, result.stderr


def test_no_optional_groups_need_no_lock(tmp_path: Path) -> None:
    root = scaffold_copy(tmp_path)
    (root / "pyproject.toml").write_text('[project]\nname = "demo"\n')
    (root / "requirements.lock").unlink()
    result = run_validator(root)
    assert result.returncode == 0, result.stderr


def test_optional_groups_need_lock(tmp_path: Path) -> None:
    root = scaffold_copy(tmp_path)
    (root / "requirements.lock").unlink()
    result = run_validator(root)
    assert result.returncode == 1
    assert "requirements.lock is missing" in result.stderr


def test_no_product_specific_probe_in_shipped_validator() -> None:
    source = SCRIPT.read_text()
    assert "src/trend_analysis/io/validators.py" not in source
    assert "dependabot-auto-lock.yml" not in source
