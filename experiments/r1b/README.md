# R1b — independent evidence-source boundary (offline pilot, HOLD)

**Experimental evidence only. Not an installed GitHub check or merge authority.**

The related Ario research candidates are [#133](https://github.com/SepehrGhanbari/Ario/pull/133) and [#151](https://github.com/SepehrGhanbari/Ario/pull/151), both still HOLD. R0 previously failed; R1b does not upgrade that outcome.

## Executed local simulation — 2026-11-13

- Python standard-library `unittest`, no credentials, network, GitHub mutations or untrusted code execution.
- **18/18 tests PASS** (local run only; hosted GitHub execution NOT claimed).
- Baseline is explicitly `ACCEPT_LAB_ONLY`, NEVER actual merge permission.
- All five preregistered attacks resulted in **HOLD**: PR prints fake `exit 0` green, PR removes tests from its own workflow, `skipped`, `neutral`, and head/base SHA drift during audit.
- Additional HOLD tests: wrong producer, incomplete trusted suite, replay from another PR, modified protected paths / rename from protected path, missing or unpinned evaluator, stale run and lost mutable-state snapshot.
- Critically, a caller must provide a *separate* trusted evidence source; the evaluator does not consume PR-provided success text. That source is a test fixture, **not authenticated**, in this pilot.

## Provenance and reproduction

The runnable Python source, 18 tests, stdout, SHA-256 manifest and explicit limitations are preserved in the conversation attachment named `ario_trusted_gate_pilot_R1b.zip` (not published in this repository; do not represent this Markdown as a release of its source).

Archive SHA-256 (locally computed):
`6e0e3210d439eba662037f119872a5adf982f75f56ae87c9c61b7270a11971c5`

After independently obtaining the archive, extract and run:

```bash
python -m unittest discover -s trusted_gate_v0/tests -p 'test_*.py' -v
```

## What is NOT proven

No separately controlled runner, authenticated producer identity, GitHub App check publisher, durable deleted-review HOLD, or atomic PR-status-to-merge recheck is in place. A caller who lets the PR forge the separate `TrustedRun` defeats this fixture. The lab illustrates **a trust boundary required for future enforcement**, not a security claim.

The original rehearsal repo `main`, Ario `main`, all Rulesets, keys, signer, Trust, Genesis and PR #133/#151 remain unchanged by this experiment. No current CI status may be treated as an independent attestation.
