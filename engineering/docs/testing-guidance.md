# Engineering Pattern Testing Guidance

## Vulnerable and Secure Examples

When practical, provide both:

* a minimal vulnerable example;
* a recommended secure example.

The vulnerable example should exist only to demonstrate the failure mode.

It must:

* be clearly labeled;
* avoid unnecessary dangerous capabilities;
* remain minimal;
* not be presented as production guidance.

The secure example should demonstrate the security invariant rather than merely changing syntax.

Avoid examples where the apparent fix only hides the vulnerability.

## Security Tests

Every mature engineering pattern should include verification guidance.

For guide delivery, the required artifact is a concrete verification method.
Runnable examples, automated suites, and CI are optional extensions selected for
a specific implementation question and maintenance need. Their absence does not
leave an otherwise complete guide unfinished.

For reader-facing guides, provide a compact negative-test checklist with attempted
actions, expected results, evidence and side effects to inspect, and result fields.
Pair it with positive examples. Record untested, passed, failed, or not applicable
with a reason. A checklist describes verification to perform; it is not a record
of successful execution until evidence is supplied. Directly exercise the
enforcement boundary as well as the model path: model refusal alone is insufficient.
Check document consistency and links separately from executing product tests.
Record execution results only for the actual implementation, version, and
environment exercised. When an executable extension is selected, prefer automated
checks for repeatable security outcomes.

Consider:

* positive tests;
* negative tests;
* abuse-case tests;
* authorization failure tests;
* boundary tests;
* injection tests;
* malformed input tests;
* isolation tests;
* tenant-separation tests;
* credential-scope tests;
* failure-mode tests.

Tests should verify the security invariant, not merely implementation details.

Example:

Prefer verifying:

"Tenant A cannot retrieve Tenant B data."

over verifying:

"`tenant_id` is passed to function X."
