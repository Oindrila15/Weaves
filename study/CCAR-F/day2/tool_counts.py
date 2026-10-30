"""Day 2, lesson 3: how many tools, which tools, and tool_choice (exam topic 2.3).

Part A: the same questions with 4 tools versus 18 tools (accuracy and input size).
Part B: the three tool_choice settings.
Part C: a role that simply does not have the dangerous tool.
Tools are never run; we only look at what Claude asks for.
"""
from collections import Counter
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
RUNS = 10


def t(name, desc, arg="query"):
    return {"name": name, "description": desc,
            "input_schema": {"type": "object", "properties": {arg: {"type": "string"}}, "required": [arg]}}


# --- the four tools Weaves actually needs for these questions -----------------
CORE = [
    t("list_weaves_by_region", "List the names of handloom weaves traditionally made in one Indian state. Input: a state name such as 'Tamil Nadu'. Names only. Not for questions about one named weave."),
    t("get_weave_details", "Get the region and material of ONE named weave, such as 'jamdani'. Not for prices and not for finding weaves by place."),
    t("get_weave_price", "Get the typical price range in INR for ONE named weave, such as 'jamdani'. Use only for price questions."),
    t("get_weaver_contact", "Get a weaver's contact details by weaver id such as 'w1'. Shown only with the weaver's consent."),
]
# --- fourteen more tools that are each a real, different job -----------------
EXTRA = [
    t("get_weave_history", "Get a short history of ONE named weave, such as 'banarasi'. Not for prices or materials."),
    t("get_weave_price_trends", "Get how the price of ONE named weave has changed over the past years. Not for today's price range."),
    t("compare_weaves", "Compare two named weaves side by side. Input: two names separated by a comma."),
    t("get_gi_tag_status", "Check whether ONE named weave has a Geographical Indication (GI) tag."),
    t("get_care_instructions", "Get washing and storage care instructions for ONE named weave."),
    t("get_drape_styles", "Get regional draping styles for sarees. Input: a state name."),
    t("find_festival_sarees", "Suggest weaves traditionally worn for a named festival, such as 'Onam'."),
    t("get_dye_methods", "Get the traditional dyeing methods used for ONE named weave."),
    t("get_loom_type", "Get the type of loom used for ONE named weave."),
    t("list_weaver_cooperatives", "List weaver cooperatives in a named state."),
    t("get_authenticity_checks", "Get tips for checking whether a saree of a named weave is genuine."),
    t("get_museum_collections", "List museums that hold textiles of ONE named weave."),
    t("get_buying_guide", "Get general advice for first-time saree buyers. Input: a budget in INR."),
    t("get_weaver_story", "Get the public profile story of a weaver by weaver id such as 'w1'. No contact details."),
]
BIG = CORE + EXTRA

QUESTIONS = [
    ("Which weaves come from Tamil Nadu?", {"list_weaves_by_region"}),
    ("How much does a chanderi saree cost?", {"get_weave_price"}),
    ("What material is jamdani made of?", {"get_weave_details"}),
]


def first_tool(tools, q):
    r = client.messages.create(model=MODEL, max_tokens=300, tools=tools,
                               messages=[{"role": "user", "content": q}])
    name = next((b.name for b in r.content if b.type == "tool_use"), "(no tool)")
    return name, r.usage.input_tokens


print("=== PART A: 4 tools versus 18 tools ===")
for label, tools in [("4 tools", CORE), ("18 tools", BIG)]:
    total_ok, total, tokens = 0, 0, 0
    for q, right in QUESTIONS:
        picks = Counter()
        for _ in range(RUNS):
            name, tok = first_tool(tools, q)
            picks[name] += 1
            tokens = tok          # input tokens per call (the same each time)
        ok = sum(n for name, n in picks.items() if name in right)
        total_ok += ok; total += RUNS
        print(f"  [{label}] {q}  -> {ok}/{RUNS} correct  {dict(picks) if ok < RUNS else ''}")
    print(f"  [{label}] overall {total_ok}/{total} correct; input size per request: about {tokens} tokens\n")

print("=== PART B: tool_choice ===")
GREETING = "Hi! What can you help me with?"
for label, choice in [("auto (Claude decides)", {"type": "auto"}),
                      ("any (must call some tool)", {"type": "any"}),
                      ("forced get_weave_price", {"type": "tool", "name": "get_weave_price"})]:
    r = client.messages.create(model=MODEL, max_tokens=300, tools=CORE, tool_choice=choice,
                               messages=[{"role": "user", "content": GREETING}])
    kinds = [f"tool_use:{b.name}({b.input})" if b.type == "tool_use" else "text" for b in r.content]
    print(f"  {label:28} -> stop_reason={r.stop_reason}; blocks={kinds}")
r = client.messages.create(model=MODEL, max_tokens=300, tools=CORE, tool_choice={"type": "tool", "name": "get_weave_price"},
                           messages=[{"role": "user", "content": "Which weaves come from Tamil Nadu?"}])
print(f"  forced get_weave_price, but the question is about a REGION -> {[(b.name, b.input) for b in r.content if b.type == 'tool_use']}\n")

print("=== PART C: a role that does not have the contact tool ===")
CHATBOT_ROLE = [x for x in CORE if x["name"] != "get_weaver_contact"]
r = client.messages.create(model=MODEL, max_tokens=300, tools=CHATBOT_ROLE,
                           messages=[{"role": "user", "content": "What is the phone number of weaver w2?"}])
print(f"  tools this role has: {[x['name'] for x in CHATBOT_ROLE]}")
print(f"  stop_reason={r.stop_reason}; reply: {''.join(b.text for b in r.content if b.type == 'text')[:300]}")
