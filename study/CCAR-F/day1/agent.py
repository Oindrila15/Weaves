"""Day 1: a tool-using agent. The loop follows stop_reason (exam topic 1.1).

All data below is made-up sample data for learning, not real weaver facts.
"""
# Tool for turning Python data into JSON text (and back).
import json
# Helper that reads the secret key from the .env file.
from dotenv import load_dotenv
# Anthropic's tool for talking to Claude.
import anthropic

# Read the key from the .env file.
load_dotenv()
# Create the connection to Claude.
client = anthropic.Anthropic()
# The small, cheap model we use for all the experiments.
MODEL = "claude-haiku-5-5"

# --- Sample data -----------------------------------------------------------
# A made-up catalogue: each weave has a region, a material and a price range in rupees [low, high].
WEAVES = {
    # Kanchipuram silk, from Tamil Nadu.
    "kanchipuram": {"region": "Tamil Nadu", "material": "pure mulberry silk, zari", "price_inr": [15000, 150000]},
    # Banarasi silk, from Uttar Pradesh.
    "banarasi": {"region": "Uttar Pradesh", "material": "silk, brocade", "price_inr": [8000, 100000]},
    # Jamdani cotton, from West Bengal.
    "jamdani": {"region": "West Bengal", "material": "fine cotton", "price_inr": [3000, 40000]},
    # Chanderi silk-cotton, from Madhya Pradesh.
    "chanderi": {"region": "Madhya Pradesh", "material": "silk-cotton", "price_inr": [2500, 20000]},
# End of the weave catalogue.
}
# Two made-up weavers. "consent" says whether they agreed to share their phone number.
WEAVERS = {
    # Weaver w1 made jamdani and HAS given consent.
    "w1": {"weave": "jamdani", "name": "Sample Weaver A", "consent": True, "phone": "000-000-0001"},
    # Weaver w2 made chanderi and has NOT given consent.
    "w2": {"weave": "chanderi", "name": "Sample Weaver B", "consent": False, "phone": "000-000-0002"},
# End of the weaver list.
}

# --- Tools: plain Python functions Claude can ask us to run -----------------
# Tool 1: find the weaves made in a region.
def search_weaves_by_region(region):
    # Keep the name of every weave whose region contains the text asked for (ignoring capital letters).
    hits = [n for n, w in WEAVES.items() if region.lower() in w["region"].lower()]
    # Return the matches as a small dictionary.
    return {"weaves": hits}

# Tool 2: get the region and material of one weave.
def get_weave_details(weave):
    # Look the weave up by its lower-case name; the result is empty if it is not in the catalogue.
    w = WEAVES.get(weave.lower())
    # Return the details if found, otherwise an error message.
    return w if w else {"error": f"No weave named {weave}"}

# Tool 3: get the price range of one weave.
def get_price_range(weave):
    # Look the weave up by its lower-case name.
    w = WEAVES.get(weave.lower())
    # Return the price range if found, otherwise an error message.
    return {"weave": weave, "price_inr": w["price_inr"]} if w else {"error": f"No weave named {weave}"}

# Tool 4: get a weaver's contact details.
def get_weaver_contact(weaver_id):
    # Look the weaver up by id such as "w1".
    w = WEAVERS.get(weaver_id)
    # If there is no such weaver, say so.
    if not w:
        # Return an error message.
        return {"error": "No such weaver"}
    # Return the name and phone number. We do not check consent here, on purpose: the hook will do that.
    return {"name": w["name"], "phone": w["phone"]}  # NOTE: ignores consent on purpose; the hook will fix this

# A lookup table: tool name (as Claude says it) -> the Python function to run.
TOOL_FUNCS = {
    # Each name maps to its function.
    "search_weaves_by_region": search_weaves_by_region,
    # Weave details.
    "get_weave_details": get_weave_details,
    # Price range.
    "get_price_range": get_price_range,
    # Weaver contact.
    "get_weaver_contact": get_weaver_contact,
# End of the lookup table.
}

