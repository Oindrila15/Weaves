"""Day 2, lesson 4: talk to the Weaves MCP server, then let Claude use its tools.

Step 1-4 show what an MCP client sees. Step 5 runs the same agent loop as Day 1,
but the tool list and the tool calls both come from the MCP server.
"""
# asyncio runs "async" code (code that waits for replies); json formats data; sys finds this Python.
import asyncio, json, sys
# Path helps build the file path to the server.
from pathlib import Path
# Helper that reads the secret key from the .env file.
from dotenv import load_dotenv
# Anthropic's tool for talking to Claude.
import anthropic
# The MCP library's client classes.
from mcp import ClientSession, StdioServerParameters
# The function that starts a server as a subprocess and connects over stdio.
from mcp.client.stdio import stdio_client

# Read the key from the .env file.
load_dotenv()
# Create the connection to Claude.
client = anthropic.Anthropic()
# The small, cheap model.
MODEL = "claude-haiku-5-5"
# The path to the server file, sitting next to this file.
SERVER = str(Path(__file__).with_name("weaves_mcp_server.py"))


# The main function. "async" means it can wait for replies without freezing.
async def main():
    # How to start the server: run it with this same Python.
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    # Start the server and get the two pipes to talk to it (read and write).
    async with stdio_client(params) as (read, write):
        # Open an MCP session over those pipes.
        async with ClientSession(read, write) as session:
            # The handshake: say hello and agree on the protocol.
            await session.initialize()

            # Step 1 heading.
            print("STEP 1. What tools does the server offer? (names and descriptions come from the code)")
            # Ask the server for its tool list.
            tools = (await session.list_tools()).tools
            # Print each tool's name and the first line of its description.
            for t in tools:
                # One line per tool.
                print(f"   - {t.name}: {t.description.splitlines()[0]}")
            # Print the input shape of the price tool (built from the type hints in the server).
            print("   input schema of get_weave_price:", json.dumps(tools[2].input_schema))

            # Step 2 heading.
            print("\nSTEP 2. Call a tool by hand")
            # Call the price tool for jamdani.
            r = await session.call_tool("get_weave_price", {"weave": "jamdani"})
            # Print whether it was an error and what came back.
            print("   isError =", r.is_error, "| content =", r.content[0].text)

            # Step 3 heading.
            print("\nSTEP 3. Call it with a bad input")
            # Call the price tool with a weave that does not exist.
            r = await session.call_tool("get_weave_price", {"weave": "nonsense"})
            # Print the error flag and the structured message.
            print("   isError =", r.is_error, "| content =", r.content[0].text)

            # Step 4 heading.
            print("\nSTEP 4. Read a resource (a catalogue, not a tool)")
            # Ask the server which resources it offers.
            for res in (await session.list_resources()).resources:
                # Print each resource's address.
                print("   resource:", res.uri)
            # Read the catalogue resource.
            cat = await session.read_resource("weaves://catalog")
            # Print its contents on one line.
            print("   contents:", cat.contents[0].text.replace("\n", " "))

            # Step 5 heading.
            print("\nSTEP 5. Claude uses the MCP tools through our loop")
            # Convert the server's tools into the shape Claude's API expects.
            tool_defs = [{"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in tools]
            # Start the conversation with the two-step question.
            messages = [{"role": "user", "content": "Which weaves come from West Bengal, and what is the price range of the one you find?"}]
            # The same loop as Day 1.
            while True:
                # One API call, offering the tools that came from the MCP server.
                resp = client.messages.create(model=MODEL, max_tokens=800, tools=tool_defs, messages=messages)
                # Add Claude's reply to the conversation.
                messages.append({"role": "assistant", "content": resp.content})
                # Show why Claude stopped.
                print(f"   [stop_reason = {resp.stop_reason}]")
                # If Claude is not asking for a tool, print its answer and stop.
                if resp.stop_reason != "tool_use":
                    # Join the text pieces and print them.
                    print("   answer:", "".join(b.text for b in resp.content if b.type == "text"))
                    # Leave the loop.
                    break
                # Start an empty list for the tool results.
                results = []
                # Look at each piece of Claude's reply.
                for b in resp.content:
                    # Only tool requests need action.
                    if b.type == "tool_use":
                        # Send the call to the MCP server, which runs the real function.
                        out = await session.call_tool(b.name, b.input)     # <- the call goes to the MCP server
                        # Take the text of the result.
                        text = out.content[0].text
                        # Print which tool was called and what came back.
                        print(f"   tool call via MCP: {b.name}({b.input}) -> {text}")
                        # Package the result for Claude, carrying the server's error flag.
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": text, "is_error": bool(out.is_error)})
                # Add the results to the conversation as a "user" message.
                messages.append({"role": "user", "content": results})


# Run the main function.
asyncio.run(main())

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; Claude's wording changes each time)
# STEP 1. What tools does the server offer? (names and descriptions come from the code)
#    - list_weaves_by_region: List the NAMES of handloom weaves traditionally made in one Indian state.
#    - get_weave_details: Get the region and material of ONE named weave, such as 'jamdani'.
#    - get_weave_price: Get the typical price range in INR for ONE named weave, such as 'jamdani'. Use only for price questions.
#    input schema of get_weave_price: {"properties": {"weave": {"title": "Weave", "type": "string"}}, "required": ["weave"], "type": "object", "title": "get_weave_priceArguments"}
#
# STEP 2. Call a tool by hand
#    isError = False | content = { "weave": "jamdani", "price_inr": [3000, 40000] }   (printed over several lines)
#
# STEP 3. Call it with a bad input
# Tool 'get_weave_price' failed: 'Error executing tool get_weave_price: {"category": "validation", "isRetryable": true, ...}'   (the server's own log line, on stderr)
#    isError = True | content = Error executing tool get_weave_price: {"category": "validation", "isRetryable": true, "message": "No weave named 'nonsense'. Known weaves: ['banarasi', 'chanderi', 'jamdani', 'kanchipuram']"}
#
# STEP 4. Read a resource (a catalogue, not a tool)
#    resource: weaves://catalog
#    contents: {   "kanchipuram": "Tamil Nadu",   "banarasi": "Uttar Pradesh",   "jamdani": "West Bengal",   "chanderi": "Madhya Pradesh" }
#
# STEP 5. Claude uses the MCP tools through our loop
#    [stop_reason = tool_use]
#    tool call via MCP: list_weaves_by_region({'region': 'West Bengal'}) -> {"weaves": ["jamdani"]}
#    [stop_reason = tool_use]
#    tool call via MCP: get_weave_price({'weave': 'jamdani'}) -> {"weave": "jamdani", "price_inr": [3000, 40000]}
#    [stop_reason = end_turn]
#    answer: The only weave recorded for West Bengal is **jamdani**. Its typical price range is **₹3,000 to ₹40,000**.
#
# How to read it: Steps 1 to 4 show what a client can see without Claude. The names and descriptions in step 1 are the server's docstrings.
# Step 3 shows ToolError working: the structured message (category, retry flag, hint) arrives intact. Step 5 is the same loop as Day 1,
# except the tool list and every tool call come from the MCP server.
