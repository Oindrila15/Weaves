"""Day 1, step 0: check that the API key works with one tiny call."""
from dotenv import load_dotenv
import anthropic

load_dotenv()  # reads ANTHROPIC_API_KEY from the .env file
client = anthropic.Anthropic()  # finds the key by its name

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "In one short sentence, what is a handloom saree?"}],
)

print(response.content[0].text)
print("stop_reason:", response.stop_reason)
