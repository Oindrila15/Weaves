"""Day 2, lesson 1: how tool descriptions steer Claude's choice (exam topic 2.1).

We give Claude two tools and ask the same two questions several times.
We count which tool it picks FIRST. Once with vague descriptions, once with good ones.
The tools are never run; we only look at the choice.
"""
from collections import Counter
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
RUNS = 10

one_text_input = {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}

# Vague: two tools with near-identical descriptions.
VAGUE = [
    {"name": "weave_lookup", "description": "Looks up weave data.", "input_schema": one_text_input},
    {"name": "weave_query", "description": "Queries weave data.", "input_schema": one_text_input},
]
# What each vague tool really does (Claude is not told this):
VAGUE_RIGHT = {"region": "weave_lookup", "price": "weave_query"}

# Clear: purpose, input, output, when to use, when NOT to use.
CLEAR = [
    {"name": "list_weaves_by_region",
     "description": ("List the NAMES of handloom weaves traditionally made in one Indian state or region. "
                     "Input: a state name such as 'Tamil Nadu'. Returns names only, with no prices or details. "
                     "Use when the user asks which weaves come from a place. "
                     "Do not use for questions about one named weave."),
     "input_schema": one_text_input},
    {"name": "get_weave_price",
     "description": ("Get the typical price range in INR for ONE named weave, such as 'jamdani'. "
                     "Input: a weave name, not a place. Use only for price questions. "
                     "Do not use to find weaves by place."),
     "input_schema": one_text_input},
]
CLEAR_RIGHT = {"region": "list_weaves_by_region", "price": "get_weave_price"}

QUESTIONS = {
    "region": "Which weaves come from Tamil Nadu?",
    "price": "How much does a chanderi saree cost?",
}


def first_tool(tools, question):
    r = client.messages.create(model=MODEL, max_tokens=300, tools=tools,
                               messages=[{"role": "user", "content": question}])
    for b in r.content:
        if b.type == "tool_use":
            return b.name
    return "(no tool)"


for label, tools, right in [("VAGUE descriptions", VAGUE, VAGUE_RIGHT), ("CLEAR descriptions", CLEAR, CLEAR_RIGHT)]:
    print(f"\n=== {label} ===")
    for kind, q in QUESTIONS.items():
        picks = Counter(first_tool(tools, q) for _ in range(RUNS))
        good = picks[right[kind]]
        print(f"  Q: {q}")
        print(f"     correct tool = {right[kind]}; chosen: {dict(picks)}  -> {good}/{RUNS} correct")
