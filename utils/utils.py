from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
# from google import genai
import google.generativeai as genai

# from google import genai
import asyncio
import json
import sys
import os
import re

load_dotenv()

api_key = os.getenv("api_key")
model = os.getenv("model")

# llm = ChatOpenAI(api_key=api_key, model=model)
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model)  # Or "gemini-1.5-pro" etc.

# print(response.text)


# client = genai.Client(api_key=api_key)

# print(response.text)

def callLLM(prompt: str):
    # res = lm.invoke(prompt)
    # response = client.models.generate_content(
    #     model=model,
    #     contents=prompt
    # )
    response = model.generate_content(prompt)
    
    print("response.text: ", response.text)
    try:
        match = re.search(r"<output>(.*?)</output>", response.text, re.DOTALL | re.IGNORECASE)
        if match:
            output_content = match.group(1).strip()
            print("Extracted content:\n", output_content)
            return output_content
        else:
            return "Unable to process LLM output found"
    except Exception as e:
        # log_exception(e, "get_content")
        return f"Error occurred while fetching the required output from LLM response: {e}"
