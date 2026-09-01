# Standards and Knowledge Maintenance

AI-security guidance changes quickly. Maintenance is a first-class security property of this repository.

## Goal

Keep engineering guidance current without letting an automated agent silently rewrite security decisions.

## Source lifecycle

Each tracked source is recorded in `sources/registry.yaml` with at least:

- role
- canonical URL
- maturity/status
- current version or rolling state
- last verified date
- update notes

The repository must distinguish stable releases from beta, draft, public-review, deprecated, superseded, and rolling content.

## Recommended check cadence

Cadence is risk-based rather than uniform:

| Source state | Suggested check |
|---|---|
| stable/versioned | release-driven + monthly sanity check |
| draft/public-review/beta | weekly |
| rolling taxonomy/knowledge base | weekly |
| active incident or security-significant change | as needed |

A check does not imply a repository update.

## Update workflow

Do not perform "sync latest" as a blind rewrite.

### 1. Detect

Identify a version, content, status, or taxonomy change at the primary source.

### 2. Establish source state

Record:

- previous version/status
- new version/status
- publication/release date where known
- canonical upstream references

### 3. Semantic diff

Classify changes by meaning, not just text:

- editorial
- clarification
- new requirement/risk/technique
- removed requirement/risk/technique
- materially modified requirement
- identifier change
- taxonomy/structure change
- maturity/status change
- deprecation/supersession
- security-significant change

### 4. Impact analysis

Search for affected:

- source registry entries
- control interpretations
- mappings
- engineering patterns
- implementations
- tests
- architecture diagrams
- operational guidance

### 5. Proposal

Create a review artifact using `templates/framework-update-review.md`.

The proposal should explicitly separate:

- `UPDATE`
- `NO CHANGE`
- `REVIEW REQUIRED`
- `DEPRECATE`

### 6. Human security review

Security-significant changes require human judgment before merging.

Agents may prepare diffs, mapping candidates, migration notes, and test changes. They must not treat upstream publication as automatic approval of an internal engineering recommendation.

### 7. Preserve traceability

When an identifier changes, determine whether it was renamed, split, merged, replaced, or removed. Preserve historical links when useful.

## Why not fork AISVS as the main knowledge repository?

AISVS is valuable as a control backbone, but mixing organization-specific implementation examples directly into a long-lived fork creates avoidable coupling to upstream structure.

Preferred model:

- upstream AISVS remains the source of truth for AISVS text;
- this repository records versioned AISVS references;
- original engineering patterns are maintained independently;
- a mapping layer connects the two.

This makes upstream upgrades easier and reduces the risk of stale copied standard text.

## Automation boundary

The desirable automation target is:

```text
Upstream sources
  -> scheduled detection
  -> diff
  -> agent-assisted classification
  -> impact analysis
  -> Issue / PR proposal
  -> human review
  -> merge
```

Avoid:

```text
Upstream changed
  -> agent rewrites guidance
  -> auto-merge
```

## Staleness

A framework mapping is potentially stale when its upstream source changes after the mapping's last review.

Future automation should report staleness rather than pretending to prove current alignment automatically.

## Metrics worth tracking later

Prefer engineering-quality metrics over framework-coverage vanity metrics, for example:

- recommended patterns with executable abuse/regression tests;
- patterns reviewed after an upstream security-significant change;
- time from relevant upstream change to impact triage;
- stale mapping count;
- patterns adopted by engineering teams;
- security issues prevented/detected by a pattern or test.
