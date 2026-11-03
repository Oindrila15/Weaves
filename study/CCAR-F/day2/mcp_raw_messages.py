"""Day 2, lesson 4 (deep dive): see the raw MCP messages, with no MCP library on the client side.

MCP over stdio is just lines of JSON sent to the server's standard input, and
lines of JSON read back from its standard output. We type them ourselves.
"""
# json formats messages; subprocess starts the server; sys finds this Python.
import json, subprocess, sys
# Path helps build the file path to the server.
from pathlib import Path

# The path to the server file, sitting next to this file.
SERVER = str(Path(__file__).with_name("weaves_mcp_server.py"))
# Start the server as a separate program, with pipes for what we send (stdin) and what it replies (stdout).
proc = subprocess.Popen([sys.executable, SERVER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        # Throw away the server's own log messages (stderr) so they do not clutter the output.
                        stderr=subprocess.DEVNULL, text=True)


# A helper that sends one message and (usually) prints the reply.
def send(msg, expect_reply=True):
    # Print what we are about to send, formatted nicely.
    print(f"\n>>> CLIENT SENDS:\n{json.dumps(msg, indent=1)}")
    # Write the message as one line of JSON to the server's input.
    proc.stdin.write(json.dumps(msg) + "\n")
    # Push it through the pipe immediately.
    proc.stdin.flush()
    # Some messages (notifications) get no reply.
    if expect_reply:
        # Read one line from the server's output and turn it back into data.
        reply = json.loads(proc.stdout.readline())
        # Format the reply nicely.
        text = json.dumps(reply, indent=1)
        # Print it, cutting very long replies at 1400 characters.
        print(f"<<< SERVER REPLIES:\n{text[:1400]}{' ...(cut)' if len(text) > 1400 else ''}")
        # Hand the reply back to the caller.
        return reply


# 1. Handshake: say hello, agree on a protocol version, swap capabilities.
# Message 1: "initialize" with id 1. The reply will carry the same id.
send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      # The protocol version we speak, what we can do, and who we are.
      "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                 # A name for our hand-typed client.
                 "clientInfo": {"name": "hand-typed-client", "version": "0"}}})
# A notification ("I'm ready"): it has no id, so the server sends no reply.
send({"jsonrpc": "2.0", "method": "notifications/initialized"}, expect_reply=False)   # a notice: no reply

# 2. Discovery: what do you offer?
# Message 2: ask for the list of tools (id 2).
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})

# 3. A tool call that works, and one that fails.
# Message 3: call the price tool for jamdani (id 3).
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
      # Which tool, and its input.
      "params": {"name": "get_weave_price", "arguments": {"weave": "jamdani"}}})
# Message 4: call the same tool with a bad input (id 4).
send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
      # Which tool, and its input.
      "params": {"name": "get_weave_price", "arguments": {"weave": "nonsense"}}})

# 4. A resource.
# Message 5: read the catalogue resource (id 5).
send({"jsonrpc": "2.0", "id": 5, "method": "resources/read", "params": {"uri": "weaves://catalog"}})

# Close the server's input, which tells it we are finished.
proc.stdin.close()
# Wait up to 5 seconds for the server to shut down.
proc.wait(timeout=5)

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; shortened where marked)
# >>> CLIENT SENDS: {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", ...}}
# <<< SERVER REPLIES: {"jsonrpc": "2.0", "id": 1, "result": {"capabilities": {"prompts": {...}, "resources": {...}, "tools": {...}},
#                      "protocolVersion": "2025-06-18", "serverInfo": {"name": "weaves", "version": ""}}}
#
# >>> CLIENT SENDS: {"jsonrpc": "2.0", "method": "notifications/initialized"}      (no id, and no reply)
#
# >>> CLIENT SENDS: {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
# <<< SERVER REPLIES: {"jsonrpc": "2.0", "id": 2, "result": {"tools": [ {"name": "list_weaves_by_region", "description": "...", "inputSchema": {...}}, ... ]}}   (cut)
#
# >>> CLIENT SENDS: {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_weave_price", "arguments": {"weave": "jamdani"}}}
# <<< SERVER REPLIES: {"jsonrpc": "2.0", "id": 3, "result": {"content": [{"text": "{ \"weave\": \"jamdani\", \"price_inr\": [3000, 40000] }", "type": "text"}], "isError": false}}
#
# >>> CLIENT SENDS: {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_weave_price", "arguments": {"weave": "nonsense"}}}
# <<< SERVER REPLIES: {"jsonrpc": "2.0", "id": 4, "result": {"content": [{"text": "Error executing tool get_weave_price: {\"category\": \"validation\", \"isRetryable\": true, \"message\": \"No weave named 'nonsense'. Known weaves: ['banarasi', 'chanderi', 'jamdani', 'kanchipuram']\"}", "type": "text"}], "isError": true}}
#
# >>> CLIENT SENDS: {"jsonrpc": "2.0", "id": 5, "method": "resources/read", "params": {"uri": "weaves://catalog"}}
# <<< SERVER REPLIES: {"jsonrpc": "2.0", "id": 5, "result": {"contents": [{"mimeType": "text/plain", "text": "{ \"kanchipuram\": \"Tamil Nadu\", ... }", "uri": "weaves://catalog"}]}}
#
# (The real output prints each message over many lines; here each is squeezed onto one line to save space.)
#
# How to read it: a message WITH an id is a request, and the reply carries the same id so we can match them. A message without an id is a notification:
# no reply. A failed tool is still a normal reply with "isError": true, not a protocol error. That is the difference between a tool execution error
# and a protocol error (for example, a malformed message).
