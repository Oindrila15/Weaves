"""Chapter 1 (exam topic 4.1): explicit criteria.

Same job, same claims, two prompts. Job: from a saree listing, flag the claims that Weaves must
verify before recording them. We run each prompt 3 times to see how steady the answer is.
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

# Seven claims from a made-up listing, numbered so Claude can point at them.
CLAIMS = """1. Pure handloom Chanderi silk.
2. The softest saree you will ever wear.
3. Woven by master weaver Ramesh over 21 days.
4. Handloom Mark certified.
5. Beautiful gold zari border.
6. Limited stock, only 2 left!
7. 100% pure zari."""

# Prompt V: vague. It asks for care but gives no definition of "suspicious".
VAGUE = "Flag the claims that look suspicious. Be conservative. Reply with only the claim numbers, comma separated."

# Prompt E: explicit. It defines what to flag, what to skip, and gives an example of each.
EXPLICIT = """Flag a claim ONLY if it states a checkable fact about origin, material, certification, or who made it.
Flag these:  "Pure silk" (material), "GI tagged" (certification), "Woven by Meena" (who made it).
Skip these:  opinions and praise ("so soft", "beautiful"), sales pressure ("only 2 left"), and plain descriptions of looks.
Reply with only the claim numbers, comma separated. If none, reply: none."""


# Ask Claude once with a given instruction and return its short answer.
def ask(instruction):
    # Send the instruction as the system prompt and the claims as the user message.
    # max_tokens is generous because the model may "think" first, and thinking uses the same budget (50 gave empty answers).
    r = client.messages.create(model=MODEL, max_tokens=3000, system=instruction,
                               messages=[{"role": "user", "content": CLAIMS}])
    # Join the text parts of the reply and tidy the spaces.
    return "".join(b.text for b in r.content if b.type == "text").strip()


# Run each prompt three times and print what came back.
for name, prompt in (("V vague   ", VAGUE), ("E explicit", EXPLICIT)):
    # Collect three answers.
    answers = [ask(prompt) for _ in range(3)]
    # Print them side by side.
    print(name, "->", answers)

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 4 Nov 2026)
# V vague    -> ['1, 3, 6, 7', '3, 7', '3,6,7']
# E explicit -> ['1, 3, 4, 7', '1, 3, 4, 7', '1, 3, 4, 7']
#
# How to read it: the vague prompt gave a different answer each time, and it flagged claim 6 ("only 2 left!"), which is sales
# pressure, not a fact about the saree. It also missed claim 4 (Handloom Mark) in all three runs.
# The explicit prompt gave the same, correct set every time: 1, 3, 4, 7.
# (An early run printed empty answers because max_tokens=50 was used up by the model's thinking. Lesson: leave room to think.)
