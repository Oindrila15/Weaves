"""Chapter 5 (exam topic 4.5): the Message Batches API.

Same extraction job as before, but sent as ONE batch of many requests. A batch is cheaper (about half price)
but is not instant: results can take up to 24 hours, and there is no promise on speed.
Two steps, because the answer does not come straight back:
  python ch5_batch.py submit    -> sends the batch and saves its id in batch_id.txt
  python ch5_batch.py collect   -> checks the batch; when finished, prints each result by custom_id
Each request carries a custom_id we choose, because results can come back in ANY order.
"""
# Used to read the command word (submit or collect) typed after the script name.
import sys
# Tool for turning Python data into JSON text.
import json
# Used to find the folder this script is in, so batch_id.txt is saved next to it.
from pathlib import Path
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
# Where we remember the batch id between the two steps.
ID_FILE = Path(__file__).parent / "batch_id.txt"

# Five made-up listings. In real life this would be hundreds or thousands.
LISTINGS = {
    # The custom_id (our own label) on the left, the listing text on the right.
    "listing-001": "Chanderi silk cotton saree. Rs 4,200.",
    "listing-002": "Kanjivaram pure silk, zari border, from Kanchipuram. Rs 18,500.",
    "listing-003": "Jamdani cotton, woven in Dhaka style. approx. 7k.",
    "listing-004": "Banarasi brocade saree. Price on request.",
    "listing-005": "Kota Doria cotton-silk, square check. Rs 3,800.",
}
# The record blueprint (nullable price, because "on request" has no number).
SCHEMA = {"type": "object", "properties": {"weave": {"type": "string"}, "price_inr": {"type": ["integer", "null"]}}, "required": ["weave", "price_inr"]}


# Build the parameters for one request (the same shape as a normal call).
def params(text, model=MODEL):
    # Same kind of forced-tool call we used in Chapter 3.
    return {"model": model, "max_tokens": 3000, "system": "Extract one saree record. Use null if a price is not stated.",
            "messages": [{"role": "user", "content": text}],
            "tools": [{"name": "record", "description": "Save the record.", "input_schema": SCHEMA}],
            "tool_choice": {"type": "tool", "name": "record"}}


# Step 1: send the batch.
def submit():
    # One entry per listing: our custom_id plus the normal request parameters.
    reqs = [{"custom_id": cid, "params": params(text)} for cid, text in LISTINGS.items()]
    # Send them all at once.
    batch = client.messages.batches.create(requests=reqs)
    # Remember the batch id for step 2.
    ID_FILE.write_text(batch.id)
    # Report what we got back.
    print("submitted batch", batch.id, "status:", batch.processing_status, "requests:", batch.request_counts)


# Step 2: check the batch and print results if it has finished.
def collect():
    # Read the saved batch id.
    bid = ID_FILE.read_text().strip()
    # Ask for the batch's current state.
    batch = client.messages.batches.retrieve(bid)
    # Print the state.
    print("batch", bid, "status:", batch.processing_status, "counts:", batch.request_counts)
    # If it is not finished, stop here and say so.
    if batch.processing_status != "ended":
        # Nothing to collect yet.
        print("not finished yet; run 'collect' again later")
        # Leave the function.
        return
    # Go through the results; each carries our custom_id, so order does not matter.
    for item in client.messages.batches.results(bid):
        # Succeeded: pull out the tool call's input (the record).
        if item.result.type == "succeeded":
            # Find the tool call in the reply.
            rec = next(b.input for b in item.result.message.content if b.type == "tool_use")
            # Print the id and the record.
            print(item.custom_id, "->", json.dumps(rec))
        # Anything else (errored, expired, canceled): print it, so we can resubmit ONLY these.
        else:
            # Print the id and the failure type.
            print(item.custom_id, "-> FAILED:", item.result.type)


# Run whichever step was typed on the command line.
{"submit": submit, "collect": collect}[sys.argv[1]]()

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 12 Nov 2026; five requests, batch finished in about 3 minutes)
# submitted batch msgbatch_01SJ... status: in_progress requests: processing=5
# (after ~45 seconds) status: in_progress   (after ~2.5 minutes) status: ended, succeeded=5
# listing-001 -> {"weave": "Chanderi silk cotton", "price_inr": 4200}
# listing-005 -> {"weave": "Kota Doria cotton-silk, square check", "price_inr": 3800}
# listing-003 -> {"weave": "Jamdani cotton, woven in Dhaka style", "price_inr": 7000}
# listing-004 -> {"weave": "Banarasi brocade", "price_inr": null}
# listing-002 -> {"weave": "Kanjivaram pure silk, zari border", "price_inr": 18500}
#
# How to read it: the results did NOT come back in the order we sent them (001, 005, 003, 004, 002), so custom_id is how we match each
# result to its listing. This small batch was quick, but the guarantee is only "within 24 hours", so never use a batch where someone waits.
