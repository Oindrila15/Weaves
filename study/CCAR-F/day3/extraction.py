"""Day 3: structured extraction (exam topics 4.1 to 4.4).

One deliberately messy product page goes in. We try four ways to turn it into a record:
  A. plain prose prompt (no structure)
  B. forced tool, strict schema where every field is required
  C. forced tool, nullable fields, an "unclear" option and explicit criteria
  D. a meaning check (stated total vs calculated total) and a retry with the specific error
The page has no weaver name (only a shop), a price written as "approx. 5k", and a total that does not add up.
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
# A running total of tokens used, so we can report the cost at the end.
TOKENS = {"in": 0, "out": 0}

# The messy product page, made up on purpose with three traps (it is just text inside quotes).
PAGE = """Chanderi handloom saree - silk cotton blend.
Woven in the town of Chanderi (Ashoknagar district). Sheer texture, gold zari border, comes with a blouse piece.
Price: approx. 5k.
Order summary: Saree Rs 4,200; Blouse piece Rs 800; Shipping Rs 150; Total Rs 5,500.
Listed by Heritage Looms Store."""

# --- B: strict schema, every field required ---------------------------------------
# The blueprint for the record. Here EVERY field must be filled, even if the page does not say.
STRICT = {
    # The record is an object (a set of named fields).
    "type": "object",
    # The fields and their types.
    "properties": {
        # The name of the weave: text.
        "weave": {"type": "string"},
        # The material: text.
        "material": {"type": "string"},
        # The region: text.
        "region": {"type": "string"},
        # The weaver's name: text, and REQUIRED (this is what forces Claude to invent one).
        "weaver_name": {"type": "string"},
        # The price: a number.
        "price_inr": {"type": "number"},
        # How much we trust the record: one of three allowed words (no honest "unclear" option).
        "trust_level": {"type": "string", "enum": ["high", "medium", "low"]},
    # End of the field list.
    },
    # All six fields must be present.
    "required": ["weave", "material", "region", "weaver_name", "price_inr", "trust_level"],
# End of the strict blueprint.
}

# --- C: nullable fields, "unclear" in the enum, line items for the meaning check --
# The better blueprint: fields may be empty (null) when the page does not say.
NULLABLE = {
    # The record is an object.
    "type": "object",
    # The fields and their types.
    "properties": {
        # The weave name: text.
        "weave": {"type": "string"},
        # The material: text or null.
        "material": {"type": ["string", "null"]},
        # The region: text or null.
        "region": {"type": ["string", "null"]},
        # The weaver: text or null, with a note that a shop is not a weaver.
        "weaver_name": {"type": ["string", "null"], "description": "The person who wove it. Null if the page does not name one. A shop or seller is not a weaver."},
        # The price: a whole number or null.
        "price_inr": {"type": ["integer", "null"], "description": "Whole rupees. Null if no price is stated."},
        # Trust level, now with an honest "unclear" option.
        "trust_level": {"type": "string", "enum": ["high", "medium", "low", "unclear"]},
        # A list of line items (name and amount), so the program can add them up itself.
        "line_items": {"type": "array", "items": {"type": "object", "properties": {
            # Each item has a name and an amount in rupees.
            "name": {"type": "string"}, "amount_inr": {"type": "integer"}}, "required": ["name", "amount_inr"]}},
        # The total exactly as the page writes it, even if it is wrong.
        "stated_total_inr": {"type": ["integer", "null"], "description": "The total exactly as written on the page."},
    # End of the field list.
    },
    # These fields must be present (but several may be null).
    "required": ["weave", "material", "region", "weaver_name", "price_inr", "trust_level", "line_items", "stated_total_inr"],
# End of the nullable blueprint.
}

# The written rules given to Claude (explicit criteria, topic 4.1).
CRITERIA = """Extract one saree record from the page.
Rules:
- Report only what the page states. If a field is not stated, use null. Never guess.
- weaver_name is a person or weaving cooperative that made the saree. A shop or seller is not a weaver.
- price_inr: if the price is written loosely ("approx. 5k"), give the number it means (5000).
- trust_level: high = names a weaver and a place; medium = names a place or material only; low = vague; unclear = cannot tell.
- stated_total_inr is the total as written, even if it does not match the items."""


# The one function that talks to Claude. With a schema, Claude must answer by filling it in; without one, it answers in plain text.
def call(messages, schema=None, system=None):
    # Gather the request settings: model, reply length, and the conversation.
    kwargs = dict(model=MODEL, max_tokens=800, messages=messages)
    # If we have written rules, send them as the system prompt.
    if system:
        # Add the rules to the request.
        kwargs["system"] = system
    # If we have a schema...
    if schema:
        # ...offer one tool whose input shape IS the schema.
        kwargs["tools"] = [{"name": "record_weave", "description": "Save one extracted weave record.", "input_schema": schema}]
        # ...and force Claude to call that tool (this is how the structured answer is produced).
        kwargs["tool_choice"] = {"type": "tool", "name": "record_weave"}
    # Send the request.
    r = client.messages.create(**kwargs)
    # Add this call's input tokens to the running total.
    TOKENS["in"] += r.usage.input_tokens
    # Add this call's output tokens to the running total.
    TOKENS["out"] += r.usage.output_tokens
    # If we used a schema...
    if schema:
        # ...return the filled-in record (the tool call's input).
        return next(b.input for b in r.content if b.type == "tool_use")
    # Otherwise return Claude's plain text.
    return "".join(b.text for b in r.content if b.type == "text")


# A helper that prints a title and then the data (text as-is, records as indented JSON).
def show(title, data):
    # Print the heading.
    print(f"\n=== {title} ===")
    # Print text as it is, or turn a record into indented JSON.
    print(data if isinstance(data, str) else json.dumps(data, indent=2))


# ---------------------------------------------------------------- A: plain prose
# Experiment A: ask in plain prose with no blueprint.
show("A. plain prose prompt", call([{"role": "user", "content": f"Pull out the key facts from this page.\n\n{PAGE}"}]))

# ---------------------------------------------------------------- B: strict schema, 3 runs
# Experiment B: three runs with the strict blueprint.
for i in range(3):
    # Ask for the record, forced through the strict schema.
    out = call([{"role": "user", "content": f"Extract the saree record from this page.\n\n{PAGE}"}], STRICT)
    # Print only the three fields that matter for this experiment.
    show(f"B. strict schema, run {i + 1}", {k: out.get(k) for k in ("weaver_name", "price_inr", "trust_level")})

# ---------------------------------------------------------------- C: nullable + criteria, 3 runs
# Experiment C: three runs with the nullable blueprint and the written rules.
for i in range(3):
    # Ask for the record: the page is the message, the rules go in the system prompt.
    out = call([{"role": "user", "content": PAGE}], NULLABLE, system=CRITERIA)
    # Print the fields that matter, plus the stated total.
    show(f"C. nullable + criteria, run {i + 1}", {k: out.get(k) for k in ("weaver_name", "price_inr", "trust_level", "stated_total_inr")})
# Keep the last record for the next experiment.
record = out
# Print that whole record.
show("C. last full record", record)


# ---------------------------------------------------------------- D: meaning check and retry
# The program's own check: do the line items add up to the stated total?
def check(rec):
    """Return a specific error message, or None when the record is fine."""
    # Add up the line items ourselves.
    calculated = sum(i["amount_inr"] for i in rec["line_items"])
    # If a total is stated and it differs from our sum...
    if rec["stated_total_inr"] is not None and calculated != rec["stated_total_inr"]:
        # ...return a specific error that names both numbers.
        return (f"The line items add up to {calculated} but stated_total_inr is {rec['stated_total_inr']}. "
                # Tell Claude what to do about it.
                "Re-read the page and fix the record if you made a mistake.")
    # Everything is consistent: no error.
    return None


# Run the check on experiment C's record.
error = check(record)
# Heading for experiment D.
print("\n=== D. meaning check ===")
# Print the error (or None).
print("error:", error)
# If the check failed, try one retry.
if error:
    # The retry sends three things: the page, the failed attempt, and the specific error.
    retry = call([
        # 1. The original page.
        {"role": "user", "content": PAGE},
        # 2. Claude's first (failed) attempt.
        {"role": "assistant", "content": f"My first attempt: {json.dumps(record)}"},
        # 3. The specific error from our check.
        {"role": "user", "content": f"That failed a check: {error}"},
    # Same blueprint and rules as before.
    ], NULLABLE, system=CRITERIA)
    # Print what the retry returned for the two fields in question.
    show("D. after retry (items, stated total)", {"line_items": retry["line_items"], "stated_total_inr": retry["stated_total_inr"]})
    # Check the retried record again.
    print("error after retry:", check(retry))

# Finally, report how many tokens the whole run used.
print(f"\nTokens used in this run: {TOKENS['in']} in, {TOKENS['out']} out")

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; shortened where marked)
# === A. plain prose prompt ===
# - **Product:** Chanderi handloom saree, silk-cotton blend
# - **Origin:** Woven in Chanderi, Ashoknagar district
# - **Features:** Sheer texture, gold zari border, includes a blouse piece
# - **Price breakdown:** Saree Rs 4,200; Blouse piece Rs 800; Shipping Rs 150; **Total: Rs 5,500**
# - **Seller:** Heritage Looms Store
# The listing says the price is "approx. 5k," but the itemized total is Rs 5,500.
#
# === B. strict schema, run 1 ===   (runs 2 and 3 were identical)
# {"weaver_name": "Heritage Looms Store", "price_inr": 4200, "trust_level": "medium"}
#
# === C. nullable + criteria, run 1 ===   (runs 2 and 3 were identical)
# {"weaver_name": null, "price_inr": 5000, "trust_level": "medium", "stated_total_inr": 5500}
#
# === C. last full record ===
# {"weave": "Chanderi handloom saree", "material": "Silk cotton blend", "region": "Chanderi, Ashoknagar district", "weaver_name": null,
#  "price_inr": 5000, "trust_level": "medium",
#  "line_items": [{"name": "Saree", "amount_inr": 4200}, {"name": "Blouse piece", "amount_inr": 800}, {"name": "Shipping", "amount_inr": 150}],
#  "stated_total_inr": 5500}
#
# === D. meaning check ===
# error: The line items add up to 5150 but stated_total_inr is 5500. Re-read the page and fix the record if you made a mistake.
#
# === D. after retry (items, stated total) ===
# {"line_items": [Saree 4200, Blouse piece 800, Shipping 150], "stated_total_inr": 5500}
# error after retry: The line items add up to 5150 but stated_total_inr is 5500. Re-read the page and fix the record if you made a mistake.
#
# Tokens used in this run: 7204 in, 2056 out
#
# How to read it: A looks fine to a person but a program cannot store it, and it missed the mismatch. B was forced to fill weaver_name,
# so it invented "Heritage Looms Store" (a shop), and price_inr 4200 is the saree line, not the price: valid shape, wrong meaning, the same three times.
# C allowed null and had written rules, so weaver_name is null and price_inr is 5000. D: our check caught 5150 vs 5500, but the retry changed nothing,
# because the page contradicts itself. The right next step is to flag the record for human review.
