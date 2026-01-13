from urllib.parse import quote_plus
from dotenv import load_dotenv
import requests
import os
from fastapi import HTTPException
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from gtts import gTTS
from groq import Groq

load_dotenv()

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

class MCPOverloadedError(Exception):
    pass

def generate_valid_news_url(keyword: str) -> str:
    q = quote_plus(keyword)
    return f"https://news.google.com/search?q={q}&tbs=sbd:1"

def generate_news_urls_to_scrape(list_of_keywords):
    return {keyword: generate_valid_news_url(keyword) for keyword in list_of_keywords}

def scrape_with_brightdata(url: str) -> str:
    headers = {"Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}", "Content-Type": "application/json"}
    payload = {"zone": os.getenv('BRIGHTDATA_WEB_UNLOCKER_ZONE'), "url": url, "format": "raw"}
    try:
        response = requests.post("https://api.brightdata.com/request", json=payload, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"BrightData error: {str(e)}")

def clean_html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator="\n").strip()

def extract_headlines(cleaned_text: str) -> str:
    headlines = []
    current_block = []
    lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
    for line in lines:
        if line == "More":
            if current_block:
                headlines.append(current_block[0])
                current_block = []
        else:
            current_block.append(line)
    if current_block:
        headlines.append(current_block[0])
    return "\n".join(headlines)

def generate_broadcast_news(api_key, news_data, reddit_data, topics):
    system_prompt = """You are a professional news reporter. Generate TTS-ready news reports:

For each topic:
1. If news exists: Summarize official reports
2. If Reddit exists: Summarize online discussions  
3. If both: Present news first, then Reddit reactions

Rules:
- Start directly, NO introductions
- Keep audio 60-90 seconds per topic
- Use natural transitions
- Add 1-2 short quotes from Reddit if available
- Neutral tone
- End with brief summary

Write in full paragraphs for speech. No markdown."""

    try:
        topic_blocks = []
        for topic in topics:
            news_content = news_data.get("news_analysis", {}).get(topic) if news_data else ''
            reddit_content = reddit_data.get("reddit_analysis", {}).get(topic) if reddit_data else ''
            context = []
            if news_content:
                context.append(f"NEWS: {news_content[:800]}")
            if reddit_content:
                context.append(f"REDDIT: {reddit_content[:800]}")
            if context:
                topic_blocks.append(f"TOPIC: {topic}\n" + "\n".join(context))

        user_prompt = "Create broadcast for:\n\n" + "\n\n---\n\n".join(topic_blocks)
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2000,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise e

def summarize_with_groq_news_script(api_key: str, headlines: str) -> str:
    system_prompt = """You are a news scriptwriter. Create a clean, TTS-friendly script:
- No special characters, emojis, or markdown
- No preamble
- Full paragraphs in broadcast style
- Focus on key headlines
- Natural spoken language"""

    try:
        client = Groq(api_key=api_key)
        truncated_headlines = headlines[:2000] if len(headlines) > 2000 else headlines
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": truncated_headlines}],
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            max_tokens=600,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq error: {str(e)}")

def tts_to_audio(text: str, language: str = 'en') -> str:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = AUDIO_DIR / f"tts_{timestamp}.mp3"
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(str(filename))
        return str(filename)
    except Exception as e:
        print(f"gTTS Error: {str(e)}")
        return None
