"""Day 2, lesson 2: how a tool reports problems changes what Claude does (exam topic 2.2).

One tool, one question, five ways the tool can behave when something goes wrong.
The loop still follows stop_reason. A round cap of 6 is only a safety limit.
"""
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"

TOOL = {
    "name": "get_weaves_by_region",
    "description": ("List the names of handloom weaves traditionally made in one Indian state. "
                    "Input: the full state name, such as 'Tamil Nadu'. Returns a list of weave names."),
    "input_schema": {"type": "object", "properties": {"region": {"type": "string"}}, "required": ["region"]},
}


def run(question, tool_impl, safety_cap=6):
    """tool_impl(region, call_number) returns (content_dict_or_str, is_error)."""
    messages = [{"role": "user", "content": question}]
    calls = 0
    for _ in range(safety_cap):
        r = client.messages.create(model=MODEL, max_tokens=500, tools=[TOOL], messages=messages)
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason != "tool_use":
            return calls, "".join(b.text for b in r.content if b.type == "text")
        results = []
        for b in r.content:
            if b.type == "tool_use":
                calls += 1
                content, is_err = tool_impl(b.input.get("region", ""), calls)
                shown = content if isinstance(content, str) else json.dumps(content)
                print(f"    tool call {calls}: region={b.input.get('region')!r} -> {'ERROR ' if is_err else ''}{shown}")
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": shown, "is_error": is_err})
        messages.append({"role": "user", "content": results})
    return calls, "(hit the safety cap of 6 rounds)"


def swallowed(region, n):          # the database is down, but the tool hides it as "no results"
    return {"weaves": []}, False

def vague_error(region, n):        # an error, but no detail
    return "Error", True

def transient(region, n):          # fails once, then works
    if n == 1:
        return {"isError": True, "category": "transient", "isRetryable": True,
                "message": "The weave database timed out. Safe to try again."}, True
    return {"weaves": ["kanchipuram"]}, False

def permission(region, n):         # will never work for this user
    return {"isError": True, "category": "permission", "isRetryable": False,
            "message": "This account may not read this data source. Retrying will not help."}, True

def validation(region, n):         # bad input, with a hint that lets Claude fix it
    if region.lower() != "tamil nadu":
        return {"isError": True, "category": "validation", "isRetryable": True,
                "message": f"Region {region!r} is not recognised. Use the full state name, for example 'Tamil Nadu'."}, True
    return {"weaves": ["kanchipuram"]}, False


CASES = [
    ("1. FAILURE HIDDEN AS AN EMPTY RESULT", "Which weaves come from Tamil Nadu?", swallowed),
    ("2. VAGUE ERROR ('Error')", "Which weaves come from Tamil Nadu?", vague_error),
    ("3. STRUCTURED, transient + retryable", "Which weaves come from Tamil Nadu?", transient),
    ("4. STRUCTURED, permission + NOT retryable", "Which weaves come from Tamil Nadu?", permission),
    ("5. STRUCTURED, validation with a hint", "Which weaves come from TN?", validation),
]

if __name__ == "__main__":
    for title, q, impl in CASES:
        print(f"\n=== {title}\n  Q: {q}")
        calls, answer = run(q, impl)
        print(f"  tool calls: {calls}\n  Claude's answer: {answer}")
