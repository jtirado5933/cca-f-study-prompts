Event: PreToolUse
Matches: <Placeholder>
Checks: <Placeholder: what must already be true before this tool may run?>

<Placeholder> → <Placeholder>
<Placeholder> → <Placeholder>

On block: print to stderr and exit 2. The message must start with exactly
`BLOCKED by order-ownership hook:` so you can tell the hook fired, not the server's own check.
