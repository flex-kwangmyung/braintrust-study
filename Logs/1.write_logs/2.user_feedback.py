
import os
from dotenv import load_dotenv
from braintrust import init_logger, traced, wrap_openai
from openai import OpenAI
from types import SimpleNamespace

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


# simple api에  feedback을 로깅하는 방법
logger = init_logger(project="My KY Project")
 
client = wrap_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
 
 
@traced
def some_llm_function(input):
    return client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Classify the following text as a question or a statement.",
            },
            {
                "role": "user",
                "content": input,
            },
        ],
        model="gpt-4o",
    )


def my_route_handler(req):
    with logger.start_span() as span:
        body = req.body
        result = some_llm_function(body)
        span.log(input=body, output=result)
        return {
            "result": result,
            "request_id": span.id,
        }


# Assumes that the request is a JSON object with the requestId generated
# by the previous POST request, along with additional parameters like
# score (should be 1 for thumbs up and 0 for thumbs down), comment, and userId.
def my_feedback_handler(req):
    logger.log_feedback(
        id=req.body.request_id,
        scores={
            "correctness": req.body.score,
        },
        comment=req.body.comment,
        metadata={
            "user_id": req.user.id,
        },
    )


def main():
    # 1. LLM 호출
    print("\n=== LLM 호출 및 로깅 ===")
    test_input = "What is the capital of France?"

    req = type('obj', (object,), {'body': test_input})()
    response = my_route_handler(req)

    print(f"입력: {test_input}")
    print(f"결과: {response['result'].choices[0].message.content}")
    print(f"Request ID: {response['request_id']}")

    # 2. 피드백 로깅
    print("\n=== 사용자 피드백 로깅 ===")
    feedback_req = type('obj', (object,), {
        'body': type('obj', (object,), {
            'request_id': response['request_id'],
            'score': 1,  # 1 = thumbs up, 0 = thumbs down
            'comment': "답변이 정확하고 도움이 되었습니다!"
        })(),
        'user': type('obj', (object,), {'id': 'user_12345'})()
    })()

    my_feedback_handler(feedback_req)
    print(f"피드백 로깅 완료: score=1 (thumbs up), user_id=user_12345")


if __name__ == "__main__":
    main()
