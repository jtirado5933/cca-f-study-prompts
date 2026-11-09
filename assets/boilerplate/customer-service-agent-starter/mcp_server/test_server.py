"""Self-check for the MCP server tools. Run: python mcp_server/test_server.py"""

import json

from server import ToolError, get_customer, lookup_order, process_refund


def error_of(fn, *args, **kwargs) -> dict:
    try:
        fn(*args, **kwargs)
    except ToolError as exc:
        return json.loads(str(exc))
    raise AssertionError("expected a ToolError")


assert get_customer(name="Sam Ortega")["count"] == 2           # two matches: ask for another identifier
assert get_customer(email="nobody@example.com")["count"] == 0  # valid empty result, not an error
assert lookup_order("mm-1002")["order"]["status"] == "Shipped"
assert lookup_order("MM-9999")["found"] is False
assert process_refund("MM-1001", "C-001", 20.0, "warm on arrival")["simulated"] is True
assert error_of(process_refund, "MM-1003", "C-002", 712.0, "warm")["next_step"] == "escalate_to_human"
assert error_of(process_refund, "MM-1001", "C-002", 10.0, "x")["errorCategory"] == "permission"
assert error_of(process_refund, "MM-1007", "C-006", 10.0, "x")["errorCategory"] == "business"
print("ok")
