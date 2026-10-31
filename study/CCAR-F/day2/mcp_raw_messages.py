"""Day 2, lesson 4 (deep dive): see the raw MCP messages, with no MCP library on the client side.

MCP over stdio is just lines of JSON sent to the server's standard input, and
lines of JSON read back from its standard output. We type them ourselves.
"""
import json, subprocess, sys
from pathlib import Path

SERVER = str(Path(__file__).with_name("weaves_mcp_server.py"))
proc = subprocess.Popen([sys.executable, SERVER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, text=True)


def send(msg, expect_reply=True):
    print(f"\n>>> CLIENT SENDS:\n{json.dumps(msg, indent=1)}")
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    if expect_reply:
        reply = json.loads(proc.stdout.readline())
        text = json.dumps(reply, indent=1)
        print(f"<<< SERVER REPLIES:\n{text[:1400]}{' ...(cut)' if len(text) > 1400 else ''}")
        return reply


# 1. Handshake: say hello, agree on a protocol version, swap capabilities.
send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                 "clientInfo": {"name": "hand-typed-client", "version": "0"}}})
send({"jsonrpc": "2.0", "method": "notifications/initialized"}, expect_reply=False)   # a notice: no reply

# 2. Discovery: what do you offer?
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})

# 3. A tool call that works, and one that fails.
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
      "params": {"name": "get_weave_price", "arguments": {"weave": "jamdani"}}})
send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
      "params": {"name": "get_weave_price", "arguments": {"weave": "nonsense"}}})

# 4. A resource.
send({"jsonrpc": "2.0", "id": 5, "method": "resources/read", "params": {"uri": "weaves://catalog"}})

proc.stdin.close()
proc.wait(timeout=5)
