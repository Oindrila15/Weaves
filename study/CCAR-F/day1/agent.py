"""Day 1: a tool-using agent. The loop follows stop_reason (exam topic 1.1).

All data below is made-up sample data for learning, not real weaver facts.
"""
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"

# --- Sample data -----------------------------------------------------------
WEAVES = {
    "kanchipuram": {"region": "Tamil Nadu", "material": "pure mulberry silk, zari", "price_inr": [15000, 150000]},
    "banarasi": {"region": "Uttar Pradesh", "material": "silk, brocade", "price_inr": [8000, 100000]},
    "jamdani": {"region": "West Bengal", "material": "fine cotton", "price_inr": [3000, 40000]},
    "chanderi": {"region": "Madhya Pradesh", "material": "silk-cotton", "price_inr": [2500, 20000]},
}
WEAVERS = {
    "w1": {"weave": "jamdani", "name": "Sample Weaver A", "consent": True, "phone": "000-000-0001"},
    "w2": {"weave": "chanderi", "name": "Sample Weaver B", "consent": False, "phone": "000-000-0002"},
}

# --- Tools: plain Python functions Claude can ask us to run -----------------
def search_weaves_by_region(region):
    hits = [n for n, w in WEAVES.items() if region.lower() in w["region"].lower()]
    return {"weaves": hits}

def get_weave_details(weave):
    w = WEAVES.get(weave.lower())
    return w if w else {"error": f"No weave named {weave}"}

def get_price_range(weave):
    w = WEAVES.get(weave.lower())
    return {"weave": weave, "price_inr": w["price_inr"]} if w else {"error": f"No weave named {weave}"}

def get_weaver_contact(weaver_id):
    w = WEAVERS.get(weaver_id)
    if not w:
        return {"error": "No such weaver"}
    return {"name": w["name"], "phone": w["phone"]}  # NOTE: ignores consent on purpose; the hook will fix this

TOOL_FUNCS = {
    "search_weaves_by_region": search_weaves_by_region,
    "get_weave_details": get_weave_details,
    "get_price_range": get_price_range,
    "get_weaver_contact": get_weaver_contact,
}

# --- Tool descriptions: what Claude reads to decide which tool to use -------
TOOLS = [
    {"name": "search_weaves_by_region",
     "description": "List handloom weaves traditionally made in a state or region. Use when the user names a place and wants to know which weaves come from there.",
     "input_schema": {"type": "object", "properties": {"region": {"type": "string"}}, "required": ["region"]}},
    {"name": "get_weave_details",
     "description": "Get region and material for one named weave. Use for questions about what a weave is made of or where it is from.",
     "input_schema": {"type": "object", "properties": {"weave": {"type": "string"}}, "required": ["weave"]}},
    {"name": "get_price_range",
     "description": "Get the typical price range in INR for one named weave. Use only for price questions.",
     "input_schema": {"type": "object", "properties": {"weave": {"type": "string"}}, "required": ["weave"]}},
    {"name": "get_weaver_contact",
     "description": "Get a weaver's contact details by weaver id (like w1). Contact details are shown only with the weaver's consent.",
     "input_schema": {"type": "object", "properties": {"weaver_id": {"type": "string"}}, "required": ["weaver_id"]}},
]

# --- The agentic loop -------------------------------------------------------
def run_agent(question):
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=1000, tools=TOOLS, messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})
        print(f"[stop_reason = {response.stop_reason}]")

        if response.stop_reason == "end_turn":      # Claude is done: stop
            return "".join(b.text for b in response.content if b.type == "text")

        if response.stop_reason == "tool_use":      # Claude wants tools: run them
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  tool call: {block.name}({block.input})")
                    output = TOOL_FUNCS[block.name](**block.input)
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    "content": json.dumps(output)})
            messages.append({"role": "user", "content": results})
            continue                                # send results back, go round again

        raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")

if __name__ == "__main__":
    print(run_agent("Which weaves come from West Bengal, and what is the price range of the one you find?"))
