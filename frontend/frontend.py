import streamlit as st
import requests
import json
from datetime import datetime
import time

# ✅ Page configuration
st.set_page_config(
    page_title="iPhone Price Assistant 🍎",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ✅ Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #007AFF;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0051D5;
        transform: translateY(-2px);
    }
    .price-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #007AFF;
    }
    .header-text {
        text-align: center;
        color: #1f1f1f;
    }
</style>
""", unsafe_allow_html=True)

# ✅ API Configuration
API_URL = "http://localhost:8000"  # Change this if your API is hosted elsewhere

# ✅ Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "searching" not in st.session_state:
    st.session_state.searching = False

# ✅ Header
st.markdown("<h1 class='header-text'>🍎 iPhone Price Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-text'>Get real-time iPhone prices in Sri Lanka 🇱🇰</p>", unsafe_allow_html=True)

# ✅ Create columns for better layout
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # ✅ Search form
    with st.form(key="search_form"):
        question = st.text_input(
            "Ask about iPhone prices:",
            placeholder="e.g., What's the latest iPhone 15 Pro Max price in Sri Lanka?",
            help="Type your question about iPhone prices"
        )
        submit_button = st.form_submit_button("🔍 Search", use_container_width=True)

    # ✅ Example questions
    st.markdown("### 💡 Try these questions:")
    example_questions = [
        "Latest iPhone 15 Pro Max price in Sri Lanka?",
        "iPhone 15 vs iPhone 14 prices in LKR",
        "Where to buy iPhone 15 in Colombo?",
        "iPhone 15 Pro 256GB price in Sri Lanka"
    ]
    
    cols = st.columns(2)
    for idx, example in enumerate(example_questions):
        with cols[idx % 2]:
            if st.button(example, key=f"example_{idx}", use_container_width=True):
                question = example
                submit_button = True

# ✅ Function to call API
def get_iphone_price(question: str):
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Make sure the API server is running on port 8000."}
    except Exception as e:
        return {"error": str(e)}

# ✅ Handle search
if submit_button and question:
    st.session_state.searching = True
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
    
    # Show searching animation
    with st.spinner("🔍 Searching for latest prices..."):
        # Simulate search progress
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        # Call API
        result = get_iphone_price(question)
        progress_bar.empty()
    
    # Add response to history
    if "error" in result:
        st.session_state.messages.append({
            "role": "error",
            "content": result["error"],
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": result.get("answer", "No answer received"),
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
    
    st.session_state.searching = False
    st.rerun()

# ✅ Display chat history
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 💬 Search History")
    
    for message in reversed(st.session_state.messages):
        if message["role"] == "user":
            with st.container():
                st.markdown(f"**🧑 You** • {message['timestamp']}")
                st.markdown(f"> {message['content']}")
                st.markdown("")
        
        elif message["role"] == "assistant":
            with st.container():
                st.markdown(f"**🤖 Assistant** • {message['timestamp']}")
                st.markdown(f"<div class='price-box'>{message['content']}</div>", unsafe_allow_html=True)
                st.markdown("")
        
        elif message["role"] == "error":
            with st.container():
                st.error(f"❌ Error: {message['content']}")
                st.markdown("")

# ✅ Sidebar with additional info
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.info(
        "This app uses AI to search real-time iPhone prices "
        "in Sri Lanka from various online sources."
    )
    
    st.markdown("### 🛠️ API Status")
    try:
        health_response = requests.get(f"{API_URL}/health", timeout=2)
        if health_response.status_code == 200:
            st.success("✅ API is running")
        else:
            st.error("❌ API is down")
    except:
        st.error("❌ Cannot connect to API")
    
    st.markdown("### 📊 Statistics")
    total_searches = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Total Searches", total_searches)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ✅ Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Powered by Azure OpenAI GPT-4 & Tavily Search 🚀</p>",
    unsafe_allow_html=True
)