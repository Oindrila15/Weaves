"""Day 1 hands-on: watch the agentic loop from the inside.

Same loop as agent.py, but it prints the whole conversation after every call,
so you can see exactly what is sent and received. Run it, then read the output.
"""
# Tool for turning Python data into JSON text.
import json
# Reuse the connection, model, tool list and tool functions from agent.py (no need to write them again).
from agent import client, MODEL, TOOLS, TOOL_FUNCS


# A helper that prints the conversation in a short, readable form.
def show(messages):
    """Print the conversation in a short, readable form."""
    # Go through every message in the conversation.
    for m in messages:
        # If the message content is plain text (a string)...
        if isinstance(m["content"], str):
            # ...print the speaker's role and the text.
            print(f"    {m['role']:9} text: {m['content']}")
            # Move on to the next message.
            continue
        # Otherwise the content is a list of blocks; go through each block.
        for b in m["content"]:
            # Find the kind of block (blocks are either dictionaries or objects, so handle both).
            kind = b["type"] if isinstance(b, dict) else b.type
            # A text block: someone speaking.
            if kind == "text":
                # Get the text from the block.
                text = b["text"] if isinstance(b, dict) else b.text
                # Print the role and the text.
                print(f"    {m['role']:9} text: {text}")
            # A tool request from Claude.
            elif kind == "tool_use":
                # Print the tool name, its input, and the last 6 characters of its id.
                print(f"    {m['role']:9} tool_use: {b.name}({b.input})  id={b.id[-6:]}")
            # A tool result sent back by the program.
            elif kind == "tool_result":
                # Print the result and the id of the request it answers.
                print(f"    {m['role']:9} tool_result: {b['content']}  for id={b['tool_use_id'][-6:]}")


# The same loop as agent.py, but it prints everything after every call.
def verbose_loop(question, max_tokens=1000):
    # Start the conversation with the user's question.
    messages = [{"role": "user", "content": question}]
    # Count the API calls so we can label them.
    call = 0
    # Keep looping until Claude stops asking for tools.
    while True:
        # Add one to the call counter.
        call += 1
        # One API call: send the whole conversation and the tool list.
        response = client.messages.create(model=MODEL, max_tokens=max_tokens, tools=TOOLS, messages=messages)
        # Add Claude's reply to the conversation.
        messages.append({"role": "assistant", "content": response.content})
        # Print a heading: which call this was and why Claude stopped.
        print(f"\n--- API call {call} returned. stop_reason = {response.stop_reason} ---")
        # Print the whole conversation so far.
        show(messages)
        # If Claude is not asking for a tool, the loop ends.
        if response.stop_reason != "tool_use":
            # Leave the function.
            return
        # Start an empty list for the tool results.
        results = []
        # Look at each piece of Claude's reply.
        for b in response.content:
            # Only tool requests need action.
            if b.type == "tool_use":
                # Run the real Python function.
                out = TOOL_FUNCS[b.name](**b.input)
                # Package the result with the request's id.
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(out)})
        # Add the results to the conversation as a "user" message.
        messages.append({"role": "user", "content": results})


# Run this part only when the file is run directly.
if __name__ == "__main__":
    # Experiment A: a question that needs no tool.
    print("=== EXPERIMENT A: a question that needs no tool ===")
    # Run it: expect one call that ends with end_turn.
    verbose_loop("What is 2 + 2?")
    # Experiment B: a question that needs two tools in a row.
    print("\n\n=== EXPERIMENT B: a question that needs two tools, one after the other ===")
    # Run it: expect three calls.
    verbose_loop("Which weaves come from West Bengal, and what is the price range of the one you find?")
    # Experiment C: the same question, but the reply is cut off after 5 tokens.
    print("\n\n=== EXPERIMENT C: the same question, but Claude is only allowed 5 tokens of reply ===")
    # Run it: expect stop_reason max_tokens, which is NOT a finished answer.
    verbose_loop("Which weaves come from West Bengal, and what is the price range of the one you find?", max_tokens=5)

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; the ids and wording change each run)
# === EXPERIMENT A: a question that needs no tool ===
#
# --- API call 1 returned. stop_reason = end_turn ---
#     user      text: What is 2 + 2?
#     assistant text: 2 + 2 = 4.
#
#
# === EXPERIMENT B: a question that needs two tools, one after the other ===
#
# --- API call 1 returned. stop_reason = tool_use ---
#     user      text: Which weaves come from West Bengal, and what is the price range of the one you find?
#     assistant tool_use: search_weaves_by_region({'region': 'West Bengal'})  id=TsAiRM
#
# --- API call 2 returned. stop_reason = tool_use ---
#     user      text: Which weaves come from West Bengal, and what is the price range of the one you find?
#     assistant tool_use: search_weaves_by_region({'region': 'West Bengal'})  id=TsAiRM
#     user      tool_result: {"weaves": ["jamdani"]}  for id=TsAiRM
#     assistant tool_use: get_price_range({'weave': 'jamdani'})  id=mnXMzt
#
# --- API call 3 returned. stop_reason = end_turn ---
#     user      text: Which weaves come from West Bengal, and what is the price range of the one you find?
#     assistant tool_use: search_weaves_by_region({'region': 'West Bengal'})  id=TsAiRM
#     user      tool_result: {"weaves": ["jamdani"]}  for id=TsAiRM
#     assistant tool_use: get_price_range({'weave': 'jamdani'})  id=mnXMzt
#     user      tool_result: {"weave": "jamdani", "price_inr": [3000, 40000]}  for id=mnXMzt
#     assistant text: Only one weave is listed for West Bengal: **Jamdani**. Its typical price range is **₹3,000 to ₹40,000**.
#
#
# === EXPERIMENT C: the same question, but Claude is only allowed 5 tokens of reply ===
#
# --- API call 1 returned. stop_reason = max_tokens ---
#     user      text: Which weaves come from West Bengal, and what is the price range of the one you find?
#
# How to read it: each "API call" block shows the whole conversation so far. Notice the conversation GROWS
# with every call, because the full list is resent each time (the API remembers nothing).
# In B, each tool_result is paired with its tool_use by the same id.
# In C, Claude ran out of room (max_tokens) before saying anything, so no answer: stop_reason tells you.
