"""
Utility functions for AgentRecall.
"""

import hashlib
import time
import os
import re
from typing import Optional


def generate_id(prefix: str = "mem") -> str:
    """Generate a unique ID with prefix."""
    timestamp = int(time.time() * 1000)
    random_hex = os.urandom(4).hex()
    return f"{prefix}_{timestamp}_{random_hex}"


def content_hash(content: str) -> str:
    """Generate a short hash of content for deduplication."""
    return hashlib.md5(content.encode()).hexdigest()[:12]


def estimate_tokens(text: str) -> int:
    """Estimate token count (rough: 1 token ≈ 4 chars for English)."""
    if not text:
        return 0
    return len(text) // 4


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to approximately max_tokens."""
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text

    # Try to break at sentence boundary
    truncated = text[:max_chars]
    last_period = truncated.rfind(".")
    if last_period > max_chars * 0.7:
        return truncated[:last_period + 1]

    return truncated + "..."


def format_bytes(size: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def validate_importance(value: float) -> float:
    """Validate and clamp importance value to [0.0, 1.0]."""
    return max(0.0, min(1.0, value))


def sanitize_tag(tag: str) -> str:
    """Sanitize a tag string."""
    tag = tag.strip().lower()
    tag = re.sub(r"[^\w\-]", "", tag)
    return tag[:50]


def parse_tags(tags_str: str) -> list:
    """Parse comma-separated tags string."""
    if not tags_str:
        return []
    return [sanitize_tag(t) for t in tags_str.split(",") if t.strip()]


def get_db_size(db_path: str) -> int:
    """Get database file size in bytes."""
    expanded = os.path.expanduser(db_path)
    if os.path.exists(expanded):
        return os.path.getsize(expanded)
    return 0
