"""Day 2, lesson 4: a tiny MCP server over made-up saree data (exam topic 2.4).

Run by a client as a subprocess and spoken to over stdin/stdout (the 'stdio' transport).
It offers two kinds of things:
  - tools:     things Claude can DO (look up, calculate)
  - resources: things Claude (or the app) can READ, like a catalogue
All data below is sample data for learning, not real weaver facts.
"""
import json
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("weaves")

WEAVES = {
    "kanchipuram": {"region": "Tamil Nadu", "material": "pure mulberry silk, zari", "price_inr": [15000, 150000]},
    "banarasi": {"region": "Uttar Pradesh", "material": "silk, brocade", "price_inr": [8000, 100000]},
    "jamdani": {"region": "West Bengal", "material": "fine cotton", "price_inr": [3000, 40000]},
    "chanderi": {"region": "Madhya Pradesh", "material": "silk-cotton", "price_inr": [2500, 20000]},
}


@mcp.tool()
def list_weaves_by_region(region: str) -> dict:
    """List the NAMES of handloom weaves traditionally made in one Indian state.

    Input: a state name such as 'Tamil Nadu' (capital letters do not matter).
    Returns a list of weave names, which may be empty if none are recorded.
    Names only: no prices or materials. For one named weave use get_weave_details or get_weave_price.
    """
    hits = [n for n, w in WEAVES.items() if region.strip().lower() == w["region"].lower()]
    return {"weaves": hits}


@mcp.tool()
def get_weave_details(weave: str) -> dict:
    """Get the region and material of ONE named weave, such as 'jamdani'.

    Not for prices (use get_weave_price) and not for finding weaves by place (use list_weaves_by_region).
    """
    w = WEAVES.get(weave.strip().lower())
    if not w:
        raise ToolError(json.dumps({"category": "validation", "isRetryable": True,
                                     "message": f"No weave named {weave!r}. Known weaves: {sorted(WEAVES)}"}))
    return {"weave": weave, "region": w["region"], "material": w["material"]}


@mcp.tool()
def get_weave_price(weave: str) -> dict:
    """Get the typical price range in INR for ONE named weave, such as 'jamdani'. Use only for price questions."""
    w = WEAVES.get(weave.strip().lower())
    if not w:
        raise ToolError(json.dumps({"category": "validation", "isRetryable": True,
                                     "message": f"No weave named {weave!r}. Known weaves: {sorted(WEAVES)}"}))
    return {"weave": weave, "price_inr": w["price_inr"]}


@mcp.resource("weaves://catalog")
def catalog() -> str:
    """A catalogue of every weave we know, with its region. A resource: something to read, not a tool to call."""
    return json.dumps({n: w["region"] for n, w in WEAVES.items()}, indent=2)


if __name__ == "__main__":
    mcp.run()  # stdio transport by default
