---
name: shared-agent-memory
description: Connect isolated agents to shared MCP memory safely.
version: 0.1.0
author: Natalie, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [MCP, shared-memory, gbrain, Hermes, RBAC]
    related_skills: [hermes-agent]
---

# Shared Agent Memory

Connect isolated Hermes profiles to a shared MCP memory service without sharing credentials, overgranting write access, or treating a superficial HTTP response as proof. Use this for gbrain-like memory services that expose separate write, recall, and coordination MCP endpoints.

## When to Use

- A user wants several agents to read and write a common memory or knowledge base.
- A shared MCP server uses per-agent Bearer credentials and scoped vault paths.
- An agent must retain technical decisions, runbooks, source notes, handoffs, or team knowledge across sessions.

Do not use this to store primary work artifacts such as full content plans, Word documents, or media files. Use the shared memory for durable knowledge, sources, decisions, and handoffs; use the appropriate document store for primary artifacts.

## Prerequisites

- MCP services are active and bound to intended local or protected network endpoints.
- Each Hermes agent has a dedicated profile and gateway service.
- The MCP server supports independently issued per-agent credentials and write/read scopes.
- Hermes supports HTTP MCP servers with static headers.

## Architecture

1. Give each agent its own identity and token. Never reuse an admin token or another agent's token.
2. Store raw tokens only in that profile's protected `.env`.
3. Add MCP endpoints through `hermes mcp add`, which persists an `${MCP_<SERVER>_API_KEY}` reference in `config.yaml`, not the raw token.
4. Apply least-privilege write scopes by role; choose read scopes deliberately.
5. Treat the service's tool-gating mode as a global security boundary. Enabling a full tool set can expose more tools to every connected agent even when per-agent scopes remain unchanged.

## Recommended Scope Design

Start from the agent's role and map it to concrete shared-memory sections.

| Role | Typical write scopes |
|---|---|
| Coder / infrastructure agent | decisions, runbooks, error patterns, handoffs |
| Content / research agent | external sources, distilled knowledge, handoffs |
| Coordinator | daily logs, decisions, knowledge, runbooks, handoffs |

A scope grants only the corresponding server-side operation. Do not grant a scope simply because a folder exists: first confirm that a published MCP tool can create or update that document type.

## Procedure

1. **Verify the server before changing any agent.** Confirm every service is active and listen addresses are intentional. For StreamableHTTP MCP, use a real `initialize` handshake before `tools/list`; a direct `tools/list` request can correctly fail for lack of a session ID.
2. **Inspect tool publication.** Run `hermes mcp test <name>` with a temporary or intended profile configuration. Confirm required tool names are actually in the published list. Do not assume source code means a tool is available: global tool-gating may hide it.
3. **Issue one restricted token per agent.** Set write and read scopes explicitly. Capture the token directly into the profile `.env` without printing it, logging it, or placing it in shell history.
4. **Add write, recall, and coordination endpoints.** Use `HERMES_HOME=<profile-home> hermes mcp add <name> --url <endpoint> --auth header`. Confirm authentication is recognized from the profile env, enable only intended tools, and verify `hermes mcp list`.
5. **Inspect the saved configuration.** Confirm every Authorization value is an env interpolation such as `Bearer ${MCP_GBRAIN_MEMORY_API_KEY}`. The raw credential must not occur in `config.yaml`.
6. **Restart only the affected profile gateway from an external shell.** A gateway cannot reliably restart itself from one of its own child sessions. After restart, start a fresh Telegram session with `/new` before testing, because persisted sessions can retain the old MCP tool catalog.
7. **Run a real read test and a useful write test.** For the write test, create a meaningful decision or handoff rather than disposable test garbage. Verify the write in all server-side representations: vault file, indexed document row, and audit event.
8. **Record boundaries.** Tell the user which content belongs in shared memory versus their document store.

## Verification

- `hermes mcp list` shows every intended server enabled for the target profile.
- `hermes mcp test <server>` discovers the expected tool set.
- The target gateway returns to `active (running)` after restart.
- A fresh Telegram session can perform a recall call.
- A meaningful write produces a vault file, indexed document, and successful write audit record.

## Pitfalls

- **Legacy smoke tests can be false negatives.** A test that posts `tools/list` without StreamableHTTP initialization will receive a missing-session response even when the server is healthy. Verify through the actual MCP client or a full `initialize → session ID → tools/list` sequence.
- **Read operations may not be audit logged.** Absence of a recall row in a write-oriented audit table does not prove the agent skipped the tool. Use MCP/server access logs or an explicitly instrumented read audit path.
- **Global tool gating changes every agent's surface.** Before switching from a core tool set to all tools, assess every already-connected profile and restart the affected MCP services. Scopes still enforce authorization, but exposed tools alter agent behavior.
- **A shared-memory service is not a Drive replacement.** It is for durable team knowledge and traceable operational records, not the canonical store for formatted documents and media assets.
- **Do not hand-edit Hermes YAML.** Use `hermes mcp add` and other Hermes CLI commands so environment interpolation and validation remain intact.
