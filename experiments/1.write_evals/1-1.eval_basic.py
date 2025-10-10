# Eval() 함수로 Braintrust 프로젝트에 새로운 실험을 생성가능
# 단일 파일 내에 여러 개의 eval 문이 존재할 수 있음

# 첫 번째 인자는 프로젝트 이름(name)이며, 나머지 인수를 통해 다음을 지정할 수 있습니다:

# data: 평가 데이터셋을 반환하는 함수. 입력값, 예상 출력값(선택 사항), 메타데이터 목록으로 구성.
# task: 단일 입력을 받아 LLM 완성처럼 출력을 반환하는 함수
# scores: 입력, 출력, 예상 출력(선택 사항)을 받아 점수를 반환하는 점수 함수 집합
# metadata: 사용 중인 모델이나 구성 값과 같은 실험에 대한 메타데이터
# experiment_name: 실험에 사용할 이름. 이 이름이 이미 존재하면 Braintrust가 자동으로 고유한 접미사를 추가.

# Eval()의 반환값에는 평가의 전체 결과와 함께 평균 점수, 소요 시간, 개선 사항, 퇴보 사항 및 기타 지표를 확인할 수 있는 요약 정보가 포함됨

import os
from dotenv import load_dotenv
from autoevals import Factuality
from braintrust import Eval

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

Eval(
    "Say Hi Bot",  # Replace with your project name
    data=lambda: [
        {
            "input": "David",
            "expected": "Hi David",
        },
    ],  # Replace with your eval dataset
    task=lambda input: "Hi " + input,  # Replace with your LLM call
    scores=[Factuality],
)

