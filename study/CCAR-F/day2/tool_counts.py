"""Day 2, lesson 3: how many tools, which tools, and tool_choice (exam topic 2.3).

Part A: the same questions with 4 tools versus 18 tools (accuracy and input size).
Part B: the three tool_choice settings.
Part C: a role that simply does not have the dangerous tool.
Tools are never run; we only look at what Claude asks for.
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
# How many times to repeat each question.
RUNS = 10


# A shortcut for building a tool definition: a name, a description, and one required text input.
def t(name, desc, arg="query"):
    # Return the tool as a dictionary in the shape the API expects.
    return {"name": name, "description": desc,
            # The input shape: one required text field.
            "input_schema": {"type": "object", "properties": {arg: {"type": "string"}}, "required": [arg]}}


# --- the four tools Weaves actually needs for these questions -----------------
# The four core tools.
CORE = [
    # Weave names for a region.
    t("list_weaves_by_region", "List the names of handloom weaves traditionally made in one Indian state. Input: a state name such as 'Tamil Nadu'. Names only. Not for questions about one named weave."),
    # Region and material of one weave.
    t("get_weave_details", "Get the region and material of ONE named weave, such as 'jamdani'. Not for prices and not for finding weaves by place."),
    # Price range of one weave.
    t("get_weave_price", "Get the typical price range in INR for ONE named weave, such as 'jamdani'. Use only for price questions."),
    # A weaver's contact details.
    t("get_weaver_contact", "Get a weaver's contact details by weaver id such as 'w1'. Shown only with the weaver's consent."),
# End of the core list.
]
# --- fourteen more tools that are each a real, different job -----------------
# Fourteen extra tools, each with a clearly different job (so they do not look alike).
EXTRA = [
    # History of a weave.
    t("get_weave_history", "Get a short history of ONE named weave, such as 'banarasi'. Not for prices or materials."),
    # Price changes over the years.
    t("get_weave_price_trends", "Get how the price of ONE named weave has changed over the past years. Not for today's price range."),
    # Two weaves side by side.
    t("compare_weaves", "Compare two named weaves side by side. Input: two names separated by a comma."),
    # Geographical Indication status.
    t("get_gi_tag_status", "Check whether ONE named weave has a Geographical Indication (GI) tag."),
    # Care instructions.
    t("get_care_instructions", "Get washing and storage care instructions for ONE named weave."),
    # Draping styles by region.
    t("get_drape_styles", "Get regional draping styles for sarees. Input: a state name."),
    # Festival suggestions.
    t("find_festival_sarees", "Suggest weaves traditionally worn for a named festival, such as 'Onam'."),
    # Dyeing methods.
    t("get_dye_methods", "Get the traditional dyeing methods used for ONE named weave."),
    # Loom type.
    t("get_loom_type", "Get the type of loom used for ONE named weave."),
    # Weaver cooperatives.
    t("list_weaver_cooperatives", "List weaver cooperatives in a named state."),
    # Spotting fakes.
    t("get_authenticity_checks", "Get tips for checking whether a saree of a named weave is genuine."),
    # Museums.
    t("get_museum_collections", "List museums that hold textiles of ONE named weave."),
    # Buying advice.
    t("get_buying_guide", "Get general advice for first-time saree buyers. Input: a budget in INR."),
    # A weaver's public story.
    t("get_weaver_story", "Get the public profile story of a weaver by weaver id such as 'w1'. No contact details."),
# End of the extra list.
]
# The big set: 4 core + 14 extra = 18 tools.
BIG = CORE + EXTRA

# The three questions, each with the set of tools that would be a correct pick.
QUESTIONS = [
    # A region question.
    ("Which weaves come from Tamil Nadu?", {"list_weaves_by_region"}),
    # A price question.
    ("How much does a chanderi saree cost?", {"get_weave_price"}),
    # A material question.
    ("What material is jamdani made of?", {"get_weave_details"}),
# End of the questions.
]


# Ask one question; return the tool Claude picked first and how many input tokens the request used.
def first_tool(tools, q):
    # One API call, offering the given tools.
    r = client.messages.create(model=MODEL, max_tokens=300, tools=tools,
                               # The conversation: just the question.
                               messages=[{"role": "user", "content": q}])
    # The name of the first tool requested, or "(no tool)" if none.
    name = next((b.name for b in r.content if b.type == "tool_use"), "(no tool)")
    # Return the name and the input size in tokens.
    return name, r.usage.input_tokens


# Part A heading.
print("=== PART A: 4 tools versus 18 tools ===")
# Run the test once with 4 tools and once with 18.
for label, tools in [("4 tools", CORE), ("18 tools", BIG)]:
    # Totals: correct answers, questions asked, and input tokens per request.
    total_ok, total, tokens = 0, 0, 0
    # For each question...
    for q, right in QUESTIONS:
        # ...start a fresh tally of picks.
        picks = Counter()
        # Ask it RUNS times.
        for _ in range(RUNS):
            # Get the pick and the input size.
            name, tok = first_tool(tools, q)
            # Record the pick.
            picks[name] += 1
            # Remember the input size (it is the same every time).
            tokens = tok          # input tokens per call (the same each time)
        # Count the picks that were correct.
        ok = sum(n for name, n in picks.items() if name in right)
        # Add to the totals.
        total_ok += ok; total += RUNS
        # Print this question's score (and the picks if any were wrong).
        print(f"  [{label}] {q}  -> {ok}/{RUNS} correct  {dict(picks) if ok < RUNS else ''}")
    # Print the overall score and the input size.
    print(f"  [{label}] overall {total_ok}/{total} correct; input size per request: about {tokens} tokens\n")

# Part B heading.
print("=== PART B: tool_choice ===")
# A greeting that needs no tool at all.
GREETING = "Hi! What can you help me with?"
# Try the three tool_choice settings on the greeting.
for label, choice in [("auto (Claude decides)", {"type": "auto"}),
                      # "any": Claude must call some tool.
                      ("any (must call some tool)", {"type": "any"}),
                      # "tool": Claude must call this one specific tool.
                      ("forced get_weave_price", {"type": "tool", "name": "get_weave_price"})]:
    # One API call with that setting.
    r = client.messages.create(model=MODEL, max_tokens=300, tools=CORE, tool_choice=choice,
                               # The conversation: the greeting.
                               messages=[{"role": "user", "content": GREETING}])
    # Summarise each block of the reply: a tool request, or plain text.
    kinds = [f"tool_use:{b.name}({b.input})" if b.type == "tool_use" else "text" for b in r.content]
    # Print the setting, why Claude stopped, and what the reply contained.
    print(f"  {label:28} -> stop_reason={r.stop_reason}; blocks={kinds}")
# Now force the price tool on a question that is about a REGION, to show the wrong-input trap.
r = client.messages.create(model=MODEL, max_tokens=300, tools=CORE, tool_choice={"type": "tool", "name": "get_weave_price"},
                           # The conversation: a region question.
                           messages=[{"role": "user", "content": "Which weaves come from Tamil Nadu?"}])
# Print which tools were requested and with what input.
print(f"  forced get_weave_price, but the question is about a REGION -> {[(b.name, b.input) for b in r.content if b.type == 'tool_use']}\n")

# Part C heading.
print("=== PART C: a role that does not have the contact tool ===")
# Build a tool list that leaves out the contact tool (least privilege).
CHATBOT_ROLE = [x for x in CORE if x["name"] != "get_weaver_contact"]
# Ask for a phone number to a role that has no tool for it.
r = client.messages.create(model=MODEL, max_tokens=300, tools=CHATBOT_ROLE,
                           # The conversation: a request for a phone number.
                           messages=[{"role": "user", "content": "What is the phone number of weaver w2?"}])
# Print the tools this role has.
print(f"  tools this role has: {[x['name'] for x in CHATBOT_ROLE]}")
# Print why Claude stopped and the first 300 characters of its reply.
print(f"  stop_reason={r.stop_reason}; reply: {''.join(b.text for b in r.content if b.type == 'text')[:300]}")

# ---------------------------------------------------------------------------
# OUTPUT (a real run on 3 Nov 2026)
# === PART A: 4 tools versus 18 tools ===
#   [4 tools] Which weaves come from Tamil Nadu?  -> 10/10 correct
#   [4 tools] How much does a chanderi saree cost?  -> 10/10 correct
#   [4 tools] What material is jamdani made of?  -> 10/10 correct
#   [4 tools] overall 30/30 correct; input size per request: about 734 tokens
#
#   [18 tools] Which weaves come from Tamil Nadu?  -> 10/10 correct
#   [18 tools] How much does a chanderi saree cost?  -> 10/10 correct
#   [18 tools] What material is jamdani made of?  -> 10/10 correct
#   [18 tools] overall 30/30 correct; input size per request: about 1974 tokens
#
# === PART B: tool_choice ===
#   auto (Claude decides)        -> stop_reason=end_turn; blocks=['text']
#   any (must call some tool)    -> stop_reason=tool_use; blocks=["tool_use:list_weaves_by_region({'query': 'India'})"]
#   forced get_weave_price       -> stop_reason=tool_use; blocks=["tool_use:get_weave_price({'query': 'jamdani'})"]
#   forced get_weave_price, but the question is about a REGION -> [('get_weave_price', {'query': 'Tamil Nadu'}), ('list_weaves_by_region', {'query': 'Tamil Nadu'})]
#
# === PART C: a role that does not have the contact tool ===
#   tools this role has: ['list_weaves_by_region', 'get_weave_details', 'get_weave_price']
#   stop_reason=end_turn; reply: I can't look that up. My tools only cover handloom weaves ... None of them include weaver contact details. ...
#
# How to read it: Part A: accuracy was the same (30/30) with 4 or 18 tools, but the 18-tool request was about 2.7 times bigger (1974 vs 734 tokens),
# so the cost of bloat here was tokens, not accuracy. Part B: "auto" answered in text; "any" still had to call a tool for a greeting;
# forcing the price tool on a greeting made Claude invent the input 'jamdani', and forcing it on a region question passed 'Tamil Nadu' as a weave name (a forced call with a wrong input).
# Part C: with no contact tool, the phone number could not leak, and no hook was needed for that path.
