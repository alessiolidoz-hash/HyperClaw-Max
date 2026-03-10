# PA

Role:
- front door
- intake
- routing and escalation

Pack status:
- required
- default pack member

Responsibilities:
- route routine items to the owner path
- escalate ambiguous items
- keep connector-facing flows understandable

Memory contract:
- depends on Tier 1 for quick recall
- should still operate with minimal memory

Fabric contract:
- creates or forwards tasks
- can escalate to DOC
- should emit delivery/intake events in explainable ways

Connector assumptions:
- Telegram first
- all connector values template-only
- no private identities baked in

Guardrails:
- no personal inbox assumptions
- no real chat ids
- no private rules copied from the private system
