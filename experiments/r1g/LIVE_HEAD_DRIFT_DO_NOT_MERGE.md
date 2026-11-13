# R1g append-only HEAD drift negative control — HOLD / NEVER MERGE

**Fixture scope:** disposable PR #13 only; protected base experiment/r1d-required-app-rule-20261113; active no-bypass required Check name `ario-r1d-lab-app-gate` from GitHub App `5747504`.

- Original PR head A: `0eec58824f969ba056e363d1c1f84dfe563b0964`.
- App 5747504 issued `completed/failure` Check Run `132051950320` on A. The check is real but deliberately **NOT successful**.
- This evidence-only commit makes new HEAD B, preserving A and all historical evidence. After commit, independently query GitHub check-runs for A and B. The old check should remain on A only.
- A READY-for-review, exact-B merge attempt against the protected branch should fail with unmet required App gate (HTTP 405). Immediately restore Draft/HOLD and confirm no merge, protected base SHA or ruleset mutation.

**Research limit:** This cannot prove old **successful** trusted-App Check invalidation, because there has never been a trusted-App success. We will not fabricate such a result: a real independent positive-control evaluator remains to be engineered and security reviewed.

No production Ario main, rulesets, signer, trust or #133/#151 change. Preserve records verbatim.
