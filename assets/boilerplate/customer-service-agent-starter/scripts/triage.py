"""Classify one ticket with Claude Code in non-interactive mode (Build 4).

Usage: python scripts/triage.py data/tickets/ticket-01.txt

Runs: claude -p --output-format json --json-schema "<schema>"   (prompt + ticket on stdin)
The prompt goes on stdin and the schema as one compact line: Windows CLI shims cut arguments at newlines.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
        print(__doc__)
        return 1
    claude = shutil.which("claude")
    if claude is None:
        print("Claude Code CLI not found on PATH. Install it first.")
        return 1
    prompt = (ROOT / "schemas" / "triage_prompt.md").read_text(encoding="utf-8")
    ticket = Path(sys.argv[1]).read_text(encoding="utf-8")
    schema = json.loads((ROOT / "schemas" / "ticket_triage.schema.json").read_text(encoding="utf-8"))
    cmd = [claude, "-p", "--output-format", "json", "--json-schema", json.dumps(schema, separators=(",", ":"))]
    return subprocess.run(cmd, cwd=ROOT, input=f"{prompt}\n\n## Ticket\n{ticket}", text=True, encoding="utf-8").returncode


if __name__ == "__main__":
    sys.exit(main())
