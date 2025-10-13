# 예상되는 출력이 없어서 이전 실험을 베이스라인으로 사용할 경우
# 기본 벤치마크가 없을 때 유용
# 이전 실험의 output을 현재 실험의 expected로 사용
# Battle, Summary와 같은 내장 scorer로 힐클라이밍 적용 가능
# 힐클라이밍 사용위해 BaseExperiment 함수 사용

import os
from autoevals import Battle
from braintrust import Eval, BaseExperiment
from dotenv import load_dotenv

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


Eval(
    "Say Hi Bot",  # Replace with your project name
    data=BaseExperiment(),
    task=lambda input: "Hi " + input,  # Replace with your LLM call
    scores=[Battle.partial(instructions="Which response said 'Hi'?")],s
)

# 특정 실험을 사용하려면, name을 지정
# Eval(
#     "Say Hi Bot",  # Replace with your project name
#     data=BaseExperiment(name="main-123"),
#     task=lambda input: "Hi " + input,  # Replace with your LLM call
#     scores=[Battle.partial(instructions="Which response said 'Hi'?")],
# )