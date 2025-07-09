import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# ✅ Load .env variables
load_dotenv()

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

# ✅ Define the state schema properly
class GraphState(TypedDict):
    question: str
    search_results: str
    answer: str

# ✅ Node 1: Do real-time search using Tavily
def run_search(state: GraphState) -> dict:
    query = state["question"]
    print(f"\n🔍 Searching the web for: {query}")
    
    # TavilySearch expects { "query": ... }
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

# ✅ Build the graph with proper state type
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("search", run_search)
workflow.add_node("summarize", summarize_results)

# Set the entry point
workflow.set_entry_point("search")

# Add edges
workflow.add_edge("search", "summarize")
workflow.add_edge("summarize", END)

# ✅ Compile the app
app = workflow.compile()

# ✅ Run the app
if __name__ == "__main__":
    print("💬 iPhone Price Assistant (LangGraph)")
    user_input = input("❓ Ask a question (e.g., 'Latest iPhone 15 price in Sri Lanka'): ")

    # Initialize all required state fields
    initial_state = {
        "question": user_input,
        "search_results": "",
        "answer": ""
    }

    result = app.invoke(initial_state)

    print("\n📱 Assistant Answer:")
    print(result["answer"])