# 트레이스 데이터를 수집하고 관리하는 방법을 조정하면, 
# 복잡한 프로세스를 더 잘 추적하고, 여러 서비스에 걸친 시스템을 모니터링하며, 
# 이슈를 더욱 효과적으로 디버깅할 수 있습니다.

# 데코레이트 사용하면 로그 적용 가능하다.

import os
from dotenv import load_dotenv

from braintrust import init_logger, traced, wrap_openai
from openai import OpenAI

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

logger = init_logger(project = "My KY Project")
client = wrap_openai(OpenAI())

# @traced는 이 함수의 입력(인자)과 출력(반환값)을 자동으로 하나의 스팬에 기록합니다.
# 스팬 이름을 `answer_question`으로 보장하려면,
# 함수 이름을 `answer_question`으로 지정하세요.

@traced(name = "kmyu trace1") # name 파라미터를 넣으면 span 이름을 지정할 수 있다.
def answer_question(body: str) -> str:
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": body},
    ]
 
    result = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt,
    )
    return result.choices[0].message.content



def main():
    input_text = "How can I improve my productivity?"
    result = answer_question(input_text)
    print(result)


if __name__ == "__main__":
    main()