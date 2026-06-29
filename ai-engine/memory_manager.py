"""
JARVIS AI Engine — Memory Manager
Persists conversation history to a local JSON file.
Provides retrieval for context and analytics.
"""

import os
import json
import logging
from datetime import datetime
from threading import Lock

logger = logging.getLogger("JARVIS.Memory")

# Detect Vercel environment
IS_VERCEL = "VERCEL" in os.environ

if IS_VERCEL:
    MEMORY_DIR = "/tmp"
else:
    MEMORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

MEMORY_FILE = os.path.join(MEMORY_DIR, "conversations.json")
MAX_HISTORY = 1000  # Maximum conversations to keep in memory


class MemoryManager:
    """Manages conversation persistence using a local JSON file."""

    def __init__(self):
        """Initialize the memory manager and load existing data."""
        self._lock = Lock()
        self._history = []
        self._ensure_data_dir()
        self._load()
        logger.info(f"✅ Memory manager initialized ({len(self._history)} conversations loaded)")

    def _ensure_data_dir(self):
        """Create the data directory if it doesn't exist."""
        os.makedirs(MEMORY_DIR, exist_ok=True)

    def _load(self):
        """Load conversation history from disk."""
        try:
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._history = data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not load memory file: {e}. Starting fresh.")
            self._history = []

    def _save(self):
        """Persist conversation history to disk."""
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self._history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to save memory: {e}")

    def save_conversation(self, question: str, response: str) -> None:
        """
        Save a conversation exchange to memory.

        Args:
            question: The user's question.
            response: The AI's response.
        """
        with self._lock:
            entry = {
                "question": question,
                "response": response,
                "timestamp": datetime.now().isoformat(),
            }
            self._history.append(entry)

            # Trim if exceeding max
            if len(self._history) > MAX_HISTORY:
                self._history = self._history[-MAX_HISTORY:]

            self._save()
            logger.debug(f"Saved conversation (total: {len(self._history)})")

    def get_history(self, limit: int = 50) -> list:
        """
        Retrieve recent conversation history.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            List of conversation dictionaries (most recent first).
        """
        with self._lock:
            return list(reversed(self._history[-limit:]))

    def get_context(self, n: int = 5) -> str:
        """
        Get recent conversation context as a formatted string.
        Useful for providing context to the AI model.

        Args:
            n: Number of recent conversations to include.

        Returns:
            Formatted context string.
        """
        with self._lock:
            recent = self._history[-n:]

        if not recent:
            return "No previous conversation context."

        lines = []
        for entry in recent:
            lines.append(f"User: {entry['question']}")
            lines.append(f"JARVIS: {entry['response']}")
            lines.append("")

        return "\n".join(lines)

    def search(self, query: str, limit: int = 10) -> list:
        """
        Search conversation history for matching entries.

        Args:
            query: Search query string.
            limit: Maximum results to return.

        Returns:
            List of matching conversation entries.
        """
        with self._lock:
            query_lower = query.lower()
            matches = [
                entry for entry in self._history
                if query_lower in entry["question"].lower()
                or query_lower in entry["response"].lower()
            ]
            return list(reversed(matches[-limit:]))

    def clear(self) -> None:
        """Clear all conversation history."""
        with self._lock:
            self._history = []
            self._save()
            logger.info("Memory cleared.")

    @property
    def count(self) -> int:
        """Get the total number of stored conversations."""
        return len(self._history)
