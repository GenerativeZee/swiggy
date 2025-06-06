from langgraph.graph import START, StateGraph, END
from fastapi.responses import JSONResponse
from typing import TypedDict, List, Dict
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from utils.utils import callLLM
from pydantic import BaseModel
from fastapi import FastAPI
import requests

app = FastAPI()

class State(TypedDict):
    query: str
    intent_catogory: str
    key_entities: List[str]
    confidence_score: str  # how confident LLM is in categorizing the request into a category
    follow_up_questions: List[str] # When info is missing/ambiguous

def get_intent_category(state: State):
    try:
        prompt = """You are an AI assistant whose job is to understand the user's request and produce an 'intent label'. This label should summarize what the user wants. Intent can be anything and below are the few examples:
        - 'Need a sunset-view table for the two tonight' -> 'dining_reservation'
        - 'Book me a cab from home to ariport in 30 minutes' -> 'cab_booking'
        - 'Find me gluten-free gift ideas under 1000 INR' -> 'gifting_ideas'
        - 'Show me upcoming rock concerts in Mumbai' -> 'event_search'
        - 'I want to plan a trip to Goa next month -> 'travel_planning'
        - etc.
        
        **Input:**
        
        ```
        **user's request:** {}
        ```
        
        **Instructions*:**
        1. Understand given user's request.
        2. output the intent of the user's request.
        3. If the request does not fit into a standard category (dining, travel, gifting, cab_booking) create a new, intent_label like 'other_action_desired' (try to be as specific as possible e.f., "download_document", "password reset", "concert search", etc.).
        
        **Output Format:** Enclose the final output within `<output>...</output>` tags."""
        
        prompt = prompt.format(state["query"])
        intent_by_llm = callLLM(prompt)
        return Command(update={"intent_catogory": intent_by_llm}, goto="get_key_entities")
    except Exception as e:
        return Command(update={"intent_catogory": f"error: {str(e)}"}, goto="get_key_entities")

def get_key_entities(state: State):
    try:
        prompt = """
        **Role:** You are an AI assistant that extracts **all relevant key-value entities** from a single user request. The intent label is already known (but you can ignore it if you like). Look at the raw input below and identify anything that might matter—dates, times, locations, party sizes, budgets, items, destinations, phone numbers, usernames, specific topics, etc.

        **Task:** Output all possible entities present in the user request.
    
        **Inputs:**
        ```
        user's request: {}
        ```
        
        ```
        intent: {}
        ```
        
        **Instruction:**
        - A single JSON object whose keys are each entities' name and whose values are the extracted value.
        - If a particular piece of information is not in the text, simply omit that key.
        - If you see a date like “tomorrow” or “tonight,” convert to ISO format (YYYY-MM-DD) if possible. If it’s ambiguous, you may keep the original wording (e.g., “tonight”).
    
        **Output Format:** Enclose the final output within `<output>...</output>` tags.
        """
        
        prompt = prompt.format(state["query"], state["intent_catogory"])
        key_entities = callLLM(prompt)
        return Command(update={"key_entities": key_entities}, goto="isInfoMissing")
    except Exception as e:
        return Command(update={"key_entities": [f"error: {str(e)}"]}, goto="isInfoMissing")

def get_confidence_score(state: State):
    try:
        prompt = """
        **Role:** You are an expert evaluator for evaluating the identified category by an AI assistant.
        
        **Task:** Given the user request and identified intent category from the user input, your task is to give it a score between 0 to 1. 0 being poor category classification 1 being best category classification.
        
        **Input:**
        ```
        User request: {}
        ```
        
        ```
        Identify Intent category: {}
        ```
        
        **Output Format:** Enclose the final output within `<output>...</output>` tags."""
        
        prompt = prompt.format(state["query"], state["intent_catogory"])
        confidence_score = callLLM(prompt)
        return Command(update={"confidence_score": confidence_score}, goto=END)
    except Exception as e:
        return Command(update={"confidence_score": f"error: {str(e)}"}, goto=END)

def isInfoMissing(state: State):
    try:
        prompt = """
        **Role:** You are an AI assistant that must decide whether the essential information is missing from the user's request or not.
        
        **Task:** Given the user's request, classified intent and extracted entities, your task is to check if any essential information is/are missing for fulfilling the user's request. 
        
        **Instructions:**
        1. Understand the user's request.
        2. Look at `intent: {}` and think of every possible entities related to this intent.
        3. If any of the required entities for the `intent: {}` are missing or have an empty/ambiguous values then formulate a polite follow-up question.  
        4. Check if any essential information is missing in the user's request.
        5. Output a list of follow-up questions for user for asking the missing information.
        6. Output follow-up questions without reasoing or explanations.
        
        **Input:**
        
        ```
        user's request: {}
        ```
        
        ```
        extracted entities: {}
        ```

        **Output Format:** Enclose the final output within `<output>...</output>` tags.
        
        **Example output:** <output>[follow-up 1, follow-up 1]</output>
        """
        
        prompt = prompt.format(state["intent_catogory"], state["intent_catogory"], state["query"], state["key_entities"])
        isMissing = callLLM(prompt)
        return Command(update={"follow_up_questions": isMissing}, goto="get_confidence_score")
    except Exception as e:
        return Command(update={"follow_up_questions": [f"error: {str(e)}"]}, goto="get_confidence_score")


class RequestBody(BaseModel):
    query: str

graph = StateGraph(State)
graph.add_edge(START, "get_intent_category")
graph.add_node("get_intent_category", get_intent_category)
graph.add_node("get_key_entities", get_key_entities)
graph.add_node("isInfoMissing", isInfoMissing)
graph.add_node("get_confidence_score", get_confidence_score)

worker = graph.compile()

@app.post("/response")
def chat(request: RequestBody):
    try:
        state_input = {
            "query": request.query,
            "intent_catogory": "",
            "key_entities": [],
            "confidence_score": "",
            "follow_up_questions": []
        }

        state = worker.invoke(state_input)

        return JSONResponse(
            content={
                "intent_catogory": state["intent_catogory"],
                "key_entities": state["key_entities"],
                "confidence_score": state["confidence_score"],
                "follow_up_questions": state["follow_up_questions"]
            },
            status_code=200,
            media_type="application/json",
        )
    except requests.exceptions.RequestException as e:
        return JSONResponse(
            content={"error": {"message": f"Request failed: {str(e)}"}},
            status_code=500
        )
    except Exception as e:
        return JSONResponse(
            content={"error": {"message": f"Unexpected error: {str(e)}"}},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)
