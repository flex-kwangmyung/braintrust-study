# 자체 클라이언트를 사용하는 래퍼를 경우, OpenAI 래퍼와 동일한 규칙으로 직접 래핑할 수 있습니다.

# 커스텀으로 스팬을 LLM으로 추적하려면 다음을 수행해야 합니다:

# type을 llm으로 지정하세요. name은 임의로 지정할 수 있습니다. 이 설정은 LLM 지속시간(metrics) 수집을 활성화합니다.
# metrics 필드에 prompt_tokens, completion_tokens, tokens를 추가하세요. 이 설정은 LLM 토큰 사용량 메트릭을 활성화합니다.
# 캐시된 토큰을 추적하려면 prompt_cached_tokens(캐시 읽기)와 prompt_cache_creation_tokens(캐시 쓰기)를 metrics에 기록할 수 있습니다. 
# 관례상 prompt_tokens는 prompt_cached_tokens와 prompt_cache_creation_tokens를 포함해야 합니다. 
# 예를 들어, 캐시 읽기 10, 캐시 쓰기 5, 비캐시 3이라면 prompt_tokens: 18을 기록해야 합니다.
# input은 메시지 리스트(OpenAI 포맷)를 사용하고, model 같은 다른 파라미터는 metadata에 넣으세요. 이렇게 하면 UI의 “Try prompt” 버튼이 활성화됩니다.

import os
from dotenv import load_dotenv

from braintrust import init_logger,current_span, start_span, traced
from openai import OpenAI

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

logger = init_logger(project = "My KY Project")
#client = wrap_openai(OpenAI())

def call_my_llm(input: str, params: dict) -> dict:
    # Replace with your custom LLM implementation
    return {
        "completion": "Hello, world!",
        "metrics": {
            "prompt_tokens": len(input),
            "completion_tokens": 10,
        },
    }

# notrace_io=True는 함수 인자를 입력으로 자동 기록하지 않도록 하며,
# 더 구체적인 입력 포맷을 수동으로 기록할 수 있게 해줍니다.
@traced(type="llm", name="Custom LLM", notrace_io=True)
def invoke_custom_llm(llm_input: str, params: dict):
    result = call_my_llm(llm_input, params)
    content = result["completion"]
    current_span().log(
        input=[{"role": "user", "content": llm_input}],
        output=content,
        metrics=dict(
            prompt_tokens=result["metrics"]["prompt_tokens"],
            completion_tokens=result["metrics"]["completion_tokens"],
            tokens=result["metrics"]["prompt_tokens"] + result["metrics"]["completion_tokens"],
        ),
        metadata=params,
    )
    return content
 
 
def my_route_handler(req):
    with start_span() as span:
        result = invoke_custom_llm(
                llm_input=req.body,
                params=dict(temperature=0.1),
        )
        span.log(input=req.body, output=result)
        return result


def main():
    # invoke_custom_llm 함수를 테스트하는 예제
    input_text = "What is the meaning of life?"
    params = {
        "temperature": 0.7,
        "model": "custom-llm-v1",
        "max_tokens": 100,
    }

    print("=== Testing invoke_custom_llm ===")
    print(f"Input: {input_text}")
    print(f"Params: {params}")

    result = invoke_custom_llm(llm_input=input_text, params=params)

    print(f"Output: {result}")
    print("\n결과가 Braintrust에 로깅되었습니다.")
    print("Braintrust UI에서 확인하세요: https://www.braintrust.dev")



if __name__ == "__main__":
    main()