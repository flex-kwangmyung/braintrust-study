from autoevals import Levenshtein
from braintrust import Eval
from dotenv import load_dotenv
import os

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

Eval(
    "Say Hi Bot",  # Replace with your project name
    data=lambda: [
        {
            "input": "Foo",
            "expected": "Hi Foo",
        },
        {
            "input": "Bar",
            "expected": "Hi Bar",
        },
    ],  # Replace with your eval dataset
    task=lambda input: "Hi " + input,  # Replace with your LLM call
    scores=[Levenshtein],
)