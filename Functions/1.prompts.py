
import os
from dotenv import load_dotenv
import braintrust

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


project = braintrust.projects.create(name = "Summarizer") # 기존 프로젝트 가져오는 방법은?

summarizer = project.prompts.create(
    name = "Summarizer", 
    slug = "summarizer",
    description= "Summarize text",
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can summarize text."},
        {"role": "user", "content": "{{{text}}}"},
    ],
)
# 다음 명령으로 프롭프트 업로드 가능: braintrust push summarizer.py


## tools도 추가 가능
import braintrust
 
project = braintrust.projects.create(name="RAG app")
 
# doc_search = project.prompts.create(
#     name="Doc Search",
#     slug="document-search",
#     description="Search through the Braintrust documentation to answer the user's question",
#     model="gpt-4o-mini",
#     messages=[
#         {
#             "role": "system",
#             "content": (
#                 "You are a helpful assistant that can " + "answer questions about the Braintrust documentation."
#             ),
#         },
#         {
#             "role": "user",
#             "content": "{{{question}}}",
#         },
#     ],
#     tools=[tool_rag],
# )
