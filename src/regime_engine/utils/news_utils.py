# === YAML Modules ===
import yaml

# === Path Modules ===
from pathlib import Path

# === Function to fetch queries for Tavily ===
def fetch_queries(
        file_path: str
):
    """
    Fetches queries from a yaml file.
    """
    file_path = Path(file_path)

    try:
        with open(file_path, "r", encoding = "utf-8") as f:
            data = yaml.safe_load(f)

        return data

    except FileNotFoundError as e:
        raise RuntimeError(f"YAML file not found: {file_path}") from e

    except yaml.YAMLError as e:
        raise RuntimeError(f"Error parsing YAML file: {file_path}") from e

# === Function to flatten the Queries Dict ===
def flatten_news_data(
        news_data: dict
) -> dict:
    """
    Flattens query-wise news results inside each category.
    """
    flattend_data = {}

    ## === Looping through categories ===
    for category, query_results in news_data.items():

        ## === Flattening Query Results ===
        articles = [
            article
            for results in query_results
            for article in results
        ]

        flattend_data[category] = articles

    return flattend_data

# === Function to Filter News Articles ===

def filter_articles(
        news_data: dict[str, list[dict]],
        min_score: float = 0.4
) -> dict[str, list[dict]]:
    """
    Filters low quality or incomplete news articles while preserving their respective categorie
    """
    ## === Creating Filtered News Dictionary ===
    filtered_news: dict[str, list[dict]] = {}

    ## === Looping Through News Categories ===
    for category, articles in news_data.items():

        ## === Creating Filtered Article List ===
        filtered_articles: list[dict] = []
        for article in articles:

            ## === Checking Required Fields ===
            if not article.get("title"):
                continue

            if not article.get("content"):
                continue

            if not article.get("url"):
                continue

            ## === Getting Tavily Score ===
            score = article.get(
                "score",
                0.0
            ) or 0.0

            ## === Filtering Low Relevance Articles ===
            if score < min_score:
                continue

            ## === Adding Valid Article ===
            filtered_articles.append(
                article
            )

        ## === Saving Category Articles ===
        filtered_news[category] = filtered_articles

    return filtered_news