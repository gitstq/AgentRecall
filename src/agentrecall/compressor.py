"""
Memory compressor - Intelligent content compression for efficient storage.
Reduces memory footprint while preserving semantic meaning.
"""

import re
import hashlib
from typing import Optional


class MemoryCompressor:
    """Intelligent memory content compressor."""

    # Common filler phrases to remove
    FILLER_PATTERNS = [
        r"\b(in order to)\b",
        r"\b(it is important to note that)\b",
        r"\b(as a matter of fact)\b",
        r"\b(for the purpose of)\b",
        r"\b(in the context of)\b",
        r"\b(with regard to)\b",
        r"\b(it should be noted that)\b",
        r"\b(it goes without saying that)\b",
        r"\b(at the end of the day\b)",
        r"\b(in this case\b)",
        r"\b(as you can see\b)",
        r"\b(basically|essentially|actually|literally|honestly)\b",
    ]

    # Code block markers to preserve
    CODE_BLOCK_PATTERN = re.compile(r"(```[\s\S]*?```|`[^`]+`)", re.DOTALL)

    def __init__(self, max_length: int = 2000, preserve_code: bool = True):
        self.max_length = max_length
        self.preserve_code = preserve_code

    def compress(self, content: str) -> dict:
        """
        Compress memory content while preserving key information.

        Returns:
            dict with 'compressed', 'original_length', 'compressed_length',
                  'ratio', 'hash' keys
        """
        if not content:
            return {
                "compressed": "",
                "original_length": 0,
                "compressed_length": 0,
                "ratio": 1.0,
                "hash": ""
            }

        original_length = len(content)
        original_hash = hashlib.md5(content.encode()).hexdigest()[:12]

        # Step 1: Extract and protect code blocks
        code_blocks = []
        if self.preserve_code:
            content, code_blocks = self._extract_code_blocks(content)

        # Step 2: Remove filler phrases
        compressed = content
        for pattern in self.FILLER_PATTERNS:
            compressed = re.sub(pattern, "", compressed, flags=re.IGNORECASE)

        # Step 3: Normalize whitespace
        compressed = re.sub(r"\n{3,}", "\n\n", compressed)
        compressed = re.sub(r" {2,}", " ", compressed)
        compressed = compressed.strip()

        # Step 4: Remove duplicate lines (keeping first occurrence)
        lines = compressed.split("\n")
        seen = set()
        unique_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and stripped not in seen:
                seen.add(stripped)
                unique_lines.append(line)
        compressed = "\n".join(unique_lines)

        # Step 5: Restore code blocks
        if self.preserve_code and code_blocks:
            compressed = self._restore_code_blocks(compressed, code_blocks)

        # Step 6: Truncate if needed (keep beginning and end)
        if len(compressed) > self.max_length:
            compressed = self._smart_truncate(compressed, self.max_length)

        compressed_length = len(compressed)
        ratio = compressed_length / original_length if original_length > 0 else 1.0

        return {
            "compressed": compressed,
            "original_length": original_length,
            "compressed_length": compressed_length,
            "ratio": round(ratio, 3),
            "hash": original_hash
        }

    def extract_keywords(self, content: str, max_keywords: int = 10) -> list:
        """
        Extract important keywords from content using TF-based scoring.

        Returns list of (keyword, score) tuples sorted by relevance.
        """
        if not content:
            return []

        # Remove code blocks for keyword extraction
        clean_content = re.sub(r"```[\s\S]*?```", "", content)
        clean_content = re.sub(r"`[^`]+`", "", clean_content)

        # Tokenize
        words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_-]{2,}\b", clean_content.lower())

        if not words:
            return []

        # Stop words
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "shall", "can", "need", "dare",
            "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
            "from", "as", "into", "through", "during", "before", "after", "above",
            "below", "between", "out", "off", "over", "under", "again", "further",
            "then", "once", "here", "there", "when", "where", "why", "how", "all",
            "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very",
            "just", "because", "but", "and", "or", "if", "while", "about", "this",
            "that", "these", "those", "it", "its", "what", "which", "who", "whom",
            "also", "been", "being", "get", "got", "make", "made", "like", "use",
            "using", "used", "new", "way", "well", "back", "even", "still",
        }

        # Filter stop words and count frequencies
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1

        if not word_freq:
            return []

        # Score: frequency * length bonus (longer words are more specific)
        scored = []
        for word, freq in word_freq.items():
            score = freq * (1 + len(word) * 0.1)
            # Bonus for technical terms (contain digits, underscores, hyphens)
            if re.search(r"[_\-\d]", word):
                score *= 1.5
            scored.append((word, round(score, 2)))

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[:max_keywords]

    def summarize(self, content: str, max_sentences: int = 3) -> str:
        """
        Extract key sentences from content as a summary.
        Uses sentence position and keyword density for scoring.
        """
        if not content:
            return ""

        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", content.strip())
        if len(sentences) <= max_sentences:
            return content.strip()

        # Extract keywords for scoring
        keywords = self.extract_keywords(content, max_keywords=20)
        keyword_set = {kw for kw, _ in keywords}

        # Score each sentence
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue

            score = 0.0

            # Position bonus (first and last sentences are important)
            if i == 0:
                score += 3.0
            elif i == len(sentences) - 1:
                score += 2.0
            elif i < 3:
                score += 1.0

            # Keyword density
            words = set(re.findall(r"\b\w+\b", sentence.lower()))
            keyword_matches = words & keyword_set
            score += len(keyword_matches) * 1.5

            # Length preference (medium-length sentences)
            word_count = len(sentence.split())
            if 10 <= word_count <= 40:
                score += 1.0
            elif word_count > 40:
                score -= 0.5

            # Contains numbers (often important facts)
            if re.search(r"\d", sentence):
                score += 0.5

            scored_sentences.append((sentence, score))

        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top = scored_sentences[:max_sentences]

        # Restore original order
        top.sort(key=lambda x: sentences.index(x[0]))

        return " ".join(s[0] for s in top)

    def _extract_code_blocks(self, content: str) -> tuple:
        """Extract code blocks and replace with placeholders."""
        blocks = []
        counter = [0]

        def replacer(match):
            placeholder = f"__CODE_BLOCK_{counter[0]}__"
            blocks.append(match.group(0))
            counter[0] += 1
            return placeholder

        processed = self.CODE_BLOCK_PATTERN.sub(replacer, content)
        return processed, blocks

    def _restore_code_blocks(self, content: str, blocks: list) -> str:
        """Restore code blocks from placeholders."""
        for i, block in enumerate(blocks):
            content = content.replace(f"__CODE_BLOCK_{i}__", block)
        return content

    def _smart_truncate(self, content: str, max_length: int) -> str:
        """Truncate content keeping beginning and end."""
        if len(content) <= max_length:
            return content

        head_size = max_length * 2 // 3
        tail_size = max_length - head_size - 20  # 20 for separator

        head = content[:head_size]
        tail = content[-tail_size:]

        # Try to break at sentence/line boundary
        last_period = head.rfind(".")
        if last_period > head_size * 0.5:
            head = head[:last_period + 1]

        first_newline = tail.find("\n")
        if first_newline > 0 and first_newline < tail_size * 0.3:
            tail = tail[first_newline + 1:]

        return f"{head}\n\n... [truncated] ...\n\n{tail}"
