# R1b off-PR read-only auditor — separately sourced laboratory reference

**Status: RESEARCH / HOLD.** This reference branch is separate from Draft PR #9. The operational Python program was authored and executed outside the PR checkout on the owner's authorized workstation. It accessed GitHub public REST read-only APIs; it did NOT execute code from PR #9.

## Exact source

- File: `external_auditor_v02.py`.
- Git blob SHA-1: `9a03e9b11945c8273950b731a102a496ac555381`.
- Local executor SHA-256: `1a293c6b5d14521cdc26d03bea15f0ba81dd21d6ba3642b5ac4f7dc2382f6d5d`.
- Audit target: Draft [disposable PR #9](https://github.com/SepehrGhanbari/Ario-solo-rehearsal-20261111-r0a/pull/9), expected head `d9c889ec3d14f2b3de1317ed2d70d70dca00b328`.

## Observed test

UTC `2026-11-13T16:00:16Z`: live REST readback verified exact PR head/base, all three archived code blobs, complete git tree, stable before/after PR metadata and expected file list. The auditor returned `HOLD` because the research PR remains Draft and no separately authenticated producer is installed. The version 0.2 executable used a **nonzero process exit for HOLD**. The original local version 0.1 that mistakenly returned zero exit for HOLD is preserved for audit, not silently overwritten.

## Critical limits

A separate execution source and read-only live GitHub API call do **not** create an independent GitHub App identity, an externally authenticated Check Run, replay-resistant event log, protected CI status, or atomic merge-time gate. This branch itself is unprotected and is **not** a source of authority; pin to its immutable commit and verify blob bytes before independent reuse. No GitHub Actions job or PR-specific required check is installed by this work. #133/#151 and Ario main stay HOLD/unchanged.

For code inspection only; do not merge this reference branch or treat its workflow status as clearance.
