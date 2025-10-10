import os
from dotenv import load_dotenv
from braintrust import init_logger, wrap_openai
from openai import OpenAI

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

logger = init_logger(project="OpenAI Tracing Test(stream=False)")
client = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# All API calls are automatically logged
result = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True,
    stream_options={"include_usage": True},  # Required for token metrics
)
 
for chunk in result:
    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
