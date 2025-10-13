# braintrust eval을 실행하면 결과를 터미널에 기록
# Reporter를 사용하면  사용자 정의 리포터 사용 가능

# 다시 볼것 wip

import os
from dotenv import load_dotenv
import json
 
from braintrust import Reporter
from braintrust.framework import report_failures

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


def report_eval(evaluator, result, opts):
    # # 단일 리포터의 결과를 요약하고 원하는 대로 반환합니다(전체 결과, 텍스트 일부 또는 둘 다!).
    pass
 
 
def report_run(results):
    # 모든 결과를 취해 요약합니다. 프로세스 종료를 알리는 참 또는 거짓을 반환합니다.
    return True
 
 
# Reporter(
#     "My reporter",  # Replace with your reporter name
#     report_eval=report_eval,
#     report_run=report_run,
# )

Reporter(
    "default",
    report_eval=report_eval,
    report_run=report_run,
)

#평가 대상 파일에 포함된 모든 리포터는 braintrust eval 명령에 의해 자동으로 선택됩니다.

#리포터가 정의되지 않은 경우, 결과를 콘솔에 기록하는 기본 리포터가 사용됩니다.
#하나의 리포터를 정의하면 모든 Eval 블록에 적용됩니다.
#여러 리포터를 정의한 경우, Eval()의 선택적 세 번째 인수로 리포터 이름을 지정해야 합니다.