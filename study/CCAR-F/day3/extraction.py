"""Day 3: structured extraction (exam topics 4.1 to 4.4).

One deliberately messy product page goes in. We try four ways to turn it into a record:
  A. plain prose prompt (no structure)
  B. forced tool, strict schema where every field is required
  C. forced tool, nullable fields, an "unclear" option and explicit criteria
  D. a meaning check (stated total vs calculated total) and a retry with the specific error
The page has no weaver name (only a shop), a price written as "approx. 5k", and a total that does not add up.
"""
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
TOKENS = {"in": 0, "out": 0}

PAGE = """Chanderi handloom saree - silk cotton blend.
Woven in the town of Chanderi (Ashoknagar district). Sheer texture, gold zari border, comes with a blouse piece.
Price: approx. 5k.
Order summary: Saree Rs 4,200; Blouse piece Rs 800; Shipping Rs 150; Total Rs 5,500.
Listed by Heritage Looms Store."""

# --- B: strict schema, every field required ---------------------------------------
STRICT = {
    "type": "object",
    "properties": {
        "weave": {"type": "string"},
        "material": {"type": "string"},
        "region": {"type": "string"},
        "weaver_name": {"type": "string"},
        "price_inr": {"type": "number"},
        "trust_level": {"type": "string", "enum": ["high", "medium", "low"]},
    },
    "required": ["weave", "material", "region", "weaver_name", "price_inr", "trust_level"],
}

# --- C: nullable fields, "unclear" in the enum, line items for the meaning check --
NULLABLE = {
    "type": "object",
    "properties": {
        "weave": {"type": "string"},
        "material": {"type": ["string", "null"]},
        "region": {"type": ["string", "null"]},
        "weaver_name": {"type": ["string", "null"], "description": "The person who wove it. Null if the page does not name one. A shop or seller is not a weaver."},
        "price_inr": {"type": ["integer", "null"], "description": "Whole rupees. Null if no price is stated."},
        "trust_level": {"type": "string", "enum": ["high", "medium", "low", "unclear"]},
        "line_items": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string"}, "amount_inr": {"type": "integer"}}, "required": ["name", "amount_inr"]}},
        "stated_total_inr": {"type": ["integer", "null"], "description": "The total exactly as written on the page."},
    },
    "required": ["weave", "material", "region", "weaver_name", "price_inr", "trust_level", "line_items", "stated_total_inr"],
}

CRITERIA = """Extract one saree record from the page.
Rules:
- Report only what the page states. If a field is not stated, use null. Never guess.
- weaver_name is a person or weaving cooperative that made the saree. A shop or seller is not a weaver.
- price_inr: if the price is written loosely ("approx. 5k"), give the number it means (5000).
- trust_level: high = names a weaver and a place; medium = names a place or material only; low = vague; unclear = cannot tell.
- stated_total_inr is the total as written, even if it does not match the items."""


def call(messages, schema=None, system=None):
    kwargs = dict(model=MODEL, max_tokens=800, messages=messages)
    if system:
        kwargs["system"] = system
    if schema:
        kwargs["tools"] = [{"name": "record_weave", "description": "Save one extracted weave record.", "input_schema": schema}]
        kwargs["tool_choice"] = {"type": "tool", "name": "record_weave"}
    r = client.messages.create(**kwargs)
    TOKENS["in"] += r.usage.input_tokens
    TOKENS["out"] += r.usage.output_tokens
    if schema:
        return next(b.input for b in r.content if b.type == "tool_use")
    return "".join(b.text for b in r.content if b.type == "text")


def show(title, data):
    print(f"\n=== {title} ===")
    print(data if isinstance(data, str) else json.dumps(data, indent=2))


# ---------------------------------------------------------------- A: plain prose
show("A. plain prose prompt", call([{"role": "user", "content": f"Pull out the key facts from this page.\n\n{PAGE}"}]))

# ---------------------------------------------------------------- B: strict schema, 3 runs
for i in range(3):
    out = call([{"role": "user", "content": f"Extract the saree record from this page.\n\n{PAGE}"}], STRICT)
    show(f"B. strict schema, run {i + 1}", {k: out.get(k) for k in ("weaver_name", "price_inr", "trust_level")})

# ---------------------------------------------------------------- C: nullable + criteria, 3 runs
for i in range(3):
    out = call([{"role": "user", "content": PAGE}], NULLABLE, system=CRITERIA)
    show(f"C. nullable + criteria, run {i + 1}", {k: out.get(k) for k in ("weaver_name", "price_inr", "trust_level", "stated_total_inr")})
record = out
show("C. last full record", record)


# ---------------------------------------------------------------- D: meaning check and retry
def check(rec):
    """Return a specific error message, or None when the record is fine."""
    calculated = sum(i["amount_inr"] for i in rec["line_items"])
    if rec["stated_total_inr"] is not None and calculated != rec["stated_total_inr"]:
        return (f"The line items add up to {calculated} but stated_total_inr is {rec['stated_total_inr']}. "
                "Re-read the page and fix the record if you made a mistake.")
    return None


error = check(record)
print("\n=== D. meaning check ===")
print("error:", error)
if error:
    retry = call([
        {"role": "user", "content": PAGE},
        {"role": "assistant", "content": f"My first attempt: {json.dumps(record)}"},
        {"role": "user", "content": f"That failed a check: {error}"},
    ], NULLABLE, system=CRITERIA)
    show("D. after retry (items, stated total)", {"line_items": retry["line_items"], "stated_total_inr": retry["stated_total_inr"]})
    print("error after retry:", check(retry))

print(f"\nTokens used in this run: {TOKENS['in']} in, {TOKENS['out']} out")
