import os
from typing import TypedDict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END

# ✅ Load .env variables
load_dotenv()

# ✅ Initialize FastAPI app
app = FastAPI(
    title="iPhone Price Assistant API",
    description="Get latest iPhone prices in Sri Lanka using AI",
    version="1.0.0"
)

# ✅ Add CORS middleware (allows frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Setup LLM (Azure GPT-4o)
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    temperature=0.3
)

# ✅ Tavily Tool (real-time search)
search_tool = TavilySearch()

# ✅ Define the state schema
class GraphState(TypedDict):
    question: str
    search_results: str
    answer: str

# ✅ Node 1: Do real-time search using Tavily
def run_search(state: GraphState) -> dict:
    query = state["question"]
    search_output = search_tool.invoke({"query": query})
    return {"search_results": str(search_output)}

# ✅ Node 2: Use GPT-4o to summarize search result
def summarize_results(state: GraphState) -> dict:
    question = state["question"]
    results = state["search_results"]

    prompt = f"""
You are an assistant. Use the following search results to answer the user query.

User Question:
{question}

Search Results:
{results}

Please extract and summarize the relevant price in LKR (Sri Lankan Rupees).
"""

    response = llm.invoke(prompt)
    return {"answer": response.content}

# ✅ Build the graph
workflow = StateGraph(GraphState)
workflow.add_node("search", run_search)
workflow.add_node("summarize", summarize_results)
workflow.set_entry_point("search")
workflow.add_edge("search", "summarize")
workflow.add_edge("summarize", END)

# ✅ Compile the app
langgraph_app = workflow.compile()

# ✅ Request/Response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    success: bool = True

# ✅ API Endpoints
@app.get("/")
async def root():
    return {
        "message": "iPhone Price Assistant API",
        "endpoints": {
            "POST /ask": "Ask about iPhone prices",
            "GET /health": "Check API health",
            "GET /docs": "API documentation"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iPhone Price Assistant"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        # Initialize state
        initial_state = {
            "question": request.question,
            "search_results": "",
            "answer": ""
        }
        
        # Run the LangGraph workflow
        result = langgraph_app.invoke(initial_state)
        
        return AnswerResponse(
            question=request.question,
            answer=result["answer"],
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)