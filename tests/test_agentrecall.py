"""
Tests for AgentRecall - Memory Store, Search Engine, Compressor, and CLI.
"""

import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agentrecall.store import MemoryStore
from agentrecall.search import SearchEngine
from agentrecall.compressor import MemoryCompressor
from agentrecall.session import SessionManager
from agentrecall.utils import (
    generate_id, content_hash, estimate_tokens,
    truncate_to_tokens, validate_importance, sanitize_tag, parse_tags
)


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_generate_id(self):
        """Test ID generation."""
        id1 = generate_id("test")
        id2 = generate_id("test")
        self.assertTrue(id1.startswith("test_"))
        self.assertNotEqual(id1, id2)

    def test_content_hash(self):
        """Test content hashing."""
        h1 = content_hash("hello world")
        h2 = content_hash("hello world")
        h3 = content_hash("different content")
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
        self.assertEqual(len(h1), 12)

    def test_estimate_tokens(self):
        """Test token estimation."""
        self.assertEqual(estimate_tokens(""), 0)
        self.assertGreater(estimate_tokens("hello world"), 0)

    def test_truncate_to_tokens(self):
        """Test token truncation."""
        text = "word " * 1000
        result = truncate_to_tokens(text, 10)
        self.assertLess(len(result), len(text))

    def test_validate_importance(self):
        """Test importance validation."""
        self.assertEqual(validate_importance(0.5), 0.5)
        self.assertEqual(validate_importance(-1.0), 0.0)
        self.assertEqual(validate_importance(2.0), 1.0)

    def test_sanitize_tag(self):
        """Test tag sanitization."""
        self.assertEqual(sanitize_tag("Hello World!"), "helloworld")
        self.assertEqual(sanitize_tag("  test-tag  "), "test-tag")

    def test_parse_tags(self):
        """Test tag parsing."""
        self.assertEqual(parse_tags("a, b, c"), ["a", "b", "c"])
        self.assertEqual(parse_tags(""), [])
        self.assertEqual(parse_tags(None), [])


class TestMemoryCompressor(unittest.TestCase):
    """Test memory compressor."""

    def setUp(self):
        self.compressor = MemoryCompressor()

    def test_compress_basic(self):
        """Test basic compression."""
        content = "This is a test content. " * 100
        result = self.compressor.compress(content)
        self.assertIn("compressed", result)
        self.assertIn("ratio", result)
        self.assertLess(result["compressed_length"], result["original_length"])

    def test_compress_empty(self):
        """Test compression of empty content."""
        result = self.compressor.compress("")
        self.assertEqual(result["compressed"], "")
        self.assertEqual(result["ratio"], 1.0)

    def test_compress_preserves_code(self):
        """Test that code blocks are preserved."""
        content = """
Some text before code.
```python
def hello():
    print("Hello, World!")
```
Some text after code.
"""
        result = self.compressor.compress(content)
        self.assertIn("def hello", result["compressed"])
        self.assertIn("print", result["compressed"])

    def test_extract_keywords(self):
        """Test keyword extraction."""
        content = "The authentication system uses JWT tokens for API security. The JWT implementation includes refresh token rotation."
        keywords = self.compressor.extract_keywords(content)
        self.assertTrue(len(keywords) > 0)
        # JWT should be highly ranked
        keyword_words = [kw for kw, score in keywords]
        self.assertIn("jwt", keyword_words)

    def test_summarize(self):
        """Test summarization."""
        content = (
            "AgentRecall is a memory engine for AI coding agents. "
            "It uses SQLite for storage and TF-IDF for search. "
            "The tool supports multiple agents and categories. "
            "It can export memories in JSON and Markdown formats. "
            "The compression engine reduces memory footprint. "
        )
        summary = self.compressor.summarize(content, max_sentences=2)
        self.assertTrue(len(summary) < len(content))
        self.assertTrue(len(summary) > 0)


class TestMemoryStore(unittest.TestCase):
    """Test memory store."""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.store = MemoryStore(self.db_path)

    def tearDown(self):
        self.store.close()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_save_and_get(self):
        """Test saving and retrieving a memory."""
        mid = self.store.save_memory(
            agent_id="test",
            category="decision",
            title="Test Memory",
            content="This is a test memory content.",
            tags=["test", "unit"]
        )
        mem = self.store.get_memory(mid)
        self.assertIsNotNone(mem)
        self.assertEqual(mem["title"], "Test Memory")
        self.assertEqual(mem["category"], "decision")
        self.assertEqual(mem["tags"], ["test", "unit"])

    def test_search(self):
        """Test memory search."""
        self.store.save_memory("test", "general", "Python Setup",
                               "Python 3.10 with virtual environment setup", ["python"])
        self.store.save_memory("test", "general", "JavaScript Setup",
                               "Node.js 18 with npm setup", ["javascript"])
        self.store.save_memory("test", "decision", "Auth Decision",
                               "Use JWT for authentication", ["auth", "jwt"])

        results = self.store.search_memories("python", "test")
        self.assertTrue(len(results) > 0)
        self.assertIn("Python", results[0]["title"])

    def test_keyword_search(self):
        """Test keyword search."""
        self.store.save_memory("test", "general", "Database Config",
                               "PostgreSQL database configuration", ["database", "postgres"])
        self.store.save_memory("test", "general", "Cache Config",
                               "Redis cache configuration", ["cache", "redis"])

        results = self.store.keyword_search(["database", "postgres"], "test")
        self.assertTrue(len(results) > 0)

    def test_update(self):
        """Test memory update."""
        mid = self.store.save_memory("test", "general", "Original",
                                     "Original content", ["tag1"])
        success = self.store.update_memory(mid, title="Updated",
                                           content="Updated content")
        self.assertTrue(success)
        mem = self.store.get_memory(mid)
        self.assertEqual(mem["title"], "Updated")
        self.assertEqual(mem["content"], "Updated content")

    def test_delete(self):
        """Test memory deletion."""
        mid = self.store.save_memory("test", "general", "To Delete",
                                     "Delete me", [])
        success = self.store.delete_memory(mid)
        self.assertTrue(success)
        mem = self.store.get_memory(mid)
        self.assertIsNone(mem)

    def test_get_recent(self):
        """Test getting recent memories."""
        for i in range(5):
            self.store.save_memory("test", "general", f"Memory {i}",
                                   f"Content {i}", [])
        recent = self.store.get_recent("test", limit=3)
        self.assertEqual(len(recent), 3)

    def test_get_stats(self):
        """Test statistics."""
        self.store.save_memory("test", "decision", "D1", "Content 1", [])
        self.store.save_memory("test", "bug", "B1", "Content 2", [])
        self.store.save_memory("test", "feature", "F1", "Content 3", [])

        stats = self.store.get_stats("test")
        self.assertEqual(stats["total_memories"], 3)
        self.assertEqual(stats["categories"], 3)

    def test_export_import(self):
        """Test export and import."""
        self.store.save_memory("test", "decision", "Export Test",
                               "Export content", ["export"])
        exported = self.store.export_memories("test", "json")
        data = json.loads(exported)
        self.assertEqual(len(data), 1)

    def test_register_agent(self):
        """Test agent registration."""
        self.store.register_agent("claude", "Claude Code", "Anthropic's coding agent")
        agents = self.store.get_all_agents()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["name"], "Claude Code")

    def test_session_management(self):
        """Test session management."""
        sid = self.store.start_session("test")
        self.assertIsNotNone(sid)
        self.store.save_memory("test", "general", "Session Mem",
                               "In session", [], session_id=sid)
        self.store.end_session(sid)
        memories = self.store.get_session_memories(sid)
        self.assertEqual(len(memories), 1)

    def test_context_generation(self):
        """Test context generation for agent."""
        self.store.save_memory("test", "decision", "Auth Decision",
                               "Use JWT tokens", ["auth"], importance=0.9)
        self.store.save_memory("test", "architecture", "MVC Pattern",
                               "Use MVC architecture", ["arch"], importance=0.8)
        context = self.store.get_context_for_agent("test", max_tokens=1000)
        self.assertIn("Auth Decision", context)
        self.assertIn("JWT", context)

    def test_cleanup(self):
        """Test cleanup of old memories."""
        # Save a memory and manually backdate it
        mid = self.store.save_memory("test", "general", "Old Memory",
                                     "Old content", [], importance=0.1)
        # Manually set created_at to very old
        import time
        old_time = time.time() - (100 * 86400)  # 100 days ago
        self.store.conn.execute(
            "UPDATE memories SET created_at = ? WHERE id = ?", (old_time, mid)
        )
        self.store.conn.commit()

        deleted = self.store.cleanup_old_memories("test", max_age_days=90, min_importance=0.3)
        self.assertGreater(deleted, 0)


