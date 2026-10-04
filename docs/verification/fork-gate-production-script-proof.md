# Template fork-Gate production-script proof

Workflows [#3399](https://github.com/stranske/Workflows/issues/3399) lacked a committed Template harness. This follow-up executes the deployed `Report Gate commit status` step under Node; it changes no workflow, permission, token, or sync policy. The retry wrapper is a pass-through stub, so this proves the step catch/summary behavior, not retry-library integration. The production script is extracted from YAML at test runtime.

Baseline: Template main `92174dbaa81ca3e104b1a3abcf06fada31e9a386`.
Test command: `python3 -m pytest -q --no-cov tests/test_gate_commit_status_fork_tolerance.py`.

Controls cover fork read-only 403 and preserved verdict, same-repository 403 refusal, unrelated 500 refusal, seven rate-limit variants, positive-quota fork refusal, and successful writes. Missing Node fails in CI instead of yielding a vacuous skip.

## Deliberate break and restoration

Only in the local worktree, replace the status step's `error?.status === 403 && isForkPullRequest && !hitRateLimit;` expression with `false;`. This disables only the deployed fork-status fallback, reproducing the old rethrow behavior. No base-workflow revert is claimed: the existing deployed fallback predates this test-only PR.

RED: `3 failed, 4 passed`; the failing cases are `test_fork_read_only_403_does_not_fail_the_gate`, `test_fork_read_only_403_reports_the_real_verdict`, and `test_positive_quota_permission_403_uses_fork_fallback`. Each reports thrown status403. Same-repo/non-403/rate-limit controls remain passing.

Restore the workflow from the saved original bytes. GREEN: `7 passed`. The workflow bytes are identical before and after, and the committed diff contains the test, its declared and locked PyYAML development dependency, and this evidence document. Full command output remains in closer `work/20261004T1444Z/template-red.log` and `template-restored-green.log`.

This closes the missing committed-test prerequisite after normal PR review/merge/verification. Parent#3399 stays open: the separately documented Orchestrator status-write exception still requires a source acceptance decision; this test does not waive that discrepancy.

Workflow SHA256: `0740c45d71678af24d8f2a302cea68e3ce62628a9a4bfccfd703a1196d867ee4`.
Test SHA256: `7877023e8d61e79f66e6aee8a4ee5053fff874b1b1ea9285346a7b65bfe4f213`.

CI follow-through: run37211097784 failed before pytest because the new YAML import lacked a declared development dependency. Declare `PyYAML>=6.0.3` and lock it at6.0.3; the exact `scripts/sync_test_dependencies.py --verify` command and full local pytest suite pass after repair. Workflow files remain unchanged.
