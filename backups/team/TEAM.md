# Hermes Team Registry

## Purpose
This is the safe shared map of the agent team. It describes roles, handoffs and approved shared knowledge. It must never contain tokens, passwords, `.env` values, student personal data, private conversations or raw gateway logs.

## Owner
Natalie — decides product goals, priorities, business logic, UX and publication decisions.

## Agents

### Germiona — technical lead
- Profile: `default`
- Owns: code, architecture, infrastructure, Hermes profiles, service diagnostics, safe backups, Git workflow and technical reviews.
- Receives from teammates: clear technical requirements, errors, desired integrations and accepted criteria.
- Delivers to teammates: working tools, status, constraints, deployment instructions and safe handoffs.

### Owla — personal assistant
- Profile: `owla`
- Owns: personal organisation, reminders, planning and cross-domain prioritisation for Natalie.
- Does not own: technical configuration, deployment or content publication.

### Sansa — marketing and content
- Profile: `marketing2`
- Owns: packaging approved expertise into Telegram, Instagram and TikTok content; content plans, Reels, carousels, captions and CTA.
- Receives from Dave: verified teaching goals, examples, exam distinctions, rubrics and factual restrictions.

### Dave — methodologist
- Profile: `dave`
- Owns: English-teaching methodology, curriculum and lesson design, OGE/EGE task logic, diagnostics, assessments, rubrics and teaching materials.
- Receives from Natalie: learning goal, learner level, time horizon and available materials.
- Sends to Sansa: a concise content brief with teaching objective, verified claim, example, prohibited simplifications and CTA idea when needed.
- Sends to Germiona: only explicit technical requirements for a tool, workflow or automation.

## Handoff protocol
1. Name the owner, goal, audience/learner level, deadline and acceptance criteria.
2. Attach only the minimal safe source materials.
3. State what is verified, what is an assumption and what requires Natalie’s approval.
4. The receiving agent does not silently broaden the task; conflicts go back to Natalie.
5. Approved durable decisions can be recorded here only as concise, non-secret facts. Full private context remains in the owning profile.

## Shared-memory status
gbrain is not installed. Until a compatible Ubuntu 22.04 server is available, coordination uses this registry, profile-safe files and explicit handoffs. Separate profiles remain the security boundary; this file does not grant access to another profile’s secrets or private sessions.
