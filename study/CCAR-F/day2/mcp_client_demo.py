"""Day 2, lesson 4: talk to the Weaves MCP server, then let Claude use its tools.

Step 1-4 show what an MCP client sees. Step 5 runs the same agent loop as Day 1,
but the tool list and the tool calls both come from the MCP server.
"""
import asyncio, json, sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
SERVER = str(Path(__file__).with_name("weaves_mcp_server.py"))


async def main():
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("STEP 1. What tools does the server offer? (names and descriptions come from the code)")
            tools = (await session.list_tools()).tools
            for t in tools:
                print(f"   - {t.name}: {t.description.splitlines()[0]}")
            print("   input schema of get_weave_price:", json.dumps(tools[2].input_schema))

            print("\nSTEP 2. Call a tool by hand")
            r = await session.call_tool("get_weave_price", {"weave": "jamdani"})
            print("   isError =", r.is_error, "| content =", r.content[0].text)

            print("\nSTEP 3. Call it with a bad input")
            r = await session.call_tool("get_weave_price", {"weave": "nonsense"})
            print("   isError =", r.is_error, "| content =", r.content[0].text)

            print("\nSTEP 4. Read a resource (a catalogue, not a tool)")
            for res in (await session.list_resources()).resources:
                print("   resource:", res.uri)
            cat = await session.read_resource("weaves://catalog")
            print("   contents:", cat.contents[0].text.replace("\n", " "))

            print("\nSTEP 5. Claude uses the MCP tools through our loop")
            tool_defs = [{"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in tools]
            messages = [{"role": "user", "content": "Which weaves come from West Bengal, and what is the price range of the one you find?"}]
            while True:
                resp = client.messages.create(model=MODEL, max_tokens=800, tools=tool_defs, messages=messages)
                messages.append({"role": "assistant", "content": resp.content})
                print(f"   [stop_reason = {resp.stop_reason}]")
                if resp.stop_reason != "tool_use":
                    print("   answer:", "".join(b.text for b in resp.content if b.type == "text"))
                    break
                results = []
                for b in resp.content:
                    if b.type == "tool_use":
                        out = await session.call_tool(b.name, b.input)     # <- the call goes to the MCP server
                        text = out.content[0].text
                        print(f"   tool call via MCP: {b.name}({b.input}) -> {text}")
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": text, "is_error": bool(out.is_error)})
                messages.append({"role": "user", "content": results})


asyncio.run(main())
