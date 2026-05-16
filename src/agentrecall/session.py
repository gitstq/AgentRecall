"""
Session manager - Track and manage agent coding sessions.
Captures session context and links memories to sessions.
"""

import time
import json
import os
from typing import Optional


class SessionManager:
    """Manages agent coding sessions and their memory associations."""

    def __init__(self, store):
        self.store = store
        self._current_session = None
        self._current_agent = "default"

    def start_session(self, agent_id: str = "default",
                      session_id: str = None,
                      description: str = "") -> str:
        """
        Start a new coding session.

        Args:
            agent_id: The agent identifier
            session_id: Optional custom session ID
            description: Optional session description

        Returns:
            Session ID
        """
        self._current_agent = agent_id
        self._current_session = self.store.start_session(agent_id, session_id)

        # Register agent if new
        self.store.register_agent(agent_id, agent_id, description)

        # Auto-capture session start memory
        self.store.save_memory(
            agent_id=agent_id,
            category="workflow",
            title=f"Session Started: {description or 'New Session'}",
            content=f"Coding session started at {time.strftime('%Y-%m-%d %H:%M:%S')}. "
                    f"Description: {description or 'No description provided.'}",
            tags=["session", "start"],
            importance=0.3,
            session_id=self._current_session
        )

        return self._current_session

    def end_session(self, summary: str = ""):
        """
        End the current session with optional summary.

        Args:
            summary: Optional session summary
        """
        if not self._current_session:
            return

        # Save session summary memory
        if summary:
            self.store.save_memory(
                agent_id=self._current_agent,
                category="workflow",
                title=f"Session Summary",
                content=summary,
                tags=["session", "summary"],
                importance=0.6,
                session_id=self._current_session
            )

        self.store.end_session(self._current_session)
        self._current_session = None

    def capture_decision(self, title: str, content: str,
                         tags: list = None, importance: float = 0.7):
        """Capture a technical decision made during the session."""
        if not self._current_session:
            self.start_session()

        return self.store.save_memory(
            agent_id=self._current_agent,
            category="decision",
            title=title,
            content=content,
            tags=tags or ["decision"],
            importance=importance,
            session_id=self._current_session
        )

    def capture_context(self, title: str, content: str,
                        tags: list = None, importance: float = 0.5):
        """Capture project context information."""
        if not self._current_session:
            self.start_session()

        return self.store.save_memory(
            agent_id=self._current_agent,
            category="context",
            title=title,
            content=content,
            tags=tags or ["context"],
            importance=importance,
            session_id=self._current_session
        )

    def capture_bug(self, title: str, content: str,
                    tags: list = None, importance: float = 0.8):
        """Capture a bug encountered and its resolution."""
        if not self._current_session:
            self.start_session()

        return self.store.save_memory(
            agent_id=self._current_agent,
            category="bug",
            title=title,
            content=content,
            tags=tags or ["bug"],
            importance=importance,
            session_id=self._current_session
        )

    def capture_feature(self, title: str, content: str,
                        tags: list = None, importance: float = 0.6):
        """Capture a feature implementation detail."""
        if not self._current_session:
            self.start_session()

        return self.store.save_memory(
            agent_id=self._current_agent,
            category="feature",
            title=title,
            content=content,
            tags=tags or ["feature"],
            importance=importance,
            session_id=self._current_session
        )

    def capture_lesson(self, title: str, content: str,
                       tags: list = None, importance: float = 0.7):
        """Capture a lesson learned during development."""
        if not self._current_session:
            self.start_session()

        return self.store.save_memory(
            agent_id=self._current_agent,
            category="lesson",
            title=title,
            content=content,
            tags=tags or ["lesson"],
            importance=importance,
            session_id=self._current_session
        )

    def capture_architecture(self, title: str, content: str,
                             tags: list = None, importance: float = 0.8):
        """Capture architecture decision or pattern."""
        if not self._current_session:
            self.start_session()

        return self.store.save_memory(
            agent_id=self._current_agent,
            category="architecture",
            title=title,
            content=content,
            tags=tags or ["architecture"],
            importance=importance,
            session_id=self._current_session
        )

    def get_current_session_id(self) -> Optional[str]:
        """Get the current session ID."""
        return self._current_session

    def get_session_history(self, agent_id: str = "default",
                            limit: int = 10) -> list:
        """Get recent session summaries."""
        conn = self.store.conn
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM sessions
            WHERE agent_id = ?
            ORDER BY started_at DESC
            LIMIT ?
        """, (agent_id, limit))

        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                "id": row["id"],
                "agent_id": row["agent_id"],
                "started_at": row["started_at"],
                "ended_at": row["ended_at"],
                "memory_count": row["memory_count"],
                "duration": row["ended_at"] - row["started_at"] if row["ended_at"] else None
            })

        return sessions

    def get_session_summary(self, session_id: str) -> dict:
        """Get a comprehensive summary of a session."""
        memories = self.store.get_session_memories(session_id)

        if not memories:
            return {"session_id": session_id, "memories": [], "summary": "No memories found"}

        categories = {}
        total_importance = 0
        for m in memories:
            cat = m["category"]
            categories[cat] = categories.get(cat, 0) + 1
            total_importance += m["importance"]

        return {
            "session_id": session_id,
            "total_memories": len(memories),
            "categories": categories,
            "avg_importance": round(total_importance / len(memories), 2),
            "memories": memories
        }
