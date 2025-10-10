from mimetypes import guess_type
import os
from dotenv import load_dotenv
from braintrust import Eval
# from autoevals import LLMClassifierFromSpec
from openai import OpenAI

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def task(input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": input}],
    )
    return response.choices[0].message.content

def accuracy_scorer(output: str, expected: str, **kwargs) -> int:
    return 1 if output == expected else 0


# # LLMClassifier: LLM as a judge, 현재 사용불가, 확인요
# relevance_scorer = LLMClassifierFromSpec(
#     spec="Relevance",
#     choices={"Relevant": 1, "Irrelevant": 0},
#     model="gpt-4o-mini",
#     use_cot= True,
# )


Eval(
    name = "OpenAI Evaluation",
    data=[
        {"input": "What is 2+2?", "expected": "4"},
        {"input": "What is the capital of France?", "expected": "Paris"},
    ],
    task=task,
    scores=[accuracy_scorer],
)