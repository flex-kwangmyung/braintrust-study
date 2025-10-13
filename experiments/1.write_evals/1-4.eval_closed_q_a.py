# Closed qa 같은 특정 scorer는 추가적인 필드를 전달할수도 있고, partial로 초기화하여 전달할수도 있다.
import os
from dotenv import load_dotenv
from autoevals import ClosedQA, Score, EmbeddingSimilarity
from braintrust import Eval, wrap_openai
from openai import OpenAI

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


openai = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

Eval(
    name="QA Bot",
    data=lambda: [
        {
            "input": "Which insect has the highest population?",
            "expected": "ant",
        },
    ],
    task=lambda input: openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Answer the following question."},
            {"role": "user", "content": "Question: " + input},
        ],
    )
    .choices[0]
    .message.content
    or "Unknown",
    scores=[
        ClosedQA.partial(criteria="Does the submission specify whether or not it can confidently answer the question?")
    ],
)


# criteria가 dynimic 이라면 래퍼 사용 가능

def closed_q_a(input, output, metadata):
    # 인수를 직접 전달 하기 전에 클래스 인스턴스화가 필요함
    return ClosedQA()(
        input=input,
        output=output,
        criteria=metadata["criteria"],
    )
 

Eval(
    "QA bot",
    data=lambda: [
        {
            "input": "Which insect has the highest population?",
            "expected": "ant",
            "metadata": {
                "criteria": "Does the submission specify whether or not it can confidently answer the question?",
            },
        },
    ],
    task=lambda input: openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Answer the following question. Specify how confident you are (or not)",
            },
            {"role": "user", "content": "Question: " + input},
        ],
    )
    .choices[0]
    .message.content
    or "Unknown",
    scores=[closed_q_a],
)


########### Composing scorers
# 다른 scorer를 호출하는 scorer를 만들 때...???

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def translation_score(input, output): # 번역기 앱을 평가하기 위해서, 역번역을 하여 임베딩 유사도 평가
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates from French to English."},
            {"role": "user", "content": output},
        ],
    )
    reverse_translated = completion.choices[0].message.content
    similarity = EmbeddingSimilarity()(output=reverse_translated, expected=input)
    return Score(
        name="TranslationScore",
        score=similarity.score,
        metadata={"original": input, "translated": output, "reverseTranslated": reverse_translated},
    )


def task(input): # 영어 -> 프랑스어 번역
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates from English to French."},
            {"role": "user", "content": input},
        ],
    )
    return completion.choices[0].message.content

    
    
Eval(
    "Translate",
    data=[
        {"input": "May I order a pizza?"},
        {"input": "Where is the nearest bank?"},
    ],
    task=task,
    scores=[translation_score],
)
