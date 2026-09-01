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

Prefer automated tests when practical.

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
