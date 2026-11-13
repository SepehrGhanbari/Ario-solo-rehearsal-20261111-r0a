# Ario R1b — isolated evidence-source boundary (LAB / HOLD)

**Research fixture only. Not installed. Not an independent GitHub check. No merge authority.**

This small prototype follows the lessons of Ario #133/#151 and the failed R0 solo-governance rehearsal. It separates **untrusted PR claims** from a **trusted external evidence source**. It is deliberately bounded and cannot be used to bypass current main rulesets.

## Threat model and preregistered falsifiers

The adversarial inputs are (1) `exit 0` fake green, (2) tests deleted from PR workflow, (3) skipped, (4) neutral, (5) head/base changing after evidence collection. Other controls reject replay from another PR, wrong producer/suite, missing runner, unpinned evaluator, protected path or rename, and stale evidence. In every attack the verdict must be `HOLD`; a true-success *fixture* may return only `ACCEPT_LAB_ONLY`.

The evaluator does **not** consume `Snapshot.claimed_check`, `claimed_workflow` or `claimed_evaluator_sha` as authority. The separate `trusted_source` function must be supplied by the **caller**, not by PR code. It must return results from a protected evaluator whose exact code, test suite and execution source are independently verified. A forged Python object passed as `TrustedRun` in real life would bypass this demonstration: **the source authentication is intentionally NOT implemented here**.

## Run offline

```sh
python -m unittest discover -s trusted_gate_v0/tests -p 'test_*.py' -v
```

No networking, credentials, filesystem changes, GitHub settings changes or external services required by this code. Standard library only. These tests do **not** execute any untrusted repository code or assert PR security.

## Why this is not installed protection

A GitHub Actions job defined by the PR can print `success`, skip tests or change its own workflow; its GitHub Actions App ID does not authenticate the test semantics. Even a trusted evaluator that re-reads mutable PR metadata cannot make that read atomic with a later merge. Closing the production gap needs an independently administered **source and producer**, its own authenticated check publication, an event delivery/recheck strategy, a durable deletion/edited-review HOLD, and a tested repo rule requiring that exact producer. For #133/#151, no governance/trust installation is authorized here. Fail closed until those preconditions are demonstrated.

R0 is historical **FAIL**; R1a is local-only; this fixture is **R1b local pilot**, no upgrade of prior results.
