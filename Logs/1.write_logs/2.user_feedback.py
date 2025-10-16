
import os
from dotenv import load_dotenv
from braintrust import init_logger, traced, wrap_openai
from openai import OpenAI
from urllib3 import response

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


