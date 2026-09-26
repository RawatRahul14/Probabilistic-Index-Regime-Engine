# === Python Modules ===
from typing import List, Dict, Any, Set
import numpy as np
import pandas as pd

# === Regime Engine Modules ===
from regime_engine.news.models.embedding_model import load_embedding_model

# === Class to Remove Duplicate News Articles ===
class NewsDeduplicator:
    def __init__(
            self,
            threshold: float = 0.85
    ):
        """
        Removes semantically similar news articles using embeddings.
        """
        self.threshold = threshold

        ## === Loading Embedding Model ===
        self.model = load_embedding_model()

    def _prepare_text(
            self,
            articles: pd.DataFrame
    ) -> List[str]:
        """
        Combines article title and content for embedding generation.
        """
        ## === Filing Missing values ===
        titles = articles["title"].fillna("")
        contents = articles["content"].fillna("").str[:500]

        ## === Combining Title and Content ===
        texts = (titles.astype(str) + " " + contents.astype(str)).str.strip().tolist()

        return texts

    def _generate_embeddings(
            self,
            texts: List[str]
    ) -> np.ndarray:
        """
        Generates normalized embeddings for all articles in a batch.
        """
        embeddings = self.model.encode(
            texts,
            batch_size = 32,
            normalize_embeddings = True,
            show_progress_bar = False
        )

        return embeddings

    def _calculate_similarity(
            self,
            embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Calculates cosine similarity matrix using normalized embeddings.
        """
        similarity_matrix = embeddings @ embeddings.T

        return similarity_matrix

    def deduplicate(
            self,
            articles: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Removes semantically duplicate news articles.
        Keeps the article with the higher Tavily relevance score.
        """

        ## === Empty Article Check ===
        if articles.empty:
            return []

        ## === Preparing Text ===
        texts = self._prepare_text(articles = articles)

        ## === Generating Embeddings ===
        embeddings = self._generate_embeddings(texts = texts)

        ## === Calculating Similarity Matrix ===
        similarity_matrix = self._calculate_similarity(embeddings = embeddings)

        ## === Tracking Removed Articles ===
        removed_indices: Set[int] = set()

        ## === Comparing Articles ===
        for i in range(len(articles)):

            ## === Skipping Removed Article ===
            if i in removed_indices:
                continue

            for j in range(i + 1, len(articles)):

                ## === Skipping Removed Article ===
                if j in removed_indices:
                    continue

                similarity = similarity_matrix[i][j]

                ## === Duplicate Condition ===
                if similarity >= self.threshold:
                    score_i = articles.iloc[i].get("score", 0.0) or 0.0

                    score_j = articles.iloc[j].get("score", 0.0) or 0.0

                    ## === Keeping Higher Tavily Score ===
                    if score_j > score_i:
                        removed_indices.add(i)
                        break

                    else:
                        removed_indices.add(j)

        ## === Returning Unique Articles ===
        keep_indices = [
            index
            for index in range(len(articles))
            if index not in removed_indices
        ]

        ## === Creating Deduplicated DataFrame ===
        unique_articles = articles.iloc[keep_indices].reset_index(drop = True)

        return unique_articles