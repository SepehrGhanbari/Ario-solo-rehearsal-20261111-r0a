# R1c real-ruleset negative probe (DISPOSABLE / DO NOT MERGE)
This pull request intentionally replaces the `solo-required-context` test with `exit 0`. It is an **adversarial test fixture**, not legitimate CI. The check should appear green with GitHub Actions App `15368` despite **no tests being executed**. Do not interpret that as trusted evidence.

The existing disposable ruleset `27069097` requires one Code Owner review; it has no required-status rule and no bypass. The specific question for the experiment is whether a PR *without* such review can merge despite a green fake Actions job. A refused merge proves the review gate blocked this single operation; it does NOT prove a trusted App-bound check or anti-spoof protection.

Any unexpected merge would be an R1c governance FAIL and must be reported without deleting or rewriting evidence. No real Ario repository files/rulesets are touched.
