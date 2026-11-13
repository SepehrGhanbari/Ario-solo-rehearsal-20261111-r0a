# R1i actual stale-success challenge — DO NOT MERGE

This append-only evidence-only commit advances disposable PR #14 from its previously verified successful HEAD A to HEAD B **without executing or requesting a new trusted-app test**.

Evidence at A:
- A SHA: `508a6abfacf534fa01a4b97210c35b35ca965c86`.
- External independently hosted actual unittest: [run 43484108692](https://github.com/SepehrGhanbari/ario-relay-webhook-sandbox-20261112/actions/runs/43484108692); one pinned reference test passed.
- Signed workstation witness: [lab-signed-observation](https://github.com/SepehrGhanbari/ario-relay-webhook-sandbox-20261112/blob/7015d8291dd31ce2422243c3a8ad56490034c6f1/evidence/r1i/2026-11-13/lab-signed-observation.json), Ed25519 public-key SHA-256 `b4aa27898fa77b977c7ae1d46c7a1274eb5a1aa5858548a70f1355dbd6da2e19`. Signed by operator on separate workstation; independent governance key custody **not** proven.
- App `5747504` Check Run [132094820201](https://github.com/SepehrGhanbari/Ario-solo-rehearsal-20261111-r0a/runs/132094820201), exact A, `completed/success`; read back from GitHub.
- Temporarily Ready PR #14 at A reported GitHub `mergeable_state=clean`, then was restored to Draft with **no merge**.
- Local publisher initially reported a read-after-write HOLD due an immediate check-list mismatch; subsequent independent GitHub read confirmed the Check was issued exactly once. No duplicate Check submission occurred.

**Now challenge:** After this new commit, HEAD B must **not** inherit App 5747504 success from A. Under active no-bypass Ruleset 27219627 requiring App 5747504, GitHub should reject an exact-B merge via HTTP 405. On completion, PR returns Draft/HOLD. Never merge, never activate production trust or modify Ario main.
