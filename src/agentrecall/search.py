"""
Search engine with TF-IDF and keyword hybrid scoring.
Provides intelligent memory retrieval with relevance ranking.
"""

import math
import re
import sqlite3
from collections import Counter, defaultdict
from typing import Optional


class SearchEngine:
    """Hybrid TF-IDF + keyword search engine for memories."""

    # Common English stop words
    STOP_WORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "need", "to", "of",
        "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
        "during", "before", "after", "and", "or", "but", "not", "no", "if",
        "then", "than", "too", "very", "just", "about", "this", "that", "it",
        "its", "what", "which", "who", "whom", "also", "been", "being",
    }

    def __init__(self, store):
        """Initialize with a MemoryStore instance."""
        self.store = store
        self._idf_cache = {}

    def search(self, query: str, agent_id: str = "default",
               mode: str = "hybrid", category: str = None,
               limit: int = 20, min_importance: float = 0.0) -> list:
        """
        Search memories using the specified mode.

        Args:
            query: Search query string
            agent_id: Agent to search within
            mode: 'hybrid', 'fulltext', 'keyword', or 'tfidf'
            category: Optional category filter
            limit: Maximum results
            min_importance: Minimum importance threshold

        Returns:
            List of memory dicts with '_score' field added
        """
        if not query or not query.strip():
            return []

        query = query.strip()

        if mode == "fulltext":
            results = self.store.search_memories(
                query, agent_id, category, limit * 2, min_importance
            )
        elif mode == "keyword":
            keywords = self._tokenize(query)
            results = self.store.keyword_search(
                keywords, agent_id, category, limit * 2
            )
        elif mode == "tfidf":
            results = self._tfidf_search(
                query, agent_id, category, limit * 2, min_importance
            )
        else:  # hybrid
            results = self._hybrid_search(
                query, agent_id, category, limit * 2, min_importance
            )

        # Add scores and sort
        for r in results:
            r["_score"] = r.pop("search_rank", 0) + r.pop("relevance_score", 0)

        results.sort(key=lambda x: x["_score"], reverse=True)

        # Increment access counts
        for r in results[:limit]:
            self.store.increment_access(r["id"])

        return results[:limit]

    def _hybrid_search(self, query: str, agent_id: str,
                       category: Optional[str], limit: int,
                       min_importance: float) -> list:
        """Combine fulltext and keyword search results."""
        # Get results from both methods
        ft_results = self.store.search_memories(
            query, agent_id, category, limit, min_importance
        )

        keywords = self._tokenize(query)
        kw_results = self.store.keyword_search(
            keywords, agent_id, category, limit
        )

        # Merge results using reciprocal rank fusion
        merged = {}
        k = 60  # RRF constant

        for rank, result in enumerate(ft_results):
            mem_id = result["id"]
            if mem_id not in merged:
                merged[mem_id] = result.copy()
            merged[mem_id]["_rr_score"] = merged[mem_id].get("_rr_score", 0) + 1 / (k + rank + 1)

        for rank, result in enumerate(kw_results):
            mem_id = result["id"]
            if mem_id not in merged:
                merged[mem_id] = result.copy()
            merged[mem_id]["_rr_score"] = merged[mem_id].get("_rr_score", 0) + 1 / (k + rank + 1)

        # Add TF-IDF bonus
        tfidf_results = self._tfidf_search(query, agent_id, category, limit, min_importance)
        for rank, result in enumerate(tfidf_results):
            mem_id = result["id"]
            if mem_id in merged:
                merged[mem_id]["_rr_score"] += 2 / (k + rank + 1)  # Higher weight for TF-IDF

        results = list(merged.values())
        results.sort(key=lambda x: x.get("_rr_score", 0), reverse=True)

        # Add combined score
        for r in results:
            r["relevance_score"] = r.get("_rr_score", 0) * 100

        return results[:limit]

    def _tfidf_search(self, query: str, agent_id: str,
                      category: Optional[str], limit: int,
                      min_importance: float) -> list:
        """TF-IDF based search implementation."""
        # Get all memories for the agent
        conditions = ["agent_id = ?"]
        params = [agent_id]
        if category:
            conditions.append("category = ?")
            params.append(category)
        if min_importance > 0:
            conditions.append("importance >= ?")
            params.append(min_importance)

        where = " AND ".join(conditions)
        conn = self.store.conn
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM memories WHERE {where}
            ORDER BY updated_at DESC LIMIT 500
        """, params)

        memories = [self.store._row_to_dict(row) for row in cursor.fetchall()]

        if not memories:
            return []

        # Build document corpus
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        docs = []
        for mem in memories:
            text = f"{mem['title']} {mem['content']} {' '.join(mem.get('tags', []))}"
            tokens = self._tokenize(text)
            docs.append({
                "id": mem["id"],
                "tokens": tokens,
                "memory": mem
            })

        # Calculate IDF
        N = len(docs)
        df = Counter()
        for doc in docs:
            unique_tokens = set(doc["tokens"])
            for token in unique_tokens:
                df[token] += 1

        # Calculate TF-IDF scores for each document
        scored = []
        for doc in docs:
            tf = Counter(doc["tokens"])
            score = 0.0

            for qt in query_tokens:
                if qt in tf:
                    # TF: log-normalized
                    term_tf = 1 + math.log(tf[qt]) if tf[qt] > 0 else 0
                    # IDF: smoothed
                    term_idf = math.log((N + 1) / (df.get(qt, 0) + 1)) + 1
                    score += term_tf * term_idf

            if score > 0:
                # Normalize by document length
                doc_len = len(doc["tokens"]) if doc["tokens"] else 1
                score = score / math.sqrt(doc_len)

                # Boost by importance and recency
                importance = doc["memory"].get("importance", 0.5)
                access_count = doc["memory"].get("access_count", 0)
                score = score * (1 + importance) * (1 + min(access_count * 0.05, 1))

                scored.append({
                    **doc["memory"],
                    "relevance_score": round(score, 4)
                })

        scored.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored[:limit]

    def suggest_related(self, memory_id: int, limit: int = 5) -> list:
        """Find memories related to a given memory."""
        memory = self.store.get_memory(memory_id)
        if not memory:
            return []

        # Build query from the memory's content
        text = f"{memory['title']} {memory['content']}"
        keywords = self._tokenize(text)[:15]

        if not keywords:
            return []

        query = " ".join(keywords)
        results = self.search(
            query, memory["agent_id"], mode="hybrid", limit=limit + 1
        )

        # Exclude the original memory
        return [r for r in results if r["id"] != memory_id][:limit]

    def get_trending_tags(self, agent_id: str = "default",
                          limit: int = 20) -> list:
        """Get most frequently used tags across memories."""
        conn = self.store.conn
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tags FROM memories WHERE agent_id = ?
        """, (agent_id,))

        tag_counter = Counter()
        for row in cursor.fetchall():
            try:
                import json
                tags = json.loads(row["tags"])
                for tag in tags:
                    tag_counter[tag] += 1
            except (json.JSONDecodeError, TypeError):
                pass

        return tag_counter.most_common(limit)

    def _tokenize(self, text: str) -> list:
        """Tokenize text into lowercase words, removing stop words."""
        # Extract words (including hyphenated and underscored)
        tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_-]*\b", text.lower())
        return [t for t in tokens if t not in self.STOP_WORDS and len(t) > 1]
