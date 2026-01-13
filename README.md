# 🎙️ NewsNinja - AI-Powered News & Reddit Summarizer

> Transform news articles and Reddit discussions into audio summaries with AI

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📺 Demo

https://github.com/user-attachments/assets/fecfd6be-6680-4e84-8bca-c977807934d5

> *Note: Video will appear here after first push to GitHub*

## 🎯 What It Does

NewsNinja scrapes the latest news and Reddit discussions on any topic, summarizes them using AI, and converts the summary into an audio broadcast - perfect for staying informed while multitasking!

## ✨ Features

- 🔍 **Multi-Source Scraping** - Get news from Google News and Reddit
- 🤖 **AI Summarization** - Powered by Groq's Llama 3.3 70B (FREE!)
- 🎙️ **Text-to-Speech** - Convert summaries to audio using Google TTS
- 🎨 **Clean UI** - Simple Streamlit interface
- 📥 **Download Audio** - Save summaries for offline listening

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js (for MCP server)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Aadityayadav333/AI-News-Summarizer-Agent.git
cd AI-News-Summarizer-Agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
npm install -g @brightdata/mcp
```

3. **Set up environment variables**

Create a `.env` file:
```env
# Groq API (FREE) - Get from https://console.groq.com/
GROQ_API_KEY=your_groq_api_key

# BrightData (for web scraping) - Get from https://brightdata.com/
BRIGHTDATA_API_KEY=your_brightdata_key
BRIGHTDATA_WEB_UNLOCKER_ZONE=your_zone
API_TOKEN=your_api_token
WEB_UNLOCKER_ZONE=your_zone
```

4. **Run the application**

Terminal 1 - Backend:
```bash
python backend.py
```

Terminal 2 - Frontend:
```bash
streamlit run frontend.py
```

5. **Open your browser** → `http://localhost:8501`

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Model**: Groq (Llama 3.3 70B)
- **Web Scraping**: BrightData + BeautifulSoup
- **Reddit**: MCP Server + LangGraph
- **TTS**: Google Text-to-Speech (gTTS)

## 📁 Project Structure

```
NewsNinja/
├── backend.py           # FastAPI server
├── frontend.py          # Streamlit UI
├── models.py            # Data models
├── utils.py             # Helper functions
├── news_scraper.py      # News scraping logic
├── reddit_scraper.py    # Reddit scraping logic
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── Screen Recording/    # Demo video
```

## 🎯 Usage

1. Enter a topic (e.g., "Artificial Intelligence")
2. Select source: News, Reddit, or Both
3. Click "Generate Summary"
4. Listen or download the audio!

## 💡 Use Cases

- 📰 Daily news briefings
- 📊 Market research summaries
- 🎓 Educational topic overviews
- 🚗 Commute-friendly news updates

## 🔑 API Keys (All FREE!)

1. **Groq** (Required)
   - Sign up: https://console.groq.com/
   - Free tier: 30 requests/minute
   - No credit card needed

2. **BrightData** (Required)
   - Sign up: https://brightdata.com/
   - Free trial available

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

## 📝 License

MIT License - feel free to use this project however you'd like!

## 🙏 Acknowledgments

- Groq for free AI API
- BrightData for web scraping
- Google for TTS
- Anthropic for MCP framework

## 📧 Contact

Questions? Feel free to open an issue!

---

⭐ **Star this repo if you found it helpful!**
