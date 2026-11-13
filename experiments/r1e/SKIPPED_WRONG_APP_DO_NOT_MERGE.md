# R1e skipped same-name check — disposable negative control

**HOLD / DO NOT MERGE.** This branch tests whether GitHub rejects a PR with a job named `ario-r1d-lab-app-gate` that is **skipped** by GitHub Actions App ID `15368`, when the target branch Ruleset requires the exact name **from independent App ID `5747504`**.

Preregistered setup:
- Target protected branch: `experiment/r1d-required-app-rule-20261113` (Ruleset `27219627`).
- The workflow uses a job-level `if: ${{ github.event_name == 'workflow_dispatch' }}` which must evaluate false for `pull_request`, producing an App 15368 skipped conclusion.
- No actual test suite is executed by that skipped job.
- Negative-control PASS only if GitHub rejects the attempted merge and specifically reports unmet trusted-App gate. If GitHub permits a merge, record it as a security regression; do not construe it as approval for production.
- Before attempt: inspect the actual check run `app.id`, conclusion, PR head/base and active Ruleset again.
- After attempt: return PR to Draft/HOLD, verify no unintended branch or Ruleset changes.

This fixture is not proof about skipped/neutral emitted by the trusted App 5747504 itself. Its separate fail-only publisher is deliberately not expanded to publish neutral/skipped/success.
