"""Day 1: the same agent, with hooks (exam topics 1.4 and 1.5).

A hook is a function our loop calls at a fixed point:
  - pre_tool_hook runs BEFORE a tool and can block the call.
  - post_tool_hook runs AFTER a tool, before Claude sees the result.
Rules that must always hold live here, in code, not in the prompt.
"""
import json
from agent import client, MODEL, TOOLS, TOOL_FUNCS, WEAVERS


def pre_tool_hook(name, args):
    """Return None to allow the call, or a dict explaining why it is blocked."""
    if name == "get_weaver_contact":
        weaver = WEAVERS.get(args.get("weaver_id"))
        if weaver is not None and not weaver["consent"]:
            return {
                "blocked": True,
                "category": "policy",
                "isRetryable": False,
                "message": ("Contact details are shown only with the weaver's consent, "
                            "and this weaver has not given it. Do not try again. "
                            "Tell the user you cannot share it, and offer other public information."),
            }
    return None


def post_tool_hook(name, output):
    """Clean a tool result before Claude sees it: show prices as one readable line."""
    if isinstance(output, dict) and "price_inr" in output:
        low, high = output["price_inr"]
        output = {k: v for k, v in output.items() if k != "price_inr"}
        output["price_text"] = f"INR {low:,} to {high:,}"
    return output


def run_agent(question):
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(model=MODEL, max_tokens=1000, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        print(f"[stop_reason = {response.stop_reason}]")

        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text")

        if response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"  tool call: {block.name}({block.input})")
                blocked = pre_tool_hook(block.name, block.input)          # hook BEFORE
                if blocked:
                    print(f"  [pre hook] BLOCKED: {blocked['message'][:60]}...")
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    "content": json.dumps(blocked), "is_error": True})
                    continue
                output = TOOL_FUNCS[block.name](**block.input)
                cleaned = post_tool_hook(block.name, output)              # hook AFTER
                if cleaned != output:
                    print(f"  [post hook] cleaned result: {cleaned}")
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(cleaned)})
            messages.append({"role": "user", "content": results})
            continue

        raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")


if __name__ == "__main__":
    for q in ["What is the phone number of weaver w2?",
              "What is the phone number of weaver w1?",
              "How much does a banarasi saree cost?"]:
        print(f"\n=== {q}")
        print(run_agent(q))
