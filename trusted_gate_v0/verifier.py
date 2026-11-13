"""R1b *simulation*: fail-closed evidence boundary, not a GitHub required check.

The caller, not the untrusted PR, must construct `trusted_source` from a separately
protected execution service. This module contains no authentication, GitHub API,
secrets or check publication. A PASS here NEVER authorizes merge.
"""
from dataclasses import dataclass, field
from typing import Callable, Optional
import re

HEX40 = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class Policy:
    suite_sha: str
    evaluator_sha: str
    producer: str = "R1B_OFFLINE_TRUSTED_FIXTURE"
    required_tests: frozenset[str] = frozenset({
        "fail_closed_on_malformed", "reject_protected_change", "record_exact_head"
    })


@dataclass(frozen=True)
class Snapshot:
    number: int
    head: str
    base: str
    changed_paths: tuple[str, ...]
    previous_paths: tuple[str, ...] = ()
    state: str = "open"
    draft: bool = False
    # This is an untrusted display claim, NEVER consumed as gate evidence.
    claimed_check: str = "success"
    claimed_workflow: str = "python -m pytest"
    claimed_evaluator_sha: str = ""


@dataclass(frozen=True)
class TrustedRun:
    # All fields must come from an actually independent trusted source.
    producer: str
    evaluator_sha: str
    suite_sha: str
    pr_number: int
    head: str
    base: str
    event: str
    status: str
    conclusion: str
    completed_tests: frozenset[str] = field(default_factory=frozenset)
    verified_test_execution: bool = False


@dataclass(frozen=True)
class Decision:
    verdict: str
    reason: str


def _path_allowed(path: str) -> bool:
    if (not isinstance(path, str) or not path or "\\" in path or "\x00" in path
            or path.startswith("/") or any(p in ("", ".", "..") for p in path.split("/"))):
        return False
    # This allowlist is only an *experiment*. It cannot understand semantics.
    return path.startswith("implementation/") and not any(
        segment in path.lower() for segment in (
            "governance", "signer", "secret", "authorization", "genesis", "trust",
            "identity", "memory", "admission", "continuity"
        )
    )


def decide(snapshot: Snapshot, policy: Policy,
           trusted_source: Callable[[int, str], Optional[TrustedRun]],
           read_current: Callable[[int], Snapshot]) -> Decision:
    """Never call or execute PR-supplied evaluators or trust PR-supplied status."""
    def hold(reason: str) -> Decision:
        return Decision("HOLD", reason)

    if snapshot.state != "open" or snapshot.draft:
        return hold("PR_NOT_READY")
    if not isinstance(snapshot.number, int) or snapshot.number < 1:
        return hold("INVALID_PR_NUMBER")
    if not HEX40.fullmatch(snapshot.head) or not HEX40.fullmatch(snapshot.base):
        return hold("INVALID_SHA")
    if not snapshot.changed_paths or not all(_path_allowed(x) for x in
                                             snapshot.changed_paths + snapshot.previous_paths):
        return hold("PROTECTED_OR_UNKNOWN_PATH")
    if not HEX40.fullmatch(policy.suite_sha) or not HEX40.fullmatch(policy.evaluator_sha):
        return hold("UNPINNED_TRUSTED_POLICY")

    try:
        evidence = trusted_source(snapshot.number, snapshot.head)
    except Exception:
        return hold("TRUSTED_SOURCE_UNAVAILABLE")
    if evidence is None:
        return hold("MISSING_INDEPENDENT_EXECUTION")
    if (evidence.producer != policy.producer or
        evidence.evaluator_sha != policy.evaluator_sha or
        evidence.suite_sha != policy.suite_sha):
        return hold("UNTRUSTED_PRODUCER_OR_SUITE")
    if (evidence.pr_number != snapshot.number or
        evidence.head != snapshot.head or evidence.base != snapshot.base):
        return hold("EVIDENCE_SHA_OR_PR_MISMATCH")
    if evidence.event != "trusted_external_run" or evidence.status != "completed":
        return hold("NO_COMPLETED_TRUSTED_EXECUTION")
    if evidence.conclusion != "success" or not evidence.verified_test_execution:
        return hold("NO_VERIFIED_TEST_PASS")
    if evidence.completed_tests != policy.required_tests:
        return hold("TRUSTED_SUITE_INCOMPLETE")

    # Re-fetching reduces staleness but is NOT atomic with a future GitHub merge.
    try:
        current = read_current(snapshot.number)
    except Exception:
        return hold("FRESH_SNAPSHOT_UNAVAILABLE")
    if current != snapshot:
        return hold("MUTABLE_PR_STATE_CHANGED")
    return Decision("ACCEPT_LAB_ONLY", "TRUSTED_FIXTURE_PASSED_NOT_MERGE_AUTHORITY")
