# 오류 발생 테스트 케이스에 대한 score 처리
# 기본적으로 예외를 발생시키는 eval 작업이나 점수 계산기는 점수 값을 생성하지 않습니다. 
# 이는 오류 발생 테스트 케이스가 없는 경우보다 계산된 종합 점수가 더 높게 표시될 수 있음을 의미합니다. 
# 이 동작을 변경하려면 Eval 호출에 처리되지 않은 점수 함수를 전달할 수 있습니다. 
# 성공적으로 완료되지 않은 모든 점수에 대해 0% 값을 기록하는 기본 처리기를 제공합니다.

# 확인요
# from autoevals import Factuality
# from braintrust import Eval, frameworks

# def error_task(input):
#     raise Exception("Task error")

# Eval(
#     name="Say Hi Bot",
#     data=lambda: [{
#         "input": "foo",
#     }],
#     task=error_task,
#     scores=[Factuality],
#     error_score_handler=frameworks.default_error_score_handler, # 커스텀 함수 변경가능
# )
