"""Day 1, step 0: check that the API key works with one tiny call."""
# Load a helper that reads the secret settings stored in the .env file.
from dotenv import load_dotenv
# Load Anthropic's tool for talking to Claude from Python.
import anthropic

# Read ANTHROPIC_API_KEY from the .env file into the program's settings.
load_dotenv()  # reads ANTHROPIC_API_KEY from the .env file
# Create the connection to Claude. It finds the key by its name on its own.
client = anthropic.Anthropic()  # finds the key by its name

# Send one request to Claude and keep the reply in a variable called response.
response = client.messages.create(
    # Choose the small, cheap model.
    model="claude-haiku-5-5",
    # Allow at most 100 tokens (small chunks of text) in the reply.
    max_tokens=100,
    # The conversation so far: one message from the user (the program's side) with the question.
    messages=[{"role": "user", "content": "In one short sentence, what is a handloom saree?"}],
# End of the request.
)

# Print the text of Claude's reply. content[0] is the first block of the reply.
print(response.content[0].text)
# Print why Claude stopped writing. "end_turn" means it finished its answer naturally.
print("stop_reason:", response.stop_reason)

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026; Claude's exact wording changes each time)
# A handloom saree is a traditional Indian garment, a long piece of fabric draped around the body, woven on a manually operated loom rather than a power loom.
# stop_reason: end_turn
#
# How to read it: line 1 is Claude's answer. Line 2 says it stopped because it was done.