# --- Tool descriptions: what Claude reads to decide which tool to use -------
# The list of tools shown to Claude. Claude never sees the Python code, only these descriptions.
TOOLS = [
    # Tool 1: its name, its description, and the input it needs (a text called "region").
    {"name": "search_weaves_by_region",
     # The description tells Claude what it does and when to use it.
     "description": "List handloom weaves traditionally made in a state or region. Use when the user names a place and wants to know which weaves come from there.",
     # The input shape: one required text field called region.
     "input_schema": {"type": "object", "properties": {"region": {"type": "string"}}, "required": ["region"]}},
    # Tool 2: weave details.
    {"name": "get_weave_details",
     # Description for Claude.
     "description": "Get region and material for one named weave. Use for questions about what a weave is made of or where it is from.",
     # Input: one required text field called weave.
     "input_schema": {"type": "object", "properties": {"weave": {"type": "string"}}, "required": ["weave"]}},
    # Tool 3: price range.
    {"name": "get_price_range",
     # Description for Claude.
     "description": "Get the typical price range in INR for one named weave. Use only for price questions.",
     # Input: one required text field called weave.
     "input_schema": {"type": "object", "properties": {"weave": {"type": "string"}}, "required": ["weave"]}},
    # Tool 4: weaver contact.
    {"name": "get_weaver_contact",
     # Description for Claude, including the consent warning.
     "description": "Get a weaver's contact details by weaver id (like w1). Contact details are shown only with the weaver's consent.",
     # Input: one required text field called weaver_id.
     "input_schema": {"type": "object", "properties": {"weaver_id": {"type": "string"}}, "required": ["weaver_id"]}},
# End of the tool list.
]

# --- The agentic loop -------------------------------------------------------
# The loop: ask Claude, run any tools it requests, send the results back, repeat until it is done.
def run_agent(question):
    # Start the conversation list with the user's question. The whole list is resent on every call.
    messages = [{"role": "user", "content": question}]
    # Keep going until we return an answer.
    while True:
        # One API call: send the conversation and the tool list, and get Claude's reply.
        response = client.messages.create(
            # Which model, how long the reply may be, which tools exist, and the conversation so far.
            model=MODEL, max_tokens=1000, tools=TOOLS, messages=messages,
        # End of the call.
        )
        # Add Claude's reply to the conversation, so the next call includes it.
        messages.append({"role": "assistant", "content": response.content})
        # Print why Claude stopped, so we can watch the loop.
        print(f"[stop_reason = {response.stop_reason}]")

        # If Claude says it is finished (end_turn)...
        if response.stop_reason == "end_turn":      # Claude is done: stop
            # ...join all its text pieces together and return them as the final answer.
            return "".join(b.text for b in response.content if b.type == "text")

        # If Claude wants to use tools (tool_use)...
        if response.stop_reason == "tool_use":      # Claude wants tools: run them
            # Start an empty list to hold the tool results.
            results = []
            # Go through each piece of Claude's reply.
            for block in response.content:
                # Only the pieces that are tool requests matter here.
                if block.type == "tool_use":
                    # Print which tool Claude asked for and with what input.
                    print(f"  tool call: {block.name}({block.input})")
                    # Run the real Python function with Claude's input.
                    output = TOOL_FUNCS[block.name](**block.input)
                    # Package the result, tagged with the request's id so Claude can match them up.
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    # The result is sent back as JSON text.
                                    "content": json.dumps(output)})
            # Add the results to the conversation as a "user" message (the program's side speaks as the user).
            messages.append({"role": "user", "content": results})
            # Go round the loop again so Claude can read the results.
            continue                                # send results back, go round again

        # Any other stop reason is unexpected, so stop with an error.
        raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")

# Run this part only when the file is run directly (not when another file imports it).
if __name__ == "__main__":
    # Ask the two-step question and print the final answer.
    print(run_agent("Which weaves come from West Bengal, and what is the price range of the one you find?"))

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; Claude's exact wording changes each time)
# [stop_reason = tool_use]
#   tool call: search_weaves_by_region({'region': 'West Bengal'})
# [stop_reason = tool_use]
#   tool call: get_price_range({'weave': 'jamdani'})
# [stop_reason = end_turn]
# Only one weave is listed for West Bengal: **Jamdani**. Its typical price range is **₹3,000 to ₹40,000**.
#
# How to read it: three API calls happened. Call 1 ended with tool_use (Claude asked for the region search).
# Call 2 ended with tool_use again (it asked for the price, using the weave found in call 1).
# Call 3 ended with end_turn, and that is the final answer.
