"""
JARVIS AI Engine — Chatbot
Supports free AI APIs:
  1. Groq (free) — set GROQ_API_KEY
Falls back to rule-based responses when no API is configured.
"""

import os
import json
import logging
from datetime import datetime

import requests

logger = logging.getLogger("JARVIS.Chatbot")

# API Keys from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Model configuration
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "You are JARVIS (Just A Rather Very Intelligent System), an advanced AI assistant. "
    "You are helpful, knowledgeable, witty, and professional. "
    "Keep responses concise but informative. Use markdown formatting when helpful. "
    "You can help with: answering questions, writing/debugging code, task management, "
    "general conversation and advice. "
    f"Current date/time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)


class JarvisChatbot:
    """AI chatbot supporting Groq and fallback responses."""

    def __init__(self):
        """Initialize the chatbot with the best available API."""
        self._provider = None
        self._groq_history = []
        self._init_provider()

    def _init_provider(self):
        """Detect and initialize the best available AI provider."""

        # Priority 1: Groq
        if GROQ_API_KEY:
            if self._init_groq():
                return

        # Fallback
        logger.warning(
            "⚠️ No AI API key found. Set this environment variable:\n"
            "   set GROQ_API_KEY=your_key      (free: https://console.groq.com/keys)\n"
            "Falling back to rule-based responses."
        )
        self._provider = "fallback"

    # ──────────── Groq ────────────

    def _init_groq(self) -> bool:
        """Initialize Groq API (uses OpenAI-compatible REST endpoint)."""
        try:
            # Test with a simple request
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
            test = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers,
                timeout=10,
            )
            if test.status_code == 200:
                self._provider = "groq"
                self._groq_history = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ]
                logger.info(f"✅ AI Provider: Groq ({GROQ_MODEL})")
                return True
            else:
                logger.warning(f"Groq API returned status {test.status_code}")
        except Exception as e:
            logger.error(f"❌ Groq init failed: {e}")
        return False

    def _ask_groq(self, question: str) -> str:
        """Get response from Groq API (OpenAI-compatible)."""
        try:
            self._groq_history.append({"role": "user", "content": question})

            # Keep history manageable
            if len(self._groq_history) > 21:
                self._groq_history = [self._groq_history[0]] + self._groq_history[-20:]

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": GROQ_MODEL,
                "messages": self._groq_history,
                "temperature": 0.7,
                "max_tokens": 2048,
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                self._groq_history.append({"role": "assistant", "content": answer})
                return answer
            else:
                logger.error(f"Groq API error {response.status_code}: {response.text}")
                return self._get_fallback_response(question)

        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return self._get_fallback_response(question)

    # ──────────── Main Interface ────────────

    def get_response(self, question: str) -> str:
        """
        Get an AI response using the best available provider.

        Args:
            question: The user's question.

        Returns:
            The AI-generated response string.
        """
        if self._provider == "groq":
            return self._ask_groq(question)
        else:
            return self._get_fallback_response(question)

    def get_provider_name(self) -> str:
        """Return the name of the active AI provider."""
        return self._provider or "fallback"

    def reset_session(self):
        """Reset the chat session to clear conversation history."""
        if self._provider == "groq":
            self._groq_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        logger.info("Chat session reset.")

    # ──────────── Fallback ────────────

    def _get_fallback_response(self, question: str) -> str:
        """Rule-based fallback responses when no AI API is available."""
        q = question.lower().strip()

        if any(word in q for word in ["hello", "hi", "hey", "greetings", "good morning", "good evening"]):
            return (
                "Hello! I'm JARVIS, your AI assistant. 👋\n\n"
                "I'm currently in offline mode. To enable AI responses, set:\n"
                "- `set GROQ_API_KEY=your_key` (free: https://console.groq.com/keys)\n\n"
                "Then restart the AI engine."
            )

        if any(phrase in q for phrase in ["who are you", "what are you", "your name"]):
            return (
                "I am **JARVIS** — Just A Rather Very Intelligent System. 🤖\n\n"
                "Built with Spring Boot 3.x + Java 21 backend and Python AI engine.\n"
                "Configure an API key for full AI capabilities!"
            )

        if any(word in q for word in ["time", "date", "day"]):
            now = datetime.now()
            return f"📅 Current date and time: **{now.strftime('%A, %B %d, %Y at %I:%M %p')}**"

        if "help" in q:
            return (
                "I can help with:\n\n"
                "💬 **Chat**: Ask me anything (needs API key)\n"
                "🔔 **Reminders**: Create and manage reminders\n"
                "🌐 **Open Websites**: Say 'open google.com'\n"
                "💻 **Open Apps**: Say 'open notepad'\n\n"
                "**Free API keys:**\n"
                "- Groq: https://console.groq.com/keys"
            )

        if any(word in q for word in ["thank", "thanks"]):
            return "You're welcome! Happy to help. 😊"

        if any(word in q for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! Have a great day! 👋"

        return (
            f"I received your message: \"{question}\"\n\n"
            "I'm in offline mode. To get AI responses, set a free API key:\n\n"
            "**Groq (fast, free):**\n"
            "```\nset GROQ_API_KEY=your_key\n```\n"
            "Get key: https://console.groq.com/keys\n\n"
            "Then restart: `python main.py`"
        )
