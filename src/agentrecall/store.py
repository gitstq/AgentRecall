"""
Memory storage engine using SQLite backend.
Provides persistent storage for agent memories with full-text search capabilities.
"""

import sqlite3
import json
import time
import os
from typing import Optional


class MemoryStore:
    """SQLite-backed memory storage engine."""

    def __init__(self, db_path: str = "~/.agentrecall/memories.db"):
        self.db_path = os.path.expanduser(db_path)
        self._ensure_dir()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _ensure_dir(self):
        """Ensure the database directory exists."""
        dir_path = os.path.dirname(self.db_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _init_tables(self):
        """Initialize database tables."""
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL DEFAULT 'default',
                category TEXT NOT NULL DEFAULT 'general',
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                importance REAL DEFAULT 0.5,
                access_count INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                session_id TEXT DEFAULT '',
                metadata TEXT DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS memory_fts (
                rowid INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                tags TEXT
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL DEFAULT 'default',
                started_at REAL NOT NULL,
                ended_at REAL DEFAULT 0,
                memory_count INTEGER DEFAULT 0,
                metadata TEXT DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                total_memories INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                last_active REAL NOT NULL,
                config TEXT DEFAULT '{}'
            );

            CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id);
            CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
            CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance);
            CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
            CREATE INDEX IF NOT EXISTS idx_sessions_agent ON sessions(agent_id);
        """)
        self.conn.commit()

    def save_memory(self, agent_id: str, category: str, title: str,
                    content: str, tags: list = None, importance: float = 0.5,
                    session_id: str = "", metadata: dict = None) -> int:
        """Save a new memory entry."""
        now = time.time()
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        meta_json = json.dumps(metadata or {}, ensure_ascii=False)

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memories (agent_id, category, title, content, tags,
                                  importance, created_at, updated_at,
                                  session_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (agent_id, category, title, content, tags_json,
              importance, now, now, session_id, meta_json))

        memory_id = cursor.lastrowid

        # Insert into FTS table
        tags_text = " ".join(tags or [])
        cursor.execute("""
            INSERT INTO memory_fts (rowid, title, content, tags)
            VALUES (?, ?, ?, ?)
        """, (memory_id, title, content, tags_text))

        # Update agent stats
        self._update_agent_stats(agent_id)

        self.conn.commit()
        return memory_id

    def get_memory(self, memory_id: int) -> Optional[dict]:
        """Retrieve a single memory by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_dict(row)
        return None

    def search_memories(self, query: str, agent_id: str = "default",
                        category: str = None, limit: int = 20,
                        min_importance: float = 0.0) -> list:
        """Search memories using FTS5 full-text search."""
        conditions = ["m.agent_id = ?"]
        params = [agent_id]

        if category:
            conditions.append("m.category = ?")
            params.append(category)

        if min_importance > 0:
            conditions.append("m.importance >= ?")
            params.append(min_importance)

        where_clause = " AND ".join(conditions)

        cursor = self.conn.cursor()
        try:
            cursor.execute(f"""
                SELECT m.*, rank as search_rank
                FROM memories m
                JOIN memory_fts fts ON m.id = fts.rowid
                WHERE memory_fts MATCH ? AND {where_clause}
                ORDER BY search_rank, m.importance DESC, m.updated_at DESC
                LIMIT ?
            """, (query, *params, limit))
        except sqlite3.OperationalError:
            # FTS5 might not be available, fallback to LIKE search
            like_query = f"%{query}%"
            cursor.execute(f"""
                SELECT m.*, 0 as search_rank
                FROM memories m
                WHERE (m.title LIKE ? OR m.content LIKE ?) AND {where_clause}
                ORDER BY m.importance DESC, m.updated_at DESC
                LIMIT ?
            """, (like_query, like_query, *params, limit))

        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def keyword_search(self, keywords: list, agent_id: str = "default",
                       category: str = None, limit: int = 20) -> list:
        """Search memories by keyword matching with TF-IDF-like scoring."""
        if not keywords:
            return []

        cursor = self.conn.cursor()
        conditions = ["m.agent_id = ?"]
        params = [agent_id]

        if category:
            conditions.append("m.category = ?")
            params.append(category)

        where_clause = " AND ".join(conditions)

        # Build keyword matching with scoring
        keyword_conditions = []
        keyword_params = []
        for kw in keywords:
            keyword_conditions.append(
                "(m.title LIKE ? OR m.content LIKE ? OR m.tags LIKE ?)"
            )
            like = f"%{kw}%"
            keyword_params.extend([like, like, like])

        kw_clause = " OR ".join(keyword_conditions)

        cursor.execute(f"""
            SELECT m.*,
                   (CASE WHEN m.title LIKE ? THEN 3 ELSE 0 END +
                    CASE WHEN m.tags LIKE ? THEN 2 ELSE 0 END +
                    CASE WHEN m.content LIKE ? THEN 1 ELSE 0 END +
                    m.importance * 2 +
                    m.access_count * 0.1) as relevance_score
            FROM memories m
            WHERE ({kw_clause}) AND {where_clause}
            ORDER BY relevance_score DESC, m.updated_at DESC
            LIMIT ?
        """, (f"%{keywords[0]}%", f"%{keywords[0]}%", f"%{keywords[0]}%",
              *keyword_params, *params, limit))

        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_recent(self, agent_id: str = "default", limit: int = 20,
                   category: str = None) -> list:
        """Get most recently updated memories."""
        conditions = ["agent_id = ?"]
        params = [agent_id]

        if category:
            conditions.append("category = ?")
            params.append(category)

        where_clause = " AND ".join(conditions)

        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT * FROM memories
            WHERE {where_clause}
            ORDER BY updated_at DESC
            LIMIT ?
        """, (*params, limit))

        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update_memory(self, memory_id: int, title: str = None,
                      content: str = None, tags: list = None,
                      importance: float = None, category: str = None,
                      metadata: dict = None) -> bool:
        """Update an existing memory."""
        existing = self.get_memory(memory_id)
        if not existing:
            return False

        now = time.time()
        updates = ["updated_at = ?"]
        params = [now]

        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags, ensure_ascii=False))
        if importance is not None:
            updates.append("importance = ?")
            params.append(importance)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if metadata is not None:
            updates.append("metadata = ?")
            params.append(json.dumps(metadata, ensure_ascii=False))

        params.append(memory_id)

        cursor = self.conn.cursor()
        cursor.execute(f"""
            UPDATE memories SET {', '.join(updates)} WHERE id = ?
        """, params)

        # Update FTS
        if title is not None or content is not None or tags is not None:
            new_title = title or existing["title"]
            new_content = content or existing["content"]
            new_tags = tags if tags is not None else (existing["tags"] if isinstance(existing["tags"], list) else json.loads(existing["tags"]))
            tags_text = " ".join(new_tags)
            cursor.execute("""
                UPDATE memory_fts SET title = ?, content = ?, tags = ?
                WHERE rowid = ?
            """, (new_title, new_content, tags_text, memory_id))

        self.conn.commit()
        return True

    def delete_memory(self, memory_id: int) -> bool:
        """Delete a memory by ID."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        cursor.execute("DELETE FROM memory_fts WHERE rowid = ?", (memory_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def increment_access(self, memory_id: int):
        """Increment the access count for a memory."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE memories SET access_count = access_count + 1 WHERE id = ?
        """, (memory_id,))
        self.conn.commit()

    def get_stats(self, agent_id: str = None) -> dict:
        """Get memory statistics."""
        cursor = self.conn.cursor()

        if agent_id:
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    COUNT(DISTINCT category) as categories,
                    COUNT(DISTINCT session_id) as sessions,
                    AVG(importance) as avg_importance,
                    SUM(access_count) as total_accesses
                FROM memories WHERE agent_id = ?
            """, (agent_id,))
        else:
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    COUNT(DISTINCT category) as categories,
                    COUNT(DISTINCT session_id) as sessions,
                    AVG(importance) as avg_importance,
                    SUM(access_count) as total_accesses
                FROM memories
            """)

        row = cursor.fetchone()
        return {
            "total_memories": row["total"],
            "categories": row["categories"],
            "sessions": row["sessions"],
            "avg_importance": round(row["avg_importance"], 2) if row["avg_importance"] else 0,
            "total_accesses": row["total_accesses"] or 0
        }

    def get_categories(self, agent_id: str = "default") -> list:
        """Get all categories with memory counts."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(importance) as avg_importance
            FROM memories WHERE agent_id = ?
            GROUP BY category ORDER BY count DESC
        """, (agent_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_all_agents(self) -> list:
        """Get all registered agents."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM agents ORDER BY last_active DESC")
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def register_agent(self, agent_id: str, name: str,
                       description: str = "", config: dict = None) -> bool:
        """Register a new agent or update existing one."""
        now = time.time()
        config_json = json.dumps(config or {}, ensure_ascii=False)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO agents (id, name, description, total_memories,
                               created_at, last_active, config)
            VALUES (?, ?, ?, 0, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                description = excluded.description,
                last_active = excluded.last_active,
                config = excluded.config
        """, (agent_id, name, description, now, now, config_json))
        self.conn.commit()
        return True

    def start_session(self, agent_id: str = "default",
                      session_id: str = None) -> str:
        """Start a new session."""
        if not session_id:
            session_id = f"sess_{int(time.time())}_{os.urandom(4).hex()}"

        now = time.time()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (id, agent_id, started_at, metadata)
            VALUES (?, ?, ?, '{}')
        """, (session_id, agent_id, now))
        self.conn.commit()
        return session_id

    def end_session(self, session_id: str):
        """End a session."""
        now = time.time()
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sessions SET ended_at = ?,
                memory_count = (SELECT COUNT(*) FROM memories WHERE session_id = ?)
            WHERE id = ?
        """, (now, session_id, session_id))
        self.conn.commit()

    def get_session_memories(self, session_id: str) -> list:
        """Get all memories from a specific session."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM memories WHERE session_id = ?
            ORDER BY created_at ASC
        """, (session_id,))
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def get_context_for_agent(self, agent_id: str = "default",
                              max_tokens: int = 4000,
                              categories: list = None) -> str:
        """Build a context string from top memories for agent injection."""
        conditions = ["agent_id = ?"]
        params = [agent_id]

        if categories:
            placeholders = ",".join("?" * len(categories))
            conditions.append(f"category IN ({placeholders})")
            params.extend(categories)

        where_clause = " AND ".join(conditions)

        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT * FROM memories
            WHERE {where_clause}
            ORDER BY importance DESC, access_count DESC, updated_at DESC
            LIMIT 50
        """, params)

        rows = cursor.fetchall()
        if not rows:
            return ""

        lines = ["# AgentRecall - Persistent Memory Context",
                 f"# Agent: {agent_id} | Memories: {len(rows)}", ""]

        current_length = sum(len(l) for l in lines)
        for row in rows:
            mem = self._row_to_dict(row)
            entry = f"[{mem['category'].upper()}] {mem['title']}\n{mem['content']}\n"
            if current_length + len(entry) > max_tokens:
                break
            lines.append(entry)
            current_length += len(entry)

        return "\n".join(lines)

    def export_memories(self, agent_id: str = "default",
                        format: str = "json") -> str:
        """Export all memories for an agent."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM memories WHERE agent_id = ?
            ORDER BY created_at DESC
        """, (agent_id,))
        rows = cursor.fetchall()
        memories = [self._row_to_dict(row) for row in rows]

        if format == "json":
            return json.dumps(memories, indent=2, ensure_ascii=False, default=str)
        elif format == "markdown":
            lines = [f"# AgentRecall Memories - {agent_id}", ""]
            for m in memories:
                tags = ", ".join(json.loads(m["tags"]))
                lines.append(f"## [{m['category']}] {m['title']}")
                lines.append(f"**Tags:** {tags} | **Importance:** {m['importance']}")
                lines.append(f"**Created:** {time.ctime(m['created_at'])}")
                lines.append("")
                lines.append(m["content"])
                lines.append("")
                lines.append("---")
                lines.append("")
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def import_memories(self, agent_id: str, data: str,
                        format: str = "json") -> int:
        """Import memories from exported data."""
        if format == "json":
            memories = json.loads(data)
        else:
            raise ValueError(f"Unsupported import format: {format}")

        count = 0
        for m in memories:
            self.save_memory(
                agent_id=agent_id,
                category=m.get("category", "general"),
                title=m.get("title", "Imported"),
                content=m.get("content", ""),
                tags=json.loads(m.get("tags", "[]")),
                importance=m.get("importance", 0.5),
                metadata=json.loads(m.get("metadata", "{}"))
            )
            count += 1
        return count

    def cleanup_old_memories(self, agent_id: str = "default",
                             max_age_days: int = 90,
                             min_importance: float = 0.3) -> int:
        """Remove old low-importance memories."""
        cutoff = time.time() - (max_age_days * 86400)
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM memories
            WHERE agent_id = ? AND created_at < ? AND importance < ?
        """, (agent_id, cutoff, min_importance))

        deleted = cursor.rowcount
        # Clean up FTS entries
        cursor.execute("""
            DELETE FROM memory_fts WHERE rowid NOT IN (
                SELECT id FROM memories
            )
        """)
        self.conn.commit()
        return deleted

    def _update_agent_stats(self, agent_id: str):
        """Update agent memory count stats."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM memories WHERE agent_id = ?
        """, (agent_id,))
        count = cursor.fetchone()["cnt"]

        cursor.execute("""
            INSERT INTO agents (id, name, description, total_memories,
                               created_at, last_active, config)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                total_memories = excluded.total_memories,
                last_active = excluded.last_active
        """, (agent_id, agent_id, '', count, time.time(), time.time(), '{}'))
        self.conn.commit()

    def _row_to_dict(self, row) -> dict:
        """Convert a SQLite Row to dictionary."""
        d = dict(row)
        # Parse JSON fields
        for field in ("tags", "metadata"):
            if field in d and isinstance(d[field], str):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    d[field] = [] if field == "tags" else {}
        return d

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
