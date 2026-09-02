# Engineering Source and Mapping Policy

## Framework Sources and Mapping Assessment

Frameworks provide evidence and context for engineering decisions.

Relevant sources may include:

* OWASP AISVS;
* MITRE ATLAS;
* OWASP GenAI LLM Top 10;
* OWASP Agentic Top 10;
* OWASP MCP Top 10;
* OWASP Agentic Skills Top 10;
* OWASP AI Exchange;
* relevant primary technical specifications.

Mappings are secondary outputs.

They are derived only after a Pattern and the other endpoint have each been
developed independently. Do not use a control inventory or framework coverage gap
to discover Pattern candidates.

Threat-taxonomy content is different from coverage-driven generation. Techniques,
procedures, and case studies may supply evidence of attacker behavior and recurring
attack paths during Pattern discovery. Analyze their technical content first; record
identifier relationships as Mappings only after the Pattern boundary is stable.

The engineering pattern must remain understandable without requiring the reader to interpret the external framework first.

Do not invent mappings for completeness.

A single pattern may map to multiple controls, threats, or risk categories.

Mappings should be based on technical rationale, not keyword similarity.

## Controls and Engineering Are Independent Domains

`engineering/` answers:

"How should we design, implement, and verify this securely?"

`controls/` answers:

"What security property should be assured and how should it be evaluated?"

Neither domain is subordinate to the other.

Do not:

* generate engineering patterns only because a control exists;
* restructure engineering categories to mirror control families;
* modify controls merely to match an implementation;
* claim that one engineering pattern fully satisfies a control without sufficient evidence.

Use explicit mappings to connect the two domains.

Mapping success is not a Pattern maturity requirement. Record an assessed no-match
or gap when no defensible relationship exists.

If engineering work reveals a missing or unclear control mapping, record the gap for follow-up.

## Sources and Current Guidance

AI security changes rapidly.

Before making claims that depend on current specifications, security guidance, or framework content:

1. identify the authoritative source;
2. verify the relevant version or publication status;
3. prefer primary sources;
4. distinguish stable guidance from drafts or public-review material;
5. record significant version dependencies.

Do not silently treat historical guidance as current.

Avoid copying large sections of external source material into this repository.

Prefer references, concise interpretation, and original engineering guidance.
