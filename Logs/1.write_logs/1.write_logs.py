
import os
from dotenv import load_dotenv
from braintrust import init_logger, traced, wrap_openai
from openai import OpenAI
from urllib3 import response

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


# 로거 초기화
logger = init_logger(project = "My KY Project")

client = wrap_openai(OpenAI())


@traced
def classify_text(input_text):
    # Call the OpenAI API to classify the text
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Classify the following text as a question or a statement.",
            },
            {
                "role": "user",
                "content": input_text,
            },
        ],
    )
    # Extract the classification from the response
    try:
        classification = response.choices[0].message.content.strip()
        return classification
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        return "Unable to classify the input."
 
 
def main():
    input_text = "Is this a question?"
    try:
        # Call the classify_text function and print the result
        result = classify_text(input_text)
        print("Classification:", result)
    except Exception as error:
        print("Error:", error)
 
 
if __name__ == "__main__":
    main()
    