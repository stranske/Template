# Dependency testing

The scaffold declares optional dependency groups in `pyproject.toml` and ships
`requirements.lock`. When changing dependencies, regenerate the lockfile using
the optional groups declared by this repository. The current scaffold has a
`dev` group:

```bash
uv pip compile pyproject.toml --extra=dev --universal --output-file=requirements.lock
```

Run the repository-neutral validator before merging a dependency update:

```bash
python scripts/validate_dependency_test_setup.py
```

It checks that each package named by `[project.optional-dependencies]` appears
in `requirements.lock`. It does not inspect application-specific paths or treat
numeric assertions in tests as dependency-version checks. A repo with no optional
dependency groups has no optional lockfile entries to validate.

The validator checks presence, not version resolution. The lockfile generation
command and the normal test suite remain responsible for a consistent install.
