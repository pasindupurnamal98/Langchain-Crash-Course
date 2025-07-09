# 🍎 iPhone Price Assistant

<div align="center">

![iPhone Price Assistant](https://img.shields.io/badge/iPhone-Price%20Assistant-007AFF?style=for-the-badge&logo=apple&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)

*Get real-time iPhone prices in Sri Lanka with AI-powered search* 🇱🇰

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [API](#api)

</div>

---

## 📱 About

iPhone Price Assistant is an intelligent web application that helps you find the latest iPhone prices in Sri Lanka. Using advanced AI technology powered by Azure OpenAI GPT-4 and real-time web search capabilities, it provides accurate and up-to-date pricing information from various online sources.

## ✨ Features

- 🔍 **Real-time Search** - Get the latest iPhone prices from multiple sources
- 🤖 **AI-Powered** - Uses Azure OpenAI GPT-4 for intelligent price analysis
- 💱 **LKR Conversion** - Automatic conversion to Sri Lankan Rupees
- 📱 **Beautiful UI** - Clean, responsive Streamlit interface
- 💬 **Chat History** - Keep track of your previous searches
- 🚀 **Fast Response** - Quick results with progress indicators
- 📊 **Statistics** - Track your search activity

## 🛠️ Tech Stack

- **Backend**: Python, LangGraph, Azure OpenAI
- **Frontend**: Streamlit
- **Search Engine**: Tavily Search API
- **AI Model**: Azure GPT-4
- **APIs**: FastAPI (optional)

## 📋 Prerequisites

- Python 3.8 or higher
- Azure OpenAI account
- Tavily Search API key
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/iphone-price-assistant.git
cd iphone-price-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the root directory:

```env
# Azure OpenAI Configuration
OPENAI_API_BASE=your_azure_endpoint
OPENAI_API_KEY=your_azure_api_key
OPENAI_API_VERSION=2024-02-15-preview
OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key

# Optional: API URL for frontend
API_URL=http://localhost:8000
```

## 📦 Dependencies

Create a `requirements.txt` file:

```txt
streamlit>=1.28.0
langchain-openai>=0.1.0
langchain-tavily>=0.2.7
langgraph>=0.1.0
python-dotenv>=1.0.0
requests>=2.31.0
fastapi>=0.104.0
uvicorn>=0.24.0
```

## 🎯 Usage

### Option 1: Streamlit App Only

```bash
streamlit run streamlit_app.py
```

### Option 2: With Backend API

1. **Start the backend** (in one terminal):
```bash
python backend_api.py
```

2. **Start the frontend** (in another terminal):
```bash
streamlit run streamlit_app.py
```

### 🌐 Access the Application

Open your browser and navigate to:
- **Streamlit App**: `http://localhost:8501`
- **API Docs** (if using backend): `http://localhost:8000/docs`

## 💡 Example Queries

Try these sample questions:

- "Latest iPhone 15 Pro Max price in Sri Lanka?"
- "iPhone 15 vs iPhone 14 prices in LKR"
- "Where to buy iPhone 15 in Colombo?"
- "iPhone 15 Pro 256GB price comparison"

