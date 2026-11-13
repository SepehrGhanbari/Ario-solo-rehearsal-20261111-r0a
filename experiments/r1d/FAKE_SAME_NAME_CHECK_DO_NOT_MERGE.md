# R1d fake-check negative control — HOLD / DISPOSABLE

This branch deliberately creates a GitHub Actions **success** named `ario-r1d-lab-app-gate` using `exit 0`. **No tests execute.** It is NOT the independent App ID `5747504`; the fake green belongs to GitHub Actions App ID `15368`.

Target is only `experiment/r1d-required-app-rule-20261113`. A separate branch-scoped Ruleset should require the same check name **from integration App 5747504**, not arbitrary apps. Success criterion for this negative control is GitHub REJECTING a merge even if this forged same-name check is green.

This is an adversarial research fixture, not production code and not authorization to merge; preserve and do not modify R0 main ruleset `27069097`.
