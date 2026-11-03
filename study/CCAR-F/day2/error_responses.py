"""Day 2, lesson 2: how a tool reports problems changes what Claude does (exam topic 2.2).

One tool, one question, five ways the tool can behave when something goes wrong.
The loop still follows stop_reason. A round cap of 6 is only a safety limit.
"""
# Tool for turning Python data into JSON text.
import json
# Helper that reads the secret key from the .env file.
from dotenv import load_dotenv
# Anthropic's tool for talking to Claude.
import anthropic

# Read the key from the .env file.
load_dotenv()
# Create the connection to Claude.
client = anthropic.Anthropic()
# The small, cheap model.
MODEL = "claude-haiku-5-5"

# The one tool Claude can use in every case.
TOOL = {
    # Its name.
    "name": "get_weaves_by_region",
    # Its description for Claude: purpose, input and output.
    "description": ("List the names of handloom weaves traditionally made in one Indian state. "
                    # What to pass in, and what comes back.
                    "Input: the full state name, such as 'Tamil Nadu'. Returns a list of weave names."),
    # The input shape: one required text field called region.
    "input_schema": {"type": "object", "properties": {"region": {"type": "string"}}, "required": ["region"]},
# End of the tool definition.
}


# Run the agent loop for one question, using a pretend tool that behaves however we choose.
def run(question, tool_impl, safety_cap=6):
    """tool_impl(region, call_number) returns (content_dict_or_str, is_error)."""
    # Start the conversation with the question.
    messages = [{"role": "user", "content": question}]
    # Count how many tool calls Claude makes.
    calls = 0
    # Go round at most 6 times, as a safety limit.
    for _ in range(safety_cap):
        # One API call.
        r = client.messages.create(model=MODEL, max_tokens=500, tools=[TOOL], messages=messages)
        # Add Claude's reply to the conversation.
        messages.append({"role": "assistant", "content": r.content})
        # If Claude is not asking for a tool, it is done: return the count and its answer.
        if r.stop_reason != "tool_use":
            # Join Claude's text pieces into the answer.
            return calls, "".join(b.text for b in r.content if b.type == "text")
        # Start an empty list for the tool results.
        results = []
        # Look at each piece of Claude's reply.
        for b in r.content:
            # Only tool requests need action.
            if b.type == "tool_use":
                # Count this call.
                calls += 1
                # Run the pretend tool with Claude's input.
                content, is_err = tool_impl(b.input.get("region", ""), calls)
                # Turn the result into text if it is not already.
                shown = content if isinstance(content, str) else json.dumps(content)
                # Print what was asked and what came back (marking errors).
                print(f"    tool call {calls}: region={b.input.get('region')!r} -> {'ERROR ' if is_err else ''}{shown}")
                # Package the result, flagging whether it is an error.
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": shown, "is_error": is_err})
        # Add the results to the conversation as a "user" message.
        messages.append({"role": "user", "content": results})
    # If we get here, we hit the safety cap.
    return calls, "(hit the safety cap of 6 rounds)"


# Case 1: the database is down, but the tool pretends everything is fine and returns nothing.
def swallowed(region, n):          # the database is down, but the tool hides it as "no results"
    # An empty list, not flagged as an error.
    return {"weaves": []}, False

# Case 2: an error with no detail at all.
def vague_error(region, n):        # an error, but no detail
    # Just the word "Error", flagged as an error.
    return "Error", True

# Case 3: fails on the first call, then works.
def transient(region, n):          # fails once, then works
    # On the first call only...
    if n == 1:
        # ...return a structured error that says it is temporary and safe to retry.
        return {"isError": True, "category": "transient", "isRetryable": True,
                # A message that tells Claude what to do.
                "message": "The weave database timed out. Safe to try again."}, True
    # On later calls, return a normal result.
    return {"weaves": ["kanchipuram"]}, False

# Case 4: the user is simply not allowed, and always will be.
def permission(region, n):         # will never work for this user
    # A structured error that says retrying will not help.
    return {"isError": True, "category": "permission", "isRetryable": False,
            # A message that tells Claude not to retry.
            "message": "This account may not read this data source. Retrying will not help."}, True

