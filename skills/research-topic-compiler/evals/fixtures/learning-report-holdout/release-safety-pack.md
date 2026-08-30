# Frozen holdout: feature-flag release safety

This synthetic, non-AI topic is an independent transfer holdout for the learning-report contract. It was not used to design the editorial template.

## System snapshot

A SaaS team deploys application code once per day. A new billing flow is guarded by a server-side boolean feature flag. Product managers can turn the flag on for a percentage of accounts, but the current system has no explicit exposure record attached to a user action.

Observed facts from the supplied system description:

- Deployment and release are separate operations.
- The flag service returns one boolean value per request.
- A configuration audit log records who changed the rollout percentage and when.
- Application logs record request IDs and errors but not the evaluated flag version.
- Payment requests have an idempotency key.
- Customer support can identify an account and transaction but cannot reconstruct the exact flag decision for that transaction.
- Rollback guidance says "set rollout to zero"; it does not state how long stale caches may continue serving the enabled value.

## Incident vignette

During a 10% rollout, payment errors rise for one region. The team sets the flag to zero. Error volume falls over nine minutes, but some successful retries create confusing duplicate confirmation messages. The material does not prove whether the delay came from caches, in-flight requests, regional propagation, or logging latency.

## Reader and decision

The primary reader is a product manager who understands feature flags at a basic level. They need to learn why a flag is not itself a safe release system, compare the current system with a decision-record model, and define a bounded improvement plan with acceptance and stop criteria.

## Boundaries

- Do not prescribe a vendor.
- Do not infer the live incident root cause from this static pack.
- A percentage rollout is not necessarily a randomized experiment.
- Keep detailed evidence in an endnote or collapsed audit appendix.
