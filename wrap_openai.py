import os
from dotenv import load_dotenv
from braintrust import init_logger, wrap_openai
from openai import OpenAI

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

logger = init_logger(project="OpenAI Tracing Test")
client = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# All API calls are automatically logged
result = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"},
    ],
)
print(result)