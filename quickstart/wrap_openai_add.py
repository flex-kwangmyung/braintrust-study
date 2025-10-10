# openai wrapper의 추가 기능 설명
# https://www.braintrust.dev/docs/providers/openai

import os
from dotenv import load_dotenv
from braintrust import init_logger, wrap_openai
from openai import OpenAI
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")

client = wrap_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))


completion = client.beta.chat.completions.parse(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": "Extract the person's name and age."},
        {"role": "user", "content": "My name is John and I'm 30 years old."},
    ],
    response_format=Person,
)

# 파싱된 결과 출력
parsed_result = completion.choices[0].message.parsed
print("=== 파싱된 결과 ===")
print(f"이름: {parsed_result.name}")
print(f"나이: {parsed_result.age}")
print(f"전체 객체: {parsed_result}")

# 일반적인 채팅 응답 출력 예제
print("\n=== 일반 채팅 응답 예제 ===")
chat_response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "user", "content": "안녕하세요! 간단한 인사말을 해주세요."}
    ],
)
print(f"응답: {chat_response.choices[0].message.content}")

# function calling 지원
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                },
                "required": ["location"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
    tools=tools,
)

# Function calling 결과 출력
print("\n=== Function Calling 결과 ===")
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for tool_call in tool_calls:
        print(f"함수명: {tool_call.function.name}")
        print(f"인수: {tool_call.function.arguments}")
        print(f"ID: {tool_call.id}")
else:
    print("도구 호출이 없습니다.")
    print(f"응답 내용: {response.choices[0].message.content}")