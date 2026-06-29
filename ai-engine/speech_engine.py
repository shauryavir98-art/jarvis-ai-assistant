"""
JARVIS AI Engine — Speech Engine
Provides speech-to-text and text-to-speech capabilities.
Uses SpeechRecognition for STT and pyttsx3 for TTS.
"""

import os
import logging

logger = logging.getLogger("JARVIS.Speech")


class SpeechEngine:
    """Handles speech-to-text and text-to-speech conversions."""

    def __init__(self):
        """Initialize the speech engine."""
        self._tts_engine = None
        self._recognizer = None
        
        if "VERCEL" in os.environ:
            logger.info("Speech engines disabled on Vercel serverless environment.")
            return

        self._init_tts()
        self._init_stt()

    def _init_tts(self):
        """Initialize text-to-speech engine."""
        try:
            import pyttsx3
            self._tts_engine = pyttsx3.init()

            # Configure voice properties
            self._tts_engine.setProperty("rate", 175)      # Speed
            self._tts_engine.setProperty("volume", 0.9)    # Volume

            # Try to set a clear voice
            voices = self._tts_engine.getProperty("voices")
            if voices and len(voices) > 1:
                # Use the second voice (often female/clearer)
                self._tts_engine.setProperty("voice", voices[1].id)

            logger.info("✅ TTS engine initialized (pyttsx3)")
        except ImportError:
            logger.warning("⚠️ pyttsx3 not installed. TTS will be unavailable.")
            self._tts_engine = None
        except Exception as e:
            logger.warning(f"⚠️ TTS init failed: {e}")
            self._tts_engine = None

    def _init_stt(self):
        """Initialize speech-to-text recognizer."""
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 4000
            self._recognizer.dynamic_energy_threshold = True
            logger.info("✅ STT engine initialized (SpeechRecognition)")
        except ImportError:
            logger.warning("⚠️ SpeechRecognition not installed. STT will be unavailable.")
            self._recognizer = None

    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.

        Args:
            text: The text to speak aloud.

        Raises:
            RuntimeError: If TTS engine is not available.
        """
        if not self._tts_engine:
            raise RuntimeError("TTS engine is not available. Install pyttsx3.")

        try:
            logger.info(f"Speaking: {text[:80]}...")
            self._tts_engine.say(text)
            self._tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
            raise RuntimeError(f"Speech synthesis failed: {e}")

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> str:
        """
        Listen to microphone input and convert speech to text.

        Args:
            timeout: Maximum seconds to wait for speech to start.
            phrase_time_limit: Maximum seconds for a single phrase.

        Returns:
            The recognized text string.

        Raises:
            RuntimeError: If STT engine is not available or recognition fails.
        """
        if not self._recognizer:
            raise RuntimeError("STT engine is not available. Install SpeechRecognition.")

        try:
            import speech_recognition as sr

            with sr.Microphone() as source:
                logger.info("🎤 Listening...")
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            logger.info("Processing speech...")
            text = self._recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text

        except Exception as e:
            error_type = type(e).__name__
            if "UnknownValueError" in error_type:
                raise RuntimeError("Could not understand the audio. Please speak clearly.")
            elif "RequestError" in error_type:
                raise RuntimeError("Speech recognition service is unavailable. Check internet connection.")
            elif "WaitTimeoutError" in error_type:
                raise RuntimeError("No speech detected. Please try again.")
            else:
                raise RuntimeError(f"Speech recognition failed: {e}")
