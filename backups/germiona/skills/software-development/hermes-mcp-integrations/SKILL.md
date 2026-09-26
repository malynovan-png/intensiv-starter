---
name: hermes-mcp-integrations
description: "Connect Hermes profiles to authenticated MCP servers."
version: 0.1.0
author: Natalie, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, MCP, StreamableHTTP, authentication, profiles]
    related_skills: []
---

# Hermes MCP Integrations

Use when connecting an isolated Hermes profile to an external MCP server, especially an authenticated Streamable HTTP endpoint. Keep credentials scoped per profile and verify real tool discovery before declaring the integration active.

## When to Use

- A Hermes Telegram/CLI profile needs tools from a remote or localhost MCP server.
- An MCP server uses Bearer authentication or Streamable HTTP sessions.
- A team needs separate credentials and permissions for each agent profile.

Do not use for a one-off raw HTTP request or a stdio tool that does not need persistent Hermes configuration.

## Procedure

1. Inspect the target profile and existing MCP setup before changing it:
   ```bash
   hermes profile show <profile>
   HERMES_HOME="$HOME/.hermes/profiles/<profile>" hermes mcp list
   ```
   Confirm the endpoint is reachable and discoverable with the intended credential before changing the profile.

2. Use one credential per agent profile. Give the agent only the read/write scopes it needs. Store each token only in that profile's `.env`; never put a raw token in `config.yaml`, terminal output, chat, or Git.

3. Add HTTP MCP endpoints with the Hermes CLI under the target profile:
   ```bash
   HERMES_HOME="$HOME/.hermes/profiles/<profile>" \
     hermes mcp add <server-name> --url "http://127.0.0.1:<port>/mcp" --auth header
   ```
   When prompted, Hermes stores the credential in a profile env variable and persists only an `${MCP_<SERVER>_API_KEY}` interpolation in `mcp_servers`.

4. Verify configuration without exposing secrets:
   ```bash
   HERMES_HOME="$HOME/.hermes/profiles/<profile>" hermes mcp list
   ```
   Check that every expected server is enabled and discovered tools are non-empty.

5. Restart the target gateway from a separate terminal session, not from a command running inside that same gateway:
   ```bash
   systemctl --user restart hermes-gateway-<profile>.service
   systemctl --user is-active hermes-gateway-<profile>.service
   ```
   Then send `/new` to the Telegram bot. A gateway restart does not erase an existing Telegram session; a new session refreshes its tool catalog.

6. Verify the real user path with a read-only request that forces one MCP tool call. Do not accept a prose claim that the agent "has the tool" as proof.

## Streamable HTTP Verification

A raw `tools/list` POST can fail with `400 Missing session ID` even when the server is healthy. Streamable HTTP MCP requires this sequence:

1. POST `initialize`.
2. Read the returned `mcp-session-id` response header.
3. Send `notifications/initialized` if required by the client.
4. POST `tools/list` with the `mcp-session-id` header.

Treat a successful `initialize` plus `tools/list` as the protocol health check. Do not change a healthy server merely because an old smoke test skips this handshake.

## Pitfalls

- Do not hand-edit `config.yaml`; use `hermes mcp add` or `hermes config set` so YAML and profile resolution remain valid.
- Do not reuse one team-wide Bearer token for every profile. Revocation and least-privilege scopes depend on per-agent tokens.
- `127.0.0.1` endpoints are valid only when the Hermes gateway and MCP server run on the same host.
- If restart is blocked with a self-termination warning, that is expected: open a separate VS Code/SSH terminal and run the restart there.
- Do not confuse an outdated liveness script's old route or missing session header with an MCP service outage; verify the current protocol handshake first.

## Completion Criteria

- Credentials are present only in the intended profile `.env`.
- `hermes mcp list` reports every expected server as enabled.
- The restarted gateway is `active`.
- A fresh Telegram session calls an MCP tool successfully.
