# Braintrust의 Tool functions는 LLM이 호출하여 워크플로우에 복잡한 로직이나 외부 연산을 추가할 수 있는 범용 코드를 정의하게 해줍니다. 
# Tools는 재사용 가능하고 조합 가능하여, 어시스턴트형 에이전트부터 더 고도화된 애플리케이션까지 쉽게 반복·개선할 수 있습니다. 
# 툴을 만들고, 프롬프트를 통해 UI와 API 전반에 배포할 수 있습니다.


import os
from dotenv import load_dotenv
import braintrust
import requests
from typing import Literal
from pydantic import BaseModel, RootModel

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

# 툴생성
class CalculatorInput(BaseModel):
    op: Literal["add", "subtract", "multiply", "divide"]
    a: float
    b: float

class CalculatorOutput(RootModel[float]):
    pass
 
 
def calculator(op, a, b):
    match op:
        case "add":
            return a + b
        case "subtract":
            return a - b
        case "multiply":
            return a * b
        case "divide":
            return a / b
 
project = braintrust.projects.create(name="Tools App")
 
project.tools.create(
    handler=calculator,
    name="Calculator method",
    slug="calculator-2",
    description="A simple calculator that can add, subtract, multiply, and divide.",
    parameters=CalculatorInput,  # You can also provide raw JSON schema here if you prefer
    returns=CalculatorOutput,
)
