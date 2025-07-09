import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain.tools import tool

# ✅ Load .env vars
load_dotenv()

# ✅ LLM (Azure GPT-4o)
llm = AzureChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    temperature=0.3
)

# ✅ Web search tool
search_tool = TavilySearch()
tool_executor = ToolExecutor(tools=[search_tool])

# ✅ Define Graph State (simple dict wrapper)
class AssistantState(dict):
    pass

# ✅ STEP 1: User input -> Search
def run_search(state):
    query = state.get("question")
    print(f"\n🔍 Searching the web for: {query}")
    search_results = tool_executor.invoke({"input": query})
    return {"search_results": search_results["output"], "question": query}

# ✅ STEP 2: GPT summarizes the results
def summarize_results(state):
    results = state.get("search_results")
    question = state.get("question")

    prompt = f"""You are a helpful assistant. Based on the following web search output, answer the user query:

    User Question: {question}

    Web Result: {results}

    Answer:"""

    answer = llm.invoke(prompt)
    return {"answer": answer.content}

# ✅ Build the Graph
graph = StateGraph(AssistantState)

graph.add_node("search_web", run_search)
graph.add_node("summarize", summarize_results)

graph.set_entry_point("search_web")
graph.add_edge("search_web", "summarize")
graph.add_edge("summarize", END)

# ✅ Compile the graph
app = graph.compile()

# === RUN IT! ===
if __name__ == "__main__":
    user_question = input("❓ Ask about iPhone prices in Sri Lanka: ")
    result = app.invoke({"question": user_question})

    print("\n📱 Answer from Assistant:")
    print(result["answer"])