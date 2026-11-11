"""Chapter 3 (exam topic 4.3): structured output with a schema.

Two experiments on tool_choice and on enum design.
  A. tool_choice: "auto", "any", and forcing one named tool, on an input that is NOT a saree listing.
  B. enum design: a closed list of weave names versus a list that also has "other" plus a detail field,
     on a weave that is not in the list (Kota Doria).
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

# ------------------------------------------------------------------ Experiment A
# The record tool: its input_schema is the blueprint for the record. Fields may be null.
RECORD_TOOL = {
    # The tool's name.
    "name": "record_weave",
    # What it is for (Claude reads this to decide when to call it).
    "description": "Save one saree record extracted from a product listing. Use only when the text is a saree listing.",
    # The blueprint.
    "input_schema": {"type": "object",
                     # Two fields, both allowed to be null.
                     "properties": {"weave": {"type": ["string", "null"]}, "price_inr": {"type": ["integer", "null"]}},
                     # Both fields must be present (but may be null).
                     "required": ["weave", "price_inr"]},
}
# A second tool, so that "any" has a real choice to make.
REVIEW_TOOL = {
    # The tool's name.
    "name": "send_to_human_review",
    # What it is for.
    "description": "Use when the text is not a saree listing or cannot be turned into a record. Give the reason.",
    # The blueprint: just a reason.
    "input_schema": {"type": "object", "properties": {"reason": {"type": "string"}}, "required": ["reason"]},
}
# An input that is NOT a saree listing.
NOT_A_LISTING = "Hi, what is your return policy for sarees bought online?"
# An input that IS a listing.
LISTING = "Chanderi handloom saree, silk cotton. Price: Rs 4,200."


# Ask Claude once and say what it did: which tool it called (with its input) or what text it wrote.
def act(text, tool_choice):
    # Send the request with both tools offered and the chosen tool_choice setting.
    r = client.messages.create(model=MODEL, max_tokens=3000, tools=[RECORD_TOOL, REVIEW_TOOL],
                               tool_choice=tool_choice, messages=[{"role": "user", "content": text}])
    # Look for a tool call in the reply.
    for b in r.content:
        # If Claude called a tool, report its name and input.
        if b.type == "tool_use":
            return f"TOOL {b.name} {json.dumps(b.input)}"
    # Otherwise Claude wrote plain text.
    return "TEXT " + "".join(b.text for b in r.content if b.type == "text")[:70].replace("\n", " ")


# Print the heading for experiment A.
print("=== A. tool_choice on a message that is NOT a listing ===")
# Try the three settings.
for label, choice in (("auto", {"type": "auto"}), ("any", {"type": "any"}), ("forced record_weave", {"type": "tool", "name": "record_weave"})):
    # Print what Claude did with each setting.
    print(f"{label:20} -> {act(NOT_A_LISTING, choice)}")
# Show "any" on a real listing, to see it pick the right tool.
print(f"{'any (real listing)':20} -> {act(LISTING, {'type': 'any'})}")

# ------------------------------------------------------------------ Experiment B
# The weave names we know about.
KNOWN = ["chanderi", "jamdani", "kanjivaram", "banarasi"]
# Schema 1: closed list. Claude must choose one of the four, whatever the saree is.
CLOSED = {"type": "object", "properties": {"weave": {"type": "string", "enum": KNOWN}}, "required": ["weave"]}
# Schema 2: the list plus "other", and a detail field to say what "other" is.
OPEN = {"type": "object",
        # weave can be one of the known names, or "other".
        "properties": {"weave": {"type": "string", "enum": KNOWN + ["other"]},
                       # When weave is "other", this says what it actually is. Otherwise null.
                       "weave_detail": {"type": ["string", "null"], "description": "If weave is other, the weave named on the page. Otherwise null."}},
        # Both fields present.
        "required": ["weave", "weave_detail"]}
# A listing for a weave that is not in our list.
KOTA = "Kota Doria cotton-silk saree, square-check weave from Kota, Rajasthan. Rs 3,800."


# Force Claude to fill a schema and return the filled-in record.
def fill(schema, text):
    # Offer one tool whose input is the schema, and force Claude to call it.
    r = client.messages.create(model=MODEL, max_tokens=3000, messages=[{"role": "user", "content": text}],
                               tools=[{"name": "record", "description": "Save the weave.", "input_schema": schema}],
                               tool_choice={"type": "tool", "name": "record"})
    # Return the tool call's input (the filled-in record).
    return next(b.input for b in r.content if b.type == "tool_use")


# Print the heading for experiment B.
print("\n=== B. enum design on a Kota Doria listing ===")
# Closed list: Claude has no honest option.
print("closed enum ->", fill(CLOSED, KOTA))
# Open list: Claude can say "other" and name it.
print("enum + other ->", fill(OPEN, KOTA))

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 11 Nov 2026; one long reason shortened)
# === A. tool_choice on a message that is NOT a listing ===
# auto                 -> TEXT I don't have access to any store's return policy, so I can't tell you ...
# any                  -> TOOL send_to_human_review {"reason": "...not a saree listing... needs a human"}
# forced record_weave  -> TOOL record_weave {"weave": "N/A", "price_inr": null}
# any (real listing)   -> TOOL record_weave {"weave": "Chanderi handloom silk cotton", "price_inr": 4200}
#
# === B. enum design on a Kota Doria listing ===
# closed enum -> {'weave': 'chanderi'}
# enum + other -> {'weave': 'other', 'weave_detail': 'Kota Doria'}
#
# How to read it:
#  auto: Claude MAY answer in plain text, so a program expecting a record gets prose. any: Claude MUST call a tool but picks which.
#  forced: Claude MUST call this one, even when the input is wrong for it. It wrote "N/A" (a made-up placeholder) in a text field.
#  Closed enum: Kota Doria is not on the list, so Claude silently chose "chanderi". Valid shape, wrong meaning, no warning.
#  Enum + other: Claude said "other" and named it. The data is honest and the new weave can be spotted and added later.