# Case 5: the input was badly written, and the error says how to fix it.
def validation(region, n):         # bad input, with a hint that lets Claude fix it
    # If the region is not the full state name...
    if region.lower() != "tamil nadu":
        # ...return an error that includes a hint with the right form.
        return {"isError": True, "category": "validation", "isRetryable": True,
                # The hint: use the full state name.
                "message": f"Region {region!r} is not recognised. Use the full state name, for example 'Tamil Nadu'."}, True
    # With the full name, return a normal result.
    return {"weaves": ["kanchipuram"]}, False


# The five cases: a title, the question to ask, and which pretend tool to use.
CASES = [
    # Case 1.
    ("1. FAILURE HIDDEN AS AN EMPTY RESULT", "Which weaves come from Tamil Nadu?", swallowed),
    # Case 2.
    ("2. VAGUE ERROR ('Error')", "Which weaves come from Tamil Nadu?", vague_error),
    # Case 3.
    ("3. STRUCTURED, transient + retryable", "Which weaves come from Tamil Nadu?", transient),
    # Case 4.
    ("4. STRUCTURED, permission + NOT retryable", "Which weaves come from Tamil Nadu?", permission),
    # Case 5 (note the question says "TN", the short form).
    ("5. STRUCTURED, validation with a hint", "Which weaves come from TN?", validation),
# End of the cases.
]

# Run this part only when the file is run directly.
if __name__ == "__main__":
    # Go through the five cases.
    for title, q, impl in CASES:
        # Print the case title and the question.
        print(f"\n=== {title}\n  Q: {q}")
        # Run the agent with this case's pretend tool.
        calls, answer = run(q, impl)
        # Print how many tool calls were made and Claude's final answer.
        print(f"  tool calls: {calls}\n  Claude's answer: {answer}")

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; Claude's wording is shortened here and changes each time)
# === 1. FAILURE HIDDEN AS AN EMPTY RESULT
#     tool call 1: region='Tamil Nadu' -> {"weaves": []}
#   tool calls: 1
#   Claude's answer: The tool returned no weaves, so its data may be incomplete. (Then it listed weaves from general knowledge, not from the tool.)
#
# === 2. VAGUE ERROR ('Error')
#     tool call 1: region='Tamil Nadu' -> ERROR Error
#     tool call 2: region='Tamil Nadu' -> ERROR Error
#   tool calls: 2
#   Claude's answer: I couldn't get the list. The lookup failed twice, so the service may be temporarily unavailable. (It guessed the cause.)
#
# === 3. STRUCTURED, transient + retryable
#     tool call 1: region='Tamil Nadu' -> ERROR {"isError": true, "category": "transient", "isRetryable": true, ...}
#     tool call 2: region='Tamil Nadu' -> {"weaves": ["kanchipuram"]}
#   tool calls: 2
#   Claude's answer: The only weave listed for Tamil Nadu is Kanchipuram.
#
# === 4. STRUCTURED, permission + NOT retryable
#     tool call 1: region='Tamil Nadu' -> ERROR {"isError": true, "category": "permission", "isRetryable": false, ...}
#   tool calls: 1
#   Claude's answer: I couldn't retrieve the list: a permission error, and retrying won't help. (Then general knowledge, labelled as not from the tool.)
#
# === 5. STRUCTURED, validation with a hint
#     tool call 1: region='Tamil Nadu' -> {"weaves": ["kanchipuram"]}
#   tool calls: 1
#   Claude's answer: Tamil Nadu has one traditional handloom weave in the database: Kanchipuram.
#
# How to read it: case 1 hid a failure as "no results", so Claude could not tell the difference. In case 2 the error said nothing, so Claude retried
# blindly and guessed the cause. In 3 the retryable flag let Claude retry once and succeed. In 4 the not-retryable flag stopped it after one call.
# In 5 the validation error never fired: Claude had already expanded "TN" to "Tamil Nadu" by itself, so there was nothing to fix.
