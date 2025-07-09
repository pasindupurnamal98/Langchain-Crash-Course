import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI  # ✅ Correct import for Azure OpenAI

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize AzureChatOpenAI with the new API options
chat = AzureChatOpenAI(
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME"),  # deployment name in Azure (e.g., "gpt-4o")
    azure_endpoint=os.getenv("OPENAI_API_BASE"),  # full resource endpoint (e.g., https://xxx.openai.azure.com)
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)

# ✅ Create a message
message = [HumanMessage(content="Can you summarize what LangChain is in simple terms?")]

# ✅ Use `.invoke()` instead of calling the model directly
response = chat.invoke(message)

# ✅ Display both prompt and response
print("\n🧠 Prompt:")
print(message[0].content)

print("\n🤖 Response:")
print(response.content)