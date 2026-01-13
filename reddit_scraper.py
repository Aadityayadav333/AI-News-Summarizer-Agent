from typing import List
import os
from utils import *
from typing import List
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
from tenacity import (
    retry, 
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime, timedelta


load_dotenv()


two_weeks_ago = datetime.today() - timedelta(days=14) 
two_weeks_ago_str = two_weeks_ago.strftime('%Y-%m-%d')


class MCPOverloadedError(Exception):
    pass


mcp_limiter = AsyncLimiter(1, 15)

# Use Haiku for free tier
model = ChatAnthropic(
    model="claude-3-5-haiku-20241022",  # Changed from Sonnet for lower cost
    max_tokens=1500  # Reduced token limit
)

server_params = StdioServerParameters(
    command="npx",
    env={
        "API_TOKEN": os.getenv("API_TOKEN"),
        "WEB_UNLOCKER_ZONE": os.getenv("WEB_UNLOCKER_ZONE"),
    },
    args=["@brightdata/mcp"],
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=15, max=60),
    retry=retry_if_exception_type(MCPOverloadedError),
    reraise=True
)
async def process_topic(agent, topic: str):
    async with mcp_limiter:
        messages = [
            {
                "role": "system",
                "content": f"""Reddit analyst. Use tools to:
1. Find top 2 posts about topic after {two_weeks_ago_str}
2. Analyze content and sentiment
3. Summarize discussions"""
            },
            {
                "role": "user",
                "content": f"""Analyze Reddit posts about '{topic}'. Provide:
- Main discussion points
- Key opinions
- Notable trends
- Interesting quotes (no names)
- Overall sentiment"""
            }                   
        ]
        
        try:
            response = await agent.ainvoke({"messages": messages})
            return response["messages"][-1].content
        except Exception as e:
            error_msg = str(e)
            if "Overloaded" in error_msg or "TaskGroup" in error_msg:
                raise MCPOverloadedError("Service overloaded or TaskGroup error")
            else:
                # Return partial result on error instead of failing completely
                return f"Error analyzing {topic}: {error_msg[:100]}"



async def scrape_reddit_topics(topics: List[str]) -> dict[str, dict]:
    """Process list of topics and return analysis results"""
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                agent = create_react_agent(model, tools)
                
                reddit_results = {}
                for topic in topics:
                    try:
                        summary = await process_topic(agent, topic)
                        reddit_results[topic] = summary
                        await asyncio.sleep(5)  # Maintain rate limiting
                    except Exception as e:
                        # Handle individual topic failures gracefully
                        reddit_results[topic] = f"Failed to analyze {topic}: {str(e)[:100]}"
                        continue
                    
                return {"reddit_analysis": reddit_results}
    except Exception as e:
        # If entire session fails, return empty results
        print(f"Reddit scraper failed: {str(e)}")
        return {"reddit_analysis": {topic: f"Unavailable due to error" for topic in topics}}