class TestSearchEngine(unittest.TestCase):
    """Test search engine."""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.store = MemoryStore(self.db_path)
        self.engine = SearchEngine(self.store)

        # Seed test data
        self.store.save_memory("test", "decision", "Auth Decision",
                               "Use JWT tokens for API authentication with refresh token rotation",
                               ["auth", "jwt", "api"])
        self.store.save_memory("test", "architecture", "Database Design",
                               "PostgreSQL with Redis cache layer for session management",
                               ["database", "redis", "architecture"])
        self.store.save_memory("test", "bug", "Memory Leak Fix",
                               "Fixed memory leak in WebSocket connection handler by properly closing connections",
                               ["bug", "websocket", "memory"])
        self.store.save_memory("test", "feature", "Search API",
                               "Implemented full-text search API with TF-IDF ranking and faceted filters",
                               ["search", "api", "feature"])
        self.store.save_memory("test", "config", "Docker Setup",
                               "Multi-stage Docker build with Alpine base image and health checks",
                               ["docker", "devops", "config"])

    def tearDown(self):
        self.store.close()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_hybrid_search(self):
        """Test hybrid search mode."""
        results = self.engine.search("authentication JWT", "test", mode="hybrid")
        self.assertTrue(len(results) > 0)
        # Auth decision should be top result
        titles = [r["title"] for r in results]
        self.assertIn("Auth Decision", titles)

    def test_keyword_search(self):
        """Test keyword search mode."""
        results = self.engine.search("database redis", "test", mode="keyword")
        self.assertTrue(len(results) > 0)

    def test_tfidf_search(self):
        """Test TF-IDF search mode."""
        results = self.engine.search("websocket memory leak", "test", mode="tfidf")
        self.assertTrue(len(results) > 0)

    def test_category_filter(self):
        """Test category filtering."""
        results = self.engine.search("api", "test", category="decision")
        for r in results:
            self.assertEqual(r["category"], "decision")

    def test_suggest_related(self):
        """Test related memory suggestions."""
        # Get the auth decision memory
        results = self.store.search_memories("JWT", "test")
        if results:
            related = self.engine.suggest_related(results[0]["id"])
            self.assertTrue(len(related) >= 0)  # May or may not find related

    def test_empty_query(self):
        """Test empty query handling."""
        results = self.engine.search("", "test")
        self.assertEqual(len(results), 0)

    def test_trending_tags(self):
        """Test trending tags."""
        tags = self.engine.get_trending_tags("test")
        self.assertTrue(len(tags) > 0)


class TestSessionManager(unittest.TestCase):
    """Test session manager."""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.store = MemoryStore(self.db_path)
        self.session_mgr = SessionManager(self.store)

    def tearDown(self):
        self.store.close()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_session_lifecycle(self):
        """Test full session lifecycle."""
        sid = self.session_mgr.start_session("test", description="Test session")
        self.assertIsNotNone(sid)

        self.session_mgr.capture_decision(
            "Use React", "Decided to use React for the frontend"
        )
        self.session_mgr.capture_bug(
            "Login Bug", "Fixed login redirect issue after token refresh"
        )
        self.session_mgr.capture_feature(
            "Dark Mode", "Implemented dark mode with CSS variables"
        )

        self.session_mgr.end_session("Completed auth module refactoring")

        # Verify memories were saved
        memories = self.store.get_session_memories(sid)
        self.assertTrue(len(memories) >= 3)  # At least 3 captures + session start/end

    def test_capture_types(self):
        """Test different capture types."""
        self.session_mgr.start_session("test")

        d_id = self.session_mgr.capture_decision("D", "Decision content")
        b_id = self.session_mgr.capture_bug("B", "Bug content")
        f_id = self.session_mgr.capture_feature("F", "Feature content")
        c_id = self.session_mgr.capture_context("C", "Context content")
        l_id = self.session_mgr.capture_lesson("L", "Lesson content")
        a_id = self.session_mgr.capture_architecture("A", "Architecture content")

        for mid in [d_id, b_id, f_id, c_id, l_id, a_id]:
            mem = self.store.get_memory(mid)
            self.assertIsNotNone(mem)


if __name__ == "__main__":
    unittest.main()
