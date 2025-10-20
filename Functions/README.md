# Functions
Braintrust functions는 AI 관련 로직을 실행하기 위한 원자적이고 재사용 가능한 빌딩 블록입니다.   
Functions는 고성능 서버리스 환경에서 호스팅·원격 실행되며, 프로덕션 사용을 전제로 설계되었습니다.   
Functions는 API, SDK, UI를 통해 호출할 수 있고, 스트리밍 및 구조적 출력(Structured Output)을 기본 지원합니다.

function은 현재 4가지가 있습니다.
- Prompts: LLM에 전송할 템플릿 메시지
- Tools: LLM이 호출할 수 있는 범용 코드
- Scorers: LLM 출력 품질을 0~1 점수로 평가하는 함수
- Agents: 두 개 이상의 프롬프트를 체인으로 연결하는 도구

### Composability
functions를 조합해 정교한 어플리케이션을 만들수 있습니다.

모든 function은 툴처럼 사용할 수 있으며, 호출된 결과를 채팅 히스토리에 추가할 수 있습니다.  
예를 들어, RAG 에이전트는 단 두 구성요소로 정의할 수 있습니다:



```python
def query_vector_db(query, top_k):
    embedding_response = await openai.Embedding.create(input=query, model="text-embedding-3-small")
    embedding = embedding_response["data"][0]["embedding"]

    query_response = pc.query(vector=embedding, top_k=top_k, include_metadata=True)

    results = [
        {"title": match.get("metadata", {}).get("title"), "content": match.get("metadata", {}).get("content")}
        for match in query_response["matches"]
    ]

    return results
```

툴을 사용해 콘텐츠를 검색·합성하는 방법에 대한 지시를 담은 시스템 프롬프트
```
import braintrust
 
project = braintrust.projects.create(name="Doc Search")
 
project.prompts.create(
    name="Doc Search",
    slug="document-search",
    description="Search through the Braintrust documentation to answer the user's question",
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that can answer questions about the Braintrust documentation.",
        },
        {"role": "user", "content": "{{{question}}}"},
    ],
    tools=[toolRAG],
)

```

