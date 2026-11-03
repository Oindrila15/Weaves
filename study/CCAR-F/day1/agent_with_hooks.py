"""Day 1: the same agent, with hooks (exam topics 1.4 and 1.5).

A hook is a function our loop calls at a fixed point:
  - pre_tool_hook runs BEFORE a tool and can block the call.
  - post_tool_hook runs AFTER a tool, before Claude sees the result.
Rules that must always hold live here, in code, not in the prompt.
"""
# Tool for turning Python data into JSON text.
import json
# Reuse the connection, model, tools and sample data from agent.py.
from agent import client, MODEL, TOOLS, TOOL_FUNCS, WEAVERS


# The "before" hook: runs before any tool and can stop it.
def pre_tool_hook(name, args):
    """Return None to allow the call, or a dict explaining why it is blocked."""
    # This rule only applies to the contact tool.
    if name == "get_weaver_contact":
        # Look up the weaver Claude asked about.
        weaver = WEAVERS.get(args.get("weaver_id"))
        # If the weaver exists but has NOT given consent...
        if weaver is not None and not weaver["consent"]:
            # ...block the call and return a structured error for Claude.
            return {
                # Marks this as an error.
                "isError": True,
                # The category: a business rule (consent), not a technical fault.
                "category": "business",
                # Retrying will not help, so Claude should not try again.
                "isRetryable": False,
                # A clear message that tells Claude what to do instead.
                "message": ("Contact details are shown only with the weaver's consent, "
                            # Explain that the weaver has not agreed.
                            "and this weaver has not given it. Retrying will not change that: "
                            # Explain when it could change.
                            "it becomes possible only if the weaver gives consent. "
                            # Tell Claude how to respond to the user.
                            "Tell the user you cannot share it, and offer other public information."),
            # End of the error dictionary.
            }
    # Nothing blocked: None means "go ahead".
    return None


# The "after" hook: tidies a tool result before Claude sees it.
def post_tool_hook(name, output):
    """Clean a tool result before Claude sees it: show prices as one readable line."""
    # Only act on results that contain a price range.
    if isinstance(output, dict) and "price_inr" in output:
        # Split the range [low, high] into two numbers.
        low, high = output["price_inr"]
        # Copy the result without the raw price field.
        output = {k: v for k, v in output.items() if k != "price_inr"}
        # Add a readable line such as "INR 8,000 to 100,000".
        output["price_text"] = f"INR {low:,} to {high:,}"
    # Return the (possibly cleaned) result.
    return output


# The same loop as agent.py, now with both hooks.
def run_agent(question):
    # Start the conversation with the user's question.
    messages = [{"role": "user", "content": question}]
    # Keep looping until Claude is done.
    while True:
        # One API call.
        response = client.messages.create(model=MODEL, max_tokens=1000, tools=TOOLS, messages=messages)
        # Add Claude's reply to the conversation.
        messages.append({"role": "assistant", "content": response.content})
        # Show why Claude stopped.
        print(f"[stop_reason = {response.stop_reason}]")

        # If Claude is finished, return its text.
        if response.stop_reason == "end_turn":
            # Join all text pieces and return them.
            return "".join(b.text for b in response.content if b.type == "text")

        # If Claude wants tools, run them (through the hooks).
        if response.stop_reason == "tool_use":
            # Start an empty list for the tool results.
            results = []
            # Look at each piece of Claude's reply.
            for block in response.content:
                # Skip anything that is not a tool request.
                if block.type != "tool_use":
                    # Go to the next piece.
                    continue
                # Show which tool Claude asked for.
                print(f"  tool call: {block.name}({block.input})")
                # Run the "before" hook. If it returns something, the call is blocked.
                blocked = pre_tool_hook(block.name, block.input)          # hook BEFORE
                # If it was blocked...
                if blocked:
                    # ...print the first 60 characters of the reason.
                    print(f"  [pre hook] BLOCKED: {blocked['message'][:60]}...")
                    # Send the block message back to Claude as an error result (the tool never ran).
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    # The structured error as JSON text, flagged as an error.
                                    "content": json.dumps(blocked), "is_error": True})
                    # Go to the next piece.
                    continue
                # Not blocked: run the real tool.
                output = TOOL_FUNCS[block.name](**block.input)
                # Run the "after" hook to tidy the result.
                cleaned = post_tool_hook(block.name, output)              # hook AFTER
                # If the hook changed anything, show it.
                if cleaned != output:
                    # Print the tidied result.
                    print(f"  [post hook] cleaned result: {cleaned}")
                # Package the tidied result for Claude.
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                # The result as JSON text.
                                "content": json.dumps(cleaned)})
            # Add the results to the conversation as a "user" message.
            messages.append({"role": "user", "content": results})
            # Go round the loop again.
            continue

        # Any other stop reason is unexpected, so stop with an error.
        raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")


# Run this part only when the file is run directly.
if __name__ == "__main__":
    # Three questions: a blocked weaver, an allowed weaver, and a price question.
    for q in ["What is the phone number of weaver w2?",
              # w1 gave consent, so this one is allowed.
              "What is the phone number of weaver w1?",
              # A price question, to see the "after" hook tidy the price.
              "How much does a banarasi saree cost?"]:
        # Print the question as a heading.
        print(f"\n=== {q}")
        # Run the agent and print its final answer.
        print(run_agent(q))

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; Claude's wording changes each time)
# === What is the phone number of weaver w2?
# [stop_reason = tool_use]
#   tool call: get_weaver_contact({'weaver_id': 'w2'})
#   [pre hook] BLOCKED: Contact details are shown only with the weaver's consent, an...
# [stop_reason = end_turn]
# I can't share the phone number for weaver w2. Their contact details are only released with the weaver's consent, and they haven't given it.
# (Claude then offered other public information.)
#
# === What is the phone number of weaver w1?
# [stop_reason = tool_use]
#   tool call: get_weaver_contact({'weaver_id': 'w1'})
# [stop_reason = end_turn]
# The phone number for weaver w1 (Sample Weaver A) is 000-000-0001.
#
# === How much does a banarasi saree cost?
# [stop_reason = tool_use]
#   tool call: get_price_range({'weave': 'Banarasi saree'})
# [stop_reason = tool_use]
#   tool call: get_price_range({'weave': 'Banarasi'})
#   [post hook] cleaned result: {'weave': 'Banarasi', 'price_text': 'INR 8,000 to 100,000'}
# [stop_reason = end_turn]
# A Banarasi saree typically costs between INR 8,000 and INR 1,00,000. ...
#
# How to read it: w2 has no consent, so the pre hook blocked the call BEFORE the tool ran, and the phone number never reached Claude.
# w1 has consent, so it went through. In the price question Claude first tried "Banarasi saree" (no match, so the tool returned an error),
# then corrected itself to "Banarasi". Only the successful result passed through the post hook (the cleaned price_text line).
