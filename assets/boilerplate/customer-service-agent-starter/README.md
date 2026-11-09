# Customer Service Agent starter

Hands-on starter for the Trace3 CCA-F prep workshop. You finish a Claude Code customer service agent
for Malmberg's Marinated Meats, a fictional company. All data in `data/` is made up.

It mirrors the exam's **Customer Support Resolution Agent** scenario: the four MCP tools
`get_customer`, `lookup_order`, `process_refund`, and `escalate_to_human`.

Step-by-step build checklist: see the Workshop section of the study site.

## Setup

1. Install Claude Code and sign in.
2. From this folder:
   ```
   pip install -r requirements.txt
   python mcp_server/test_server.py      # prints "ok"
   claude
   ```
3. Accept the "trust this folder" prompt. Until you do, Claude Code ignores the `allow` rules in
   `.claude/settings.json` (and `claude -p` in Build 4 asks permission for everything).
4. In Claude Code, run `/mcp`. You should see `malmberg` connected with four tools.

Python must be on your PATH as `python` (on macOS you may need to change `.mcp.json` to `python3`).
Always start `claude` from this folder so `mcp_server/server.py` resolves.

**MCP won't install?** Tell Claude: "The MCP server is unavailable. Read customers and orders from
`data/*.json` directly and follow the same rules." You still complete every build except Build 2.

## Builds

| Build | Exam domain | You fill in |
|---|---|---|
| 1 | Claude Code config (20%) | `CLAUDE.md` Commands, `.claude/rules/mcp-tools.md`, `.claude/skills/example-skill/SKILL.md` |
| 2 | Tool design & MCP (18%) | Tool descriptions and the `lookup_order` error in `mcp_server/server.py` |
| 3 | Agentic architecture (27%) | `.claude/agents/Subagent.md`, `.claude/hooks/Hook1.md` + `Hook2.md`, `.claude/commands/Slash.md`, hook wiring in `.claude/settings.json` |
| 4 | Prompting & structured output (20%) | `schemas/ticket_triage.schema.json` (it has 3 flaws), `schemas/triage_prompt.md`, then `python scripts/triage.py data/tickets/ticket-01.txt` |
| 5 | Context & reliability (15%) | `CLAUDE.md` Escalation criteria and Case facts |

Rename the templates as you fill them: `Subagent.md` → `escalation-investigator.md`,
`Slash.md` → `process-refund.md` (the file name becomes the `/command`), `example-skill/` → your skill name.

## What's in here

```
CLAUDE.md                        project memory, always loaded
.mcp.json                        local MCP server (project scope)
.mcp.snowflake.example.json      production reference only: Snowflake MCP with ${ENV} credentials
.claude/settings.json            permissions (allow / ask / deny) and, after Build 3, hooks
.claude/settings.md              document your settings and hook exit codes here
.claude/rules/                   path-scoped rules (load only when matching files are touched)
.claude/skills/ agents/ commands/ hooks/   templates
mcp_server/server.py             the four tools + refund policy resource
data/                            fictional customers, orders, policy, and tickets
schemas/ scripts/                ticket triage schema, prompt, and runner
```
