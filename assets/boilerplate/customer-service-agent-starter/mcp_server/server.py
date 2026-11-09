"""Malmberg's Marinated Meats: local MCP server over fictional sample data.

Stands in for the production Snowflake MCP server (see .mcp.snowflake.example.json).
Claude Code starts it over stdio from .mcp.json. No network, no database, nothing written.
"""

import json
import uuid
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

DATA = Path(__file__).resolve().parent.parent / "data"
AGENT_REFUND_LIMIT = 500.00
SIMULATED_TIMEOUTS = {"MM-1009"}  # carrier system "times out" for this order
# lookup_order returns only these fields; warehouse, margin, and picker data stay internal.
ORDER_FIELDS = ("order_id", "customer_id", "placed_at", "status", "items", "total", "currency",
                "ship_method", "carrier", "tracking_number", "delivery_window", "delivered_at",
                "perishable", "notes")

mcp = FastMCP("malmberg")


def _load(name: str) -> list[dict]:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _find_order(order_id: str) -> dict | None:
    oid = order_id.strip().upper()
    return next((o for o in _load("orders.json") if o["order_id"] == oid), None)


def _error(category: str, message: str, retryable: bool, **details: object) -> ToolError:
    """Structured error: the agent can tell retry-worthy failures from ones to explain or escalate."""
    return ToolError(json.dumps({"errorCategory": category, "isRetryable": retryable, "message": message, **details}))


# BUILD 2: these two descriptions are minimal on purpose. Rewrite them so Claude can tell the
# tools apart: inputs, example requests, edge cases, and when to use the other tool instead.
@mcp.tool()
def get_customer(email: str = "", customer_id: str = "", name: str = "") -> dict:
    """Retrieves customer information."""
    customers = _load("customers.json")
    for field, raw in ("customer_id", customer_id), ("email", email), ("name", name):
        if raw:
            needle = raw.strip().lower()
            matches = [c for c in customers if c[field].lower() == needle]
            return {"count": len(matches), "matches": matches}
    raise _error("validation", "Provide one of: email, customer_id, or name.", retryable=False)


@mcp.tool()
def lookup_order(order_id: str) -> dict:
    """Retrieves order details."""
    order_id = order_id.strip().upper()
    if order_id in SIMULATED_TIMEOUTS:
        # BUILD 2: generic on purpose. Replace with a structured error (see _error and process_refund)
        # so the agent knows this is a transient failure it can retry.
        raise ToolError("Operation failed")
    order = _find_order(order_id)
    trimmed = {k: order[k] for k in ORDER_FIELDS} if order else None
    return {"found": order is not None, "order": trimmed}


@mcp.tool()
def process_refund(order_id: str, customer_id: str, amount: float, reason: str) -> dict:
    """Issue a refund for one order. Simulated: nothing is written.

    Use only after get_customer has confirmed who the customer is and lookup_order has confirmed
    the order belongs to them. Amount is in USD and cannot exceed the order total. Refunds over
    $500 are rejected: use escalate_to_human instead. Returns a refund confirmation ID.
    """
    order = _find_order(order_id)
    if order is None:
        raise _error("validation", f"No order {order_id}.", retryable=False)
    if order["customer_id"] != customer_id.strip().upper():
        raise _error("permission", "That order does not belong to this customer.", retryable=False)
    if order["status"] == "Refunded":
        raise _error("business", "This order was already refunded.", retryable=False,
                     customer_message="Our records show this order has already been refunded.")
    if not 0 < amount <= order["total"]:
        raise _error("validation", f"Amount must be between 0 and the order total ({order['total']}).", retryable=False)
    if amount > AGENT_REFUND_LIMIT:
        raise _error("business", f"Refunds over ${AGENT_REFUND_LIMIT:.0f} need a human.", retryable=False,
                     next_step="escalate_to_human")
    return {"refund_id": f"RF-{uuid.uuid4().hex[:8].upper()}", "order_id": order["order_id"],
            "amount": round(amount, 2), "reason": reason, "simulated": True}


@mcp.tool()
def escalate_to_human(customer_id: str, root_cause: str, recommended_action: str,
                      case_summary: str, refund_amount: float | None = None) -> dict:
    """Hand the case to a human agent who has NOT seen this conversation.

    Use when the customer asks for a person, the refund policy does not cover the request, or a
    refund is over $500. case_summary must stand on its own: order IDs, amounts, dates, and what
    the customer expects.
    """
    return {"ticket_id": f"ESC-{uuid.uuid4().hex[:6].upper()}", "status": "queued",
            "customer_id": customer_id, "refund_amount": refund_amount}


@mcp.resource("malmberg://policies/refunds")
def refund_policy() -> str:
    """Malmberg's refund policy: limits, perishables, and what the policy does not cover."""
    return (DATA / "refund_policy.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
