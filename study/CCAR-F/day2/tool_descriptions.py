"""Day 2, lesson 1: how tool descriptions steer Claude's choice (exam topic 2.1).

We give Claude two tools and ask the same two questions several times.
We count which tool it picks FIRST. Once with vague descriptions, once with good ones.
The tools are never run; we only look at the choice.
"""
# A counter that tallies how many times each tool was picked.
from collections import Counter
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
# How many times to repeat each question (one run proves little; ten shows a pattern).
RUNS = 10

# The input shape both tools share: one required text field called "query".
one_text_input = {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}

# Vague: two tools with near-identical descriptions.
VAGUE = [
    # Tool one: a name and description that say almost nothing.
    {"name": "weave_lookup", "description": "Looks up weave data.", "input_schema": one_text_input},
    # Tool two: just as vague, and almost the same words.
    {"name": "weave_query", "description": "Queries weave data.", "input_schema": one_text_input},
# End of the vague tool list.
]
# What each vague tool really does (Claude is not told this):
# The answer key: region questions should go to weave_lookup, price questions to weave_query.
VAGUE_RIGHT = {"region": "weave_lookup", "price": "weave_query"}

# Clear: purpose, input, output, when to use, when NOT to use.
CLEAR = [
    # Tool one: lists weave names for a region.
    {"name": "list_weaves_by_region",
     # A full description: what it does, its input, its output, when to use it, when not to.
     "description": ("List the NAMES of handloom weaves traditionally made in one Indian state or region. "
                     # What to pass in, and what comes back.
                     "Input: a state name such as 'Tamil Nadu'. Returns names only, with no prices or details. "
                     # When to use it.
                     "Use when the user asks which weaves come from a place. "
                     # When NOT to use it.
                     "Do not use for questions about one named weave."),
     # The input shape.
     "input_schema": one_text_input},
    # Tool two: price of one named weave.
    {"name": "get_weave_price",
     # A full description for the price tool.
     "description": ("Get the typical price range in INR for ONE named weave, such as 'jamdani'. "
                     # What to pass in, and when to use it.
                     "Input: a weave name, not a place. Use only for price questions. "
                     # When NOT to use it.
                     "Do not use to find weaves by place."),
     # The input shape.
     "input_schema": one_text_input},
# End of the clear tool list.
]
# The answer key for the clear tools.
CLEAR_RIGHT = {"region": "list_weaves_by_region", "price": "get_weave_price"}

# The two questions we ask.
QUESTIONS = {
    # A question about a place.
    "region": "Which weaves come from Tamil Nadu?",
    # A question about a price.
    "price": "How much does a chanderi saree cost?",
# End of the questions.
}


# Ask one question and report which tool Claude picked first.
def first_tool(tools, question):
    # One API call, offering the given tools.
    r = client.messages.create(model=MODEL, max_tokens=300, tools=tools,
                               # The conversation: just the question.
                               messages=[{"role": "user", "content": question}])
    # Look through Claude's reply for a tool request.
    for b in r.content:
        # Is this piece a tool request?
        if b.type == "tool_use":
            # Return the tool's name.
            return b.name
    # Claude did not pick any tool.
    return "(no tool)"


# Run the experiment twice: once with the vague tools, once with the clear tools.
for label, tools, right in [("VAGUE descriptions", VAGUE, VAGUE_RIGHT), ("CLEAR descriptions", CLEAR, CLEAR_RIGHT)]:
    # Print a heading.
    print(f"\n=== {label} ===")
    # For each of the two questions...
    for kind, q in QUESTIONS.items():
        # ...ask it RUNS times and count which tool was chosen each time.
        picks = Counter(first_tool(tools, q) for _ in range(RUNS))
        # How many times the correct tool was chosen.
        good = picks[right[kind]]
        # Print the question.
        print(f"  Q: {q}")
        # Print the correct tool, what was chosen, and the score.
        print(f"     correct tool = {right[kind]}; chosen: {dict(picks)}  -> {good}/{RUNS} correct")

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026)
# === VAGUE descriptions ===
#   Q: Which weaves come from Tamil Nadu?
#      correct tool = weave_lookup; chosen: {'weave_lookup': 9, 'weave_query': 1}  -> 9/10 correct
#   Q: How much does a chanderi saree cost?
#      correct tool = weave_query; chosen: {'weave_lookup': 10}  -> 0/10 correct
#
# === CLEAR descriptions ===
#   Q: Which weaves come from Tamil Nadu?
#      correct tool = list_weaves_by_region; chosen: {'list_weaves_by_region': 10}  -> 10/10 correct
#   Q: How much does a chanderi saree cost?
#      correct tool = get_weave_price; chosen: {'get_weave_price': 10}  -> 10/10 correct
#
# How to read it: with vague descriptions Claude had nothing to go on, so it picked weave_lookup almost every time:
# right for the region question by luck (9/10), wrong for the price question (0/10). It was consistently wrong, not random.
# With clear descriptions it was right every time. Better descriptions were the fix.
