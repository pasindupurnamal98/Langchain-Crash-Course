import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv()

# Initialize LLM (Azure OpenAI GPT-4o)
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    temperature=0.5
)

# Load the tool – Tavily (searches the web)
search_tool = TavilySearchResults()

# Prompt template (LangChain hub)
prompt = hub.pull("hwchase17/openai-tools-agent")

# Create the agent with tools (GPT + Tools)
agent = create_openai_tools_agent(
    llm=llm,
    tools=[search_tool],
    prompt=prompt
)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

# --- Run prompt ---
question = "What are the latest iPhone prices in Sri Lanka as of July 2025?"
response = agent_executor.invoke({"input": question})

print("\n📱 iPhone Prices in Sri Lanka:")
print(response["output"])