"""Pre-registered R1b attacks: exact-head checks must fail closed."""
import unittest
from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier import Policy, Snapshot, TrustedRun, decide

A, B = "a" * 40, "b" * 40
POLICY = Policy(suite_sha="c" * 40, evaluator_sha="d" * 40)
PR = Snapshot(number=7, head=A, base=B,
              changed_paths=("implementation/example.py",))
RUN = TrustedRun(producer=POLICY.producer, evaluator_sha=POLICY.evaluator_sha,
                 suite_sha=POLICY.suite_sha, pr_number=PR.number,
                 head=A, base=B, event="trusted_external_run",
                 status="completed", conclusion="success",
                 completed_tests=POLICY.required_tests, verified_test_execution=True)


def verdict(pr=PR, run=RUN, now=None, policy=POLICY):
    # `trusted_source` is a different provider from `pr.claimed_check`.
    return decide(pr, policy, lambda n, sha: run,
                  lambda n: pr if now is None else now)


class R1bAdversarialPilot(unittest.TestCase):
    def assertHold(self, decision, reason):
        self.assertEqual(decision.verdict, "HOLD")
        self.assertEqual(decision.reason, reason)

    def test_00_valid_trusted_fixture_accepted_only_in_lab(self):
        self.assertEqual(verdict().verdict, "ACCEPT_LAB_ONLY")

    def test_01_fake_green_exit_zero_cannot_replace_trusted_run(self):
        forged = replace(PR, claimed_check="success", claimed_workflow="exit 0")
        self.assertHold(verdict(pr=forged, run=None), "MISSING_INDEPENDENT_EXECUTION")

    def test_02_pr_removes_tests_external_suite_detects_gap(self):
        claimed = replace(PR, claimed_check="success", claimed_workflow="echo tests passed")
        omitted = replace(RUN, completed_tests=POLICY.required_tests - {"reject_protected_change"})
        self.assertHold(verdict(pr=claimed, run=omitted), "TRUSTED_SUITE_INCOMPLETE")

    def test_03_skipped_trusted_check_rejected(self):
        self.assertHold(verdict(run=replace(RUN, conclusion="skipped", verified_test_execution=False)),
                        "NO_VERIFIED_TEST_PASS")

    def test_04_neutral_trusted_check_rejected(self):
        self.assertHold(verdict(run=replace(RUN, conclusion="neutral", verified_test_execution=False)),
                        "NO_VERIFIED_TEST_PASS")

    def test_05_pr_head_moves_after_evidence_read(self):
        newer = replace(PR, head="e" * 40)
        self.assertHold(verdict(now=newer), "MUTABLE_PR_STATE_CHANGED")

    def test_06_base_moves_after_evidence_read(self):
        newer = replace(PR, base="e" * 40)
        self.assertHold(verdict(now=newer), "MUTABLE_PR_STATE_CHANGED")

    def test_07_success_claim_without_proof_rejected(self):
        self.assertHold(verdict(run=replace(RUN, verified_test_execution=False)),
                        "NO_VERIFIED_TEST_PASS")

    def test_08_fake_producer_and_attacker_supplied_evaluator_sha_rejected(self):
        forged = replace(PR, claimed_evaluator_sha=POLICY.evaluator_sha)
        self.assertHold(verdict(pr=forged, run=replace(RUN, producer="attacker-check")),
                        "UNTRUSTED_PRODUCER_OR_SUITE")

    def test_09_replayed_success_from_other_pr_rejected(self):
        self.assertHold(verdict(run=replace(RUN, pr_number=99)),
                        "EVIDENCE_SHA_OR_PR_MISMATCH")

    def test_10_workflow_edit_not_eligible_for_routine_gate(self):
        guarded = replace(PR, changed_paths=(".github/workflows/ci.yml",))
        self.assertHold(verdict(pr=guarded), "PROTECTED_OR_UNKNOWN_PATH")

    def test_11_rename_out_of_protected_path_rejected(self):
        guard = replace(PR, previous_paths=(".github/CODEOWNERS",))
        self.assertHold(verdict(pr=guard), "PROTECTED_OR_UNKNOWN_PATH")

    def test_12_missing_trusted_runner_rejected(self):
        self.assertHold(verdict(run=None), "MISSING_INDEPENDENT_EXECUTION")

    def test_13_unpinned_policy_rejected(self):
        self.assertHold(verdict(policy=replace(POLICY, evaluator_sha="latest")),
                        "UNPINNED_TRUSTED_POLICY")

    def test_14_stale_or_wrong_head_run_rejected(self):
        self.assertHold(verdict(run=replace(RUN, head="f" * 40)),
                        "EVIDENCE_SHA_OR_PR_MISMATCH")

    def test_15_real_fail_rejected(self):
        self.assertHold(verdict(run=replace(RUN, conclusion="failure", verified_test_execution=True)),
                        "NO_VERIFIED_TEST_PASS")

    def test_16_current_snapshot_unavailable_rejected(self):
        d = decide(PR, POLICY, lambda n, h: RUN,
                   lambda n: (_ for _ in ()).throw(RuntimeError("offline")))
        self.assertHold(d, "FRESH_SNAPSHOT_UNAVAILABLE")

    def test_17_untrusted_claim_does_not_override_independent_pass(self):
        # Only in a controlled lab: PR changing its own displayed claim doesn't
        # affect the trusted evidence, showing separation of data sources.
        changed = replace(PR, claimed_check="failure", claimed_workflow="exit 1")
        self.assertEqual(verdict(pr=changed).verdict, "ACCEPT_LAB_ONLY")


if __name__ == "__main__":
    unittest.main()
