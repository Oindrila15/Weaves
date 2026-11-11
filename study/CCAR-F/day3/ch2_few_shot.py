"""Chapter 2 (exam topic 4.2): few-shot examples.

Job: turn a messy price phrase from a saree listing into whole rupees (a number), or null.
The hard part is a Weaves house rule that Claude cannot guess: for a RANGE we record the MIDPOINT.
We try the job with plain rules only (zero-shot), then with worked examples (few-shot).
(A first version of this file tested easy cases and both prompts scored the same; see the note at the bottom.)
"""
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

# Prices to convert. Each is a made-up listing phrase; the last four are the tricky ones.
PRICES = ["Rs 4,200", "Rs 4,200 to Rs 4,800", "Rs 9,000 - 11,000", "Price on request", "Rs 3,500 (offer price), MRP Rs 5,000"]

# The rules, with NO examples (zero-shot). It says what to return but not how to settle the hard cases.
ZERO_SHOT = "Convert the price phrase into whole rupees as a plain integer. If there is no price, reply null. Reply with only the integer or null."

# The same rules PLUS worked examples (few-shot). Each example shows the input, the answer and the reason.
FEW_SHOT = ZERO_SHOT + """

Examples:
Input: Rs 6,500 to Rs 7,500
Answer: 7000
Reason: for a range we record the midpoint, (6500 + 7500) / 2.

Input: Price on request
Answer: null
Reason: no number is given, so we must not invent one.

Input: Rs 2,100 (sale), was Rs 3,000
Answer: 2100
Reason: when a sale price and an old price both appear, return the price the buyer pays now.

Input: 8k
Answer: 8000
Reason: k means thousand."""


# Ask Claude once for one price phrase using a given instruction; return its short answer.
def ask(instruction, phrase):
    # The instruction is the system prompt; the price phrase is the user message.
    r = client.messages.create(model=MODEL, max_tokens=3000, system=instruction,
                               messages=[{"role": "user", "content": phrase}])
    # Join the text parts of the reply and tidy the spaces.
    return "".join(b.text for b in r.content if b.type == "text").strip()


# Print a small table: one row per price phrase, three runs for each of the two prompts.
print(f"{'phrase':40} | {'zero-shot x3':28} | few-shot x3")
# Go through every price phrase.
for p in PRICES:
    # Three answers with rules only.
    z = [ask(ZERO_SHOT, p) for _ in range(3)]
    # Three answers with rules plus examples.
    f = [ask(FEW_SHOT, p) for _ in range(3)]
    # Print the row.
    print(f"{p:40} | {str(z):28} | {f}")

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 11 Nov 2026)
# phrase                                   | zero-shot x3                 | few-shot x3
# Rs 4,200                                 | ['4200', '4200', '4200']     | ['4200', '4200', '4200']
# Rs 4,200 to Rs 4,800                     | ['4200', '4200', '4200']     | ['4500', '4500', '4500']
# Rs 9,000 - 11,000                        | ['9000', '9000', '9000']     | ['10000', '10000', '10000']
# Price on request                         | ['null', 'null', 'null']     | ['null', 'null', 'null']
# Rs 3,500 (offer price), MRP Rs 5,000     | ['3500', '3500', '3500']     | ['3500', '3500', '3500']
#
# How to read it: easy cases (a plain price, "on request", a sale price) were right with NO examples. The model already knows them.
# The examples mattered only for the house rule "a range is recorded as its midpoint". Zero-shot took the lower number (a sensible guess,
# but not our rule). Few-shot gave 4500, and also 10000 for a range it had never seen: it learned the rule, not the three examples.
# Honest note: a first version of this file used only easy cases and both prompts scored the same. Few-shot is for conventions and
# judgement calls the model cannot guess, not for things it already does well.
