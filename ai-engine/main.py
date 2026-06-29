"""
JARVIS AI Engine — Main Entry Point
Flask server providing REST API for the Spring Boot backend.
Endpoints:
  POST /api/chat       - Send a question, get AI response
  POST /api/speech/tts - Text-to-speech
  POST /api/tasks      - Execute system tasks (open websites/apps)
  GET  /api/health     - Health check
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot import JarvisChatbot
from speech_engine import SpeechEngine
from task_executor import TaskExecutor
from memory_manager import MemoryManager

# ──────────── Configuration ────────────
app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("JARVIS")

# Initialize modules
chatbot = JarvisChatbot()
speech_engine = SpeechEngine()
task_executor = TaskExecutor()
memory_manager = MemoryManager()


# ──────────── Routes ────────────

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "online",
        "engine": "JARVIS AI Engine",
        "version": "1.0.0"
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Process a chat question and return AI response.
    Expects JSON: { "question": "..." }
    Returns JSON: { "response": "...", "status": "success" }
    """
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    logger.info(f"Chat request: {question[:100]}...")

    try:
        # Check for task commands first
        task_result = task_executor.try_execute(question)
        if task_result:
            response_text = task_result
        else:
            # Get AI response
            response_text = chatbot.get_response(question)

        # Save to memory
        memory_manager.save_conversation(question, response_text)

        return jsonify({
            "response": response_text,
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({
            "response": f"I encountered an error: {str(e)}",
            "status": "error"
        }), 500


@app.route("/api/speech/tts", methods=["POST"])
def text_to_speech():
    """
    Convert text to speech.
    Expects JSON: { "text": "..." }
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    try:
        speech_engine.speak(data["text"])
        return jsonify({"status": "success", "message": "Speech completed"})
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/speech/stt", methods=["POST"])
def speech_to_text():
    """
    Capture speech from microphone and convert to text.
    """
    try:
        text = speech_engine.listen()
        return jsonify({"text": text, "status": "success"})
    except Exception as e:
        logger.error(f"STT error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/tasks", methods=["POST"])
def execute_task():
    """
    Execute a system task.
    Expects JSON: { "command": "open website google.com" }
    """
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Missing 'command' field"}), 400

    try:
        result = task_executor.execute(data["command"])
        return jsonify({"result": result, "status": "success"})
    except Exception as e:
        logger.error(f"Task error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/history", methods=["GET"])
def get_memory_history():
    """Get conversation history from memory."""
    limit = request.args.get("limit", 50, type=int)
    history = memory_manager.get_history(limit)
    return jsonify({"history": history, "count": len(history)})


# ──────────── Entry Point ────────────

if __name__ == "__main__":
    port = int(os.environ.get("JARVIS_PORT", 5000))
    debug = os.environ.get("JARVIS_DEBUG", "false").lower() == "true"

    logger.info(f"🚀 JARVIS AI Engine starting on port {port}")
    logger.info(f"📡 API available at http://localhost:{port}/api/")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
