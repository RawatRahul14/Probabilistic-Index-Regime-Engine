# === Python Modules ===
import os
from typing import List, Literal, Dict, Any
import asyncio

# === Tavily Modules ===
from tavily import AsyncTavilyClient

# === Fetching the Tavily API ===
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# === Async Tavily Client ===
tavily = AsyncTavilyClient(
    api_key = TAVILY_API_KEY
)

# === Async Tavily function ===
async def fetch_data_tavily(
    query: str,
    topic: str,
    max_results: int
) -> List[Dict[str, Any]]:
    """
    Fetches data from Tavily asynchronously for a single query.
    """
    response = await tavily.search(
        query = query,
        topic = topic,
        time_range = "day",
        max_results = max_results,
        include_raw_content = False,
        search_depth = "advanced",
        timeout = 10
    )
    ## === Extracting useful data ===
    data_dic: List[Dict[str, Any]] = []

    for data in response["results"]:
        data_dic.append({
            "query": query,
            "topic": topic,
            "title": data.get("title"),
            "url": data.get("url"),
            "content": data.get("content"),
            "score": data.get("score"),
            "published_date": data.get("published_date")
        })
    return data_dic

# === Fetching Multiple queries at a time ===
async def fetch_multiple_queries(
    queries: List[str],
    topic: Literal["news", "finance", "general"],
    concurrency: int = 15,
    max_results: int = 3,
) -> List[List[Dict[str, Any]]]:
    """
    Fetches Tavily data for multiple queries concurrently.
    """
    ## === Limiting the number of searches, to avoid rate limit ===
    semaphore = asyncio.Semaphore(concurrency)

    ## === Calling Async ===
    async def safe_fetch(q):
        async with semaphore:
            try:
                return await fetch_data_tavily(
                    query = q,
                    max_results = max_results,
                    topic = topic
                )

            except Exception as e:
                raise RuntimeError(
                    "Error fetching the news data async."
                ) from e

    ## === Running the async function ===
    tasks = [safe_fetch(q) for q in queries]
    return await asyncio.gather(*tasks)

# === Fetching all News Categories ===
async def fetch_news(
        data: dict,
        market_time: Literal["open_market", "pre_market"]
) -> dict:
    """
    Fetches all open market news categories concurrently.
    """
    ## === Extracting Market Queries ===
    market_queries  = data[market_time]

    ## === Creating Async Tasks ===
    tasks = {
        news_type: fetch_multiple_queries(
            queries = query_list,
            topic = "news",
            max_results = 3
        )
        for news_type, query_list in market_queries .items()
    }

    ## === Running all Categories Concurrently ===
    results = await asyncio.gather(
        *tasks.values()
    )

    ## === Mapping Results Back to Categories ===
    news_data = {
        news_type: result
        for news_type, result in zip(
            tasks.keys(),
            results
        )
    }
    return news_data