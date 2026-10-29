"""Day 1 hands-on: watch the agentic loop from the inside.

Same loop as agent.py, but it prints the whole conversation after every call,
so you can see exactly what is sent and received. Run it, then read the output.
"""
import json
from agent import client, MODEL, TOOLS, TOOL_FUNCS


def show(messages):
    """Print the conversation in a short, readable form."""
    for m in messages:
        if isinstance(m["content"], str):
            print(f"    {m['role']:9} text: {m['content']}")
            continue
        for b in m["content"]:
            kind = b["type"] if isinstance(b, dict) else b.type
            if kind == "text":
                text = b["text"] if isinstance(b, dict) else b.text
                print(f"    {m['role']:9} text: {text}")
            elif kind == "tool_use":
                print(f"    {m['role']:9} tool_use: {b.name}({b.input})  id={b.id[-6:]}")
            elif kind == "tool_result":
                print(f"    {m['role']:9} tool_result: {b['content']}  for id={b['tool_use_id'][-6:]}")


def verbose_loop(question, max_tokens=1000):
    messages = [{"role": "user", "content": question}]
    call = 0
    while True:
        call += 1
        response = client.messages.create(model=MODEL, max_tokens=max_tokens, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        print(f"\n--- API call {call} returned. stop_reason = {response.stop_reason} ---")
        show(messages)
        if response.stop_reason != "tool_use":
            return
        results = []
        for b in response.content:
            if b.type == "tool_use":
                out = TOOL_FUNCS[b.name](**b.input)
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": json.dumps(out)})
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    print("=== EXPERIMENT A: a question that needs no tool ===")
    verbose_loop("What is 2 + 2?")
    print("\n\n=== EXPERIMENT B: a question that needs two tools, one after the other ===")
    verbose_loop("Which weaves come from West Bengal, and what is the price range of the one you find?")
    print("\n\n=== EXPERIMENT C: the same question, but Claude is only allowed 5 tokens of reply ===")
    verbose_loop("Which weaves come from West Bengal, and what is the price range of the one you find?", max_tokens=5)
