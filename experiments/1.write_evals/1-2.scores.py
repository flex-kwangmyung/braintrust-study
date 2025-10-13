# scoring function을 사용하면 작업의 예상 출력과 실제 출력을 비교하여 0과 1 사이의 점수를 산출할 수 있음. 
# scoring function은는 eval의 scores 리스트에서 참조하여 사용

# Braintrust의 autoevals 라이브러리가 제공하는 스코어러로 시작하는 것을 권장. 
# 이를 통해 사용 사례에 맞춤화된 자체 스코어러를 생성하여 애플리케이션 성능에 대한 균형 잡힌 관점을 확보할 수 있음

import os
from dotenv import load_dotenv
from autoevals import Factuality, LLMClassifier
from braintrust import Eval

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


########## Define your own scorers
def exact_match(input: str, output: str, expected: str, **kwargs) -> int:
    return 1 if output == expected else 0

Eval(
    "Say Hi Bot",
    data=lambda: [
        {
            "input": "David",
            "expected": "Hi David",
        },
    ], 
    task=lambda input: "Hi " + input,
    scores=[exact_match],
)

########## Scoring using AI (LLM judge)
# 사용자 커스터마이징된 프롬프트 기반의 scoring function

no_apology = LLMClassifier( # default model: gpt-4o
    name ="No apology",
    prompt_template="Does the response contain an apology? (Y/N)\n\n{{output}}",
    choice_scores={"Y": 0, "N": 1},
    use_cot=True,
)

Eval(
    "Say Hi Bot",  # Replace with your project name
    data=lambda: [
        {
            "input": "David",
            "expected": "Hi David",
        },
    ],  # Replace with your eval dataset
    task=lambda input: "Sorry " + input,  # Replace with your LLM call
    scores=[no_apology],
)

########## Conditional scoring
# scoring function은 입력 데이터에 따라 달라질 수 있음. 예를 들어, 챗봇을 평가할 때는 계산기 스타일의 입력이 올바르게 답변되었는지 측정하는 점수 함수를 사용하고자 할 수 있음

from autoevals import NumericDiff

def caculator_accuracy(input, output, **kwargs):
    if input["type"] != "calculator":
        return None
    
    return NumericDiff(output, eval(input["text"]))

