"""
Configuration management for AgentRecall.
"""

import json
import os
from typing import Optional


DEFAULT_CONFIG = {
    "db_path": "~/.agentrecall/memories.db",
    "max_memory_length": 2000,
    "default_agent": "default",
    "default_category": "general",
    "default_importance": 0.5,
    "context_max_tokens": 4000,
    "search_mode": "hybrid",
    "search_limit": 20,
    "cleanup_max_age_days": 90,
    "cleanup_min_importance": 0.3,
    "compress_preserve_code": True,
    "categories": [
        "decision", "bug", "feature", "context",
        "architecture", "lesson", "config", "workflow", "general"
    ]
}

CONFIG_PATH = "~/.agentrecall/config.json"


class Config:
    """AgentRecall configuration manager."""

    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = os.path.expanduser(config_path)
        self._config = self._load()

    def _load(self) -> dict:
        """Load configuration from file or use defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = {**DEFAULT_CONFIG, **user_config}
                return config
            except (json.JSONDecodeError, IOError):
                pass
        return dict(DEFAULT_CONFIG)

    def save(self):
        """Save current configuration to file."""
        dir_path = os.path.dirname(self.config_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value):
        """Set a configuration value."""
        self._config[key] = value

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __contains__(self, key):
        return key in self._config

    def to_dict(self) -> dict:
        """Return configuration as dictionary."""
        return dict(self._config)
