from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
import json
import sys
import os
import re

load_dotenv()

api_key = os.getenv("api_key")
model = os.getenv("model")

llm = ChatOpenAI(api_key=api_key, model=model)
def callLLM(prompt: str):
    res = lm.invoke(prompt)
    # print("res: ", res)
    try:
        match = re.search(r"<output>(.*?)</output>", res.content, re.DOTALL | re.IGNORECASE)
        if match:
            output_content = match.group(1).strip()
            print("Extracted content:\n", output_content)
            return output_content
        else:
            return "Unable to process LLM output found"
    except Exception as e:
        # log_exception(e, "get_content")
        return f"Error occurred while fetching the required output from LLM response: {e}"
