Event: PreToolUse
Matches: <Placeholder: which MCP tool?>

Checks the tool input for:
- <Placeholder>
- <Placeholder>
- <Placeholder>

<Placeholder> → <Placeholder: allow (exit 0)>
<Placeholder> → <Placeholder: block (exit 2) and tell Claude what to do instead>

On block: print to stderr and exit 2. The message must start with exactly
`BLOCKED by refund-limit hook:` so you can tell the hook fired, not the server's own check.
