# === Python modules ===
import pandas as pd
import os

# === Async Modules ===
import asyncio

# === langchain and Langgraph Modules ===
from langchain_openai import ChatOpenAI

# === Models ===
from regime_engine.news.models.sentiment_model import SentimentModel

# === API KEY ===
api_key = os.getenv("OPENAI_API_KEY")

## === Model ===
llm_model = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0,
    openai_api_key = api_key
).with_structured_output(SentimentModel)

# === Process Single Article ===
async def sentiment_agent(
        article: dict
) -> dict:

    ## === Prompt ===
    prompt = f"""
        You are a financial news classification model.

        Analyze the following news article and determine its
        potential effect on the NIFTY 50 index.

        Article Title:
        {article['title']}

        Article Content:
        {article['content']}

        Classify the article according to the provided structured
        output schema.

        Important instructions:

        1. p_bull, p_neutral and p_bear must represent your
        probability distribution for the directional effect
        on NIFTY.

        2. confidence represents how confident you are in your
        classification.

        3. importance represents the potential significance of
        this event for NIFTY and Indian financial markets.

        4. affected_scope should contain the relevant market
        segments or sectors.

        5. event_type should represent the primary type of event.

        Do not predict whether NIFTY will actually rise or fall.
        Classify the information contained in the article.
    """

    ## === Invoking the LLM ===
    result = await llm_model.ainvoke(prompt)

    return {
        "article_id": article["article_id"],
        "sentiment": result
    }

# === Concurrent Sentiment Processing ===
async def process_articles_concurrently(
        articles: list[dict],
        concurrency: int = 10
) -> list[dict]:
    """
    Process a list of articles concurrently using the sentiment_agent function.
    """
    try:

        ## === Setting up the semaphore ===
        semaphore = asyncio.Semaphore(concurrency)

        ## === Defining the worker function ===
        async def process_with_limit(article: dict) -> dict | None:
            async with semaphore:

                try:
                    return await sentiment_agent(article)

                except Exception as e:
                    print(f"Error processing article {article['article_id']}: {e}")
                    return None

        ## === Creating tasks for all articles ===
        tasks = [
            process_with_limit(article) for article in articles
        ]

        ## === Gathering results ===
        results = await asyncio.gather(*tasks)

        ### === Filtering out None results ===
        results = [
            result
            for result in results
            if result is not None
        ]

        return results

    except Exception as e:
        raise ValueError(f"Error in process_articles_concurrently.") from e

# === Sentiment Analysis ===
async def sentiment_analysis(
        articles: pd.DataFrame,
        concurrency: int = 10
) -> pd.DataFrame:
    """
    Perform sentiment analysis on a DataFrame of articles concurrently.
    """
    try:

        ### === Copying the articles DataFrame ===
        articles = articles.copy()

        ### === Adding article_id column ===
        articles["article_id"] = articles["url"]

        ## === Converting DataFrame to List of Dictionaries ===
        articles_list = articles.to_dict(orient = "records")

        results = await process_articles_concurrently(
            articles = articles_list,
            concurrency = concurrency
        )

        sentiment_df = pd.DataFrame([
            {
                "article_id": result["article_id"],
                "p_bull": result["sentiment"].p_bull,
                "p_neutral": result["sentiment"].p_neutral,
                "p_bear": result["sentiment"].p_bear,
                "confidence": result["sentiment"].confidence,
                "importance": result["sentiment"].importance,
                "novelty": result["sentiment"].novelty,
                "affected_scope": result["sentiment"].affected_scope,
                "event_type": result["sentiment"].event_type
            }
            for result in results
        ])

        return articles.merge(
            sentiment_df,
            on = "article_id",
            how = "inner"
        )

    except Exception as e:
        raise ValueError(f"Error in sentiment_analysis.") from e