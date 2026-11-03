"""Day 2, lesson 4: a tiny MCP server over made-up saree data (exam topic 2.4).

Run by a client as a subprocess and spoken to over stdin/stdout (the 'stdio' transport).
It offers two kinds of things:
  - tools:     things Claude can DO (look up, calculate)
  - resources: things Claude (or the app) can READ, like a catalogue
All data below is sample data for learning, not real weaver facts.
"""
# Tool for turning Python data into JSON text.
import json
# The MCP library's server class.
from mcp.server.mcpserver import MCPServer
# The special error type that sends our message to the client (an ordinary error would lose it).
from mcp.server.mcpserver.exceptions import ToolError

# Create the server and give it the name "weaves".
mcp = MCPServer("weaves")

# The made-up catalogue (same as in agent.py).
WEAVES = {
    # Kanchipuram silk.
    "kanchipuram": {"region": "Tamil Nadu", "material": "pure mulberry silk, zari", "price_inr": [15000, 150000]},
    # Banarasi silk.
    "banarasi": {"region": "Uttar Pradesh", "material": "silk, brocade", "price_inr": [8000, 100000]},
    # Jamdani cotton.
    "jamdani": {"region": "West Bengal", "material": "fine cotton", "price_inr": [3000, 40000]},
    # Chanderi silk-cotton.
    "chanderi": {"region": "Madhya Pradesh", "material": "silk-cotton", "price_inr": [2500, 20000]},
# End of the catalogue.
}


# This line registers the function below as a tool that clients can discover and call.
@mcp.tool()
# Tool 1: weave names for a region. Its name, input (region: text) and docstring become what Claude reads.
def list_weaves_by_region(region: str) -> dict:
    """List the NAMES of handloom weaves traditionally made in one Indian state.

    Input: a state name such as 'Tamil Nadu' (capital letters do not matter).
    Returns a list of weave names, which may be empty if none are recorded.
    Names only: no prices or materials. For one named weave use get_weave_details or get_weave_price.
    """
    # Keep every weave whose region equals the input (ignoring spaces and capital letters).
    hits = [n for n, w in WEAVES.items() if region.strip().lower() == w["region"].lower()]
    # Return the matches.
    return {"weaves": hits}


# Register the next function as a tool.
@mcp.tool()
# Tool 2: region and material of one weave.
def get_weave_details(weave: str) -> dict:
    """Get the region and material of ONE named weave, such as 'jamdani'.

    Not for prices (use get_weave_price) and not for finding weaves by place (use list_weaves_by_region).
    """
    # Look the weave up by its lower-case name.
    w = WEAVES.get(weave.strip().lower())
    # If it is not in the catalogue...
    if not w:
        # ...raise a ToolError with a structured message, so Claude receives the category, the retry flag and a hint.
        raise ToolError(json.dumps({"category": "validation", "isRetryable": True,
                                     # The hint lists the weaves that do exist.
                                     "message": f"No weave named {weave!r}. Known weaves: {sorted(WEAVES)}"}))
    # Otherwise return the details.
    return {"weave": weave, "region": w["region"], "material": w["material"]}


# Register the next function as a tool.
@mcp.tool()
# Tool 3: price range of one weave.
def get_weave_price(weave: str) -> dict:
    """Get the typical price range in INR for ONE named weave, such as 'jamdani'. Use only for price questions."""
    # Look the weave up by its lower-case name.
    w = WEAVES.get(weave.strip().lower())
    # If it is not in the catalogue...
    if not w:
        # ...raise the same kind of structured ToolError.
        raise ToolError(json.dumps({"category": "validation", "isRetryable": True,
                                     # The hint lists the weaves that do exist.
                                     "message": f"No weave named {weave!r}. Known weaves: {sorted(WEAVES)}"}))
    # Otherwise return the price range.
    return {"weave": weave, "price_inr": w["price_inr"]}


# Register the next function as a resource, with the address weaves://catalog.
@mcp.resource("weaves://catalog")
# A resource: something to READ (the host decides to use it), not a tool Claude calls.
def catalog() -> str:
    """A catalogue of every weave we know, with its region. A resource: something to read, not a tool to call."""
    # Return a short JSON list of weave -> region, with indentation for readability.
    return json.dumps({n: w["region"] for n, w in WEAVES.items()}, indent=2)


# Run this part only when the file is started directly (the client starts it this way).
if __name__ == "__main__":
    # Start the server and listen on standard input and output (the stdio transport).
    mcp.run()  # stdio transport by default

# ---------------------------------------------------------------------------
# OUTPUT: running this file by itself prints nothing. It waits for a client to send it messages.
# Its behaviour is shown by the two programs that talk to it: mcp_client_demo.py and mcp_raw_messages.py.
# Important: in this kind of server, standard output is reserved for the protocol messages.
# If you print() anything to it, you corrupt the messages. Use stderr or logging for your own notes.
