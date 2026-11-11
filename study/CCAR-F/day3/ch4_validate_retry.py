"""Chapter 4 (exam topic 4.4): validate, retry with the specific error, or send to a human.

A small pipeline: extract -> check with our own code -> if it fails, retry ONCE with the page, the failed
attempt and the specific error -> if it still fails, mark it "needs_review" (a human looks at it).
Three made-up pages:
  P1 is clean: passes the first time.
  P2 is fine on the page, but we plant a typo in the FIRST attempt (700 instead of 7000), to show a retry that works.
  P3 contradicts itself: the page's own total does not match its items, so no retry can fix it.
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

# The record blueprint: nullable fields, line items so code can add them up, and the total as written.
SCHEMA = {
    # A record is an object.
    "type": "object",
    # The fields.
    "properties": {
        # The weave name.
        "weave": {"type": ["string", "null"]},
        # Each line on the order summary: name and amount in rupees.
        "line_items": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "amount_inr": {"type": "integer"}}, "required": ["name", "amount_inr"]}},
        # The total exactly as the page writes it.
        "stated_total_inr": {"type": ["integer", "null"], "description": "The total exactly as written on the page."},
    # End of the fields.
    },
    # All three must be present.
    "required": ["weave", "line_items", "stated_total_inr"],
# End of the blueprint.
}
# The rules for Claude.
RULES = "Extract one saree record. Report only what the page states; use null if not stated. stated_total_inr is the total as written, even if it looks wrong."

# Page 1: clean. Items add up: 7000 + 200 = 7200.
P1 = "Jamdani saree, fine cotton. Order summary: Saree Rs 7,000; Shipping Rs 200; Total Rs 7,200."
# Page 3: contradicts itself. Items add up to 7200 but the page says 7,900.
P3 = "Jamdani saree, fine cotton. Order summary: Saree Rs 7,000; Shipping Rs 200; Total Rs 7,900."


# Ask Claude to fill the record. 'history' lets us add earlier turns (used for the retry).
def extract(messages):
    # Offer one tool whose input is the schema, and force Claude to call it.
    r = client.messages.create(model=MODEL, max_tokens=3000, system=RULES, messages=messages,
                               tools=[{"name": "record", "description": "Save the record.", "input_schema": SCHEMA}],
                               tool_choice={"type": "tool", "name": "record"})
    # Return the filled-in record.
    return next(b.input for b in r.content if b.type == "tool_use")


# OUR check: code, not Claude. Returns a specific error message, or None if the record is consistent.
def validate(rec):
    # Add up the items ourselves.
    calc = sum(i["amount_inr"] for i in rec["line_items"])
    # Compare with the stated total.
    if rec["stated_total_inr"] is not None and calc != rec["stated_total_inr"]:
        # A specific message: both numbers, and what to do.
        return f"The line items add up to {calc} but stated_total_inr is {rec['stated_total_inr']}. Re-read the page and correct any value you misread."
    # Nothing wrong found.
    return None


# The pipeline for one page. 'planted' is an optional wrong first attempt (used only to demonstrate a fixable error).
def pipeline(page, planted=None):
    # First attempt: Claude's own, or the planted one.
    first = planted if planted else extract([{"role": "user", "content": page}])
    # Check it with our code.
    err = validate(first)
    # Passed the first time.
    if err is None:
        return {"status": "saved", "tries": 1, "record": first}
    # Failed: retry ONCE with the page, the failed attempt, and the specific error.
    second = extract([{"role": "user", "content": page},
                      {"role": "assistant", "content": "My first attempt: " + json.dumps(first)},
                      {"role": "user", "content": "That failed a check: " + err}])
    # Check the retry.
    err2 = validate(second)
    # Fixed by the retry.
    if err2 is None:
        return {"status": "saved", "tries": 2, "first_error": err, "record": second}
    # Still wrong: do NOT retry forever. Send it to a person, with the reason.
    return {"status": "needs_review", "tries": 2, "first_error": err, "error_after_retry": err2}


# A first attempt with a planted typo: the saree line is 700, not 7000.
PLANTED = {"weave": "Jamdani", "line_items": [{"name": "Saree", "amount_inr": 700}, {"name": "Shipping", "amount_inr": 200}], "stated_total_inr": 7200}

# Run the three cases and print the outcome of each.
for name, page, planted in (("P1 clean", P1, None), ("P2 fixable (planted typo)", P1, PLANTED), ("P3 contradicts itself", P3, None)):
    # Run the pipeline.
    out = pipeline(page, planted)
    # Print the case name and a short outcome.
    print(f"\n=== {name} ===")
    # Print the result as indented JSON.
    print(json.dumps(out, indent=2))

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 11 Nov 2026; records shortened)
# === P1 clean ===                    status: saved, tries: 1  (items 7000 + 200 = 7200 = stated total)
# === P2 fixable (planted typo) ===   status: saved, tries: 2
#     first_error: "The line items add up to 900 but stated_total_inr is 7200. Re-read the page and correct any value you misread."
#     record after retry: Saree 7000, Shipping 200, total 7200  (fixed: the page had the right number)
# === P3 contradicts itself ===       status: needs_review, tries: 2
#     first_error and error_after_retry are the same: "The line items add up to 7200 but stated_total_inr is 7900."
#
# How to read it: P2 shows retry working, because the correct number WAS on the page and the specific error pointed at it.
# P3 shows retry failing, because the page itself is wrong; no retry can create the true total. So we stop after one retry and
# send it to a person. (Honest note: P2's first attempt was planted by us, since the model did not make this mistake on its own.)
