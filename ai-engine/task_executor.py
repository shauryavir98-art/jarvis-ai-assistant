"""
JARVIS AI Engine — Task Executor
Handles system tasks: opening websites and launching applications.
"""

import os
import re
import logging
import platform
import subprocess
import webbrowser

logger = logging.getLogger("JARVIS.TaskExecutor")

# Common application mappings (Windows-focused)
APP_MAPPINGS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "terminal": "cmd.exe",
    "powershell": "powershell.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "outlook": "outlook.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "vscode": "code",
    "visual studio code": "code",
    "spotify": "spotify.exe",
    "discord": "discord.exe",
    "slack": "slack.exe",
    "teams": "teams.exe",
    "task manager": "taskmgr.exe",
    "settings": "ms-settings:",
    "control panel": "control.exe",
}

# Common website shortcuts
WEBSITE_SHORTCUTS = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "chatgpt": "https://chat.openai.com",
    "twitter": "https://twitter.com",
    "reddit": "https://www.reddit.com",
    "linkedin": "https://www.linkedin.com",
    "wikipedia": "https://www.wikipedia.org",
}


class TaskExecutor:
    """Executes system-level tasks like opening websites and applications."""

    def __init__(self):
        """Initialize the task executor."""
        self.system = platform.system().lower()
        logger.info(f"✅ Task executor initialized (platform: {self.system})")

    def try_execute(self, text: str) -> str | None:
        """
        Attempt to parse and execute a task command from natural language.

        Args:
            text: Natural language text that may contain a task command.

        Returns:
            Result string if a task was executed, None otherwise.
        """
        lower = text.lower().strip()

        # Pattern: "open <website/app>"
        open_match = re.match(r"^(?:open|launch|start|run)\s+(.+)$", lower)
        if open_match:
            target = open_match.group(1).strip()
            return self.execute(f"open {target}")

        # Pattern: "search for <query>"
        search_match = re.match(r"^(?:search|search for|google)\s+(.+)$", lower)
        if search_match:
            query = search_match.group(1).strip()
            return self._open_website(f"https://www.google.com/search?q={query}")

        return None

    def execute(self, command: str) -> str:
        """
        Execute a task command.

        Args:
            command: The command string (e.g., 'open google.com', 'open notepad')

        Returns:
            Result message string.
        """
        lower = command.lower().strip()

        # Parse "open <target>"
        open_match = re.match(r"^open\s+(.+)$", lower)
        if open_match:
            target = open_match.group(1).strip()

            # Check if it's a website shortcut
            if target in WEBSITE_SHORTCUTS:
                return self._open_website(WEBSITE_SHORTCUTS[target])

            # Check if it looks like a URL
            if self._is_url(target):
                url = target if target.startswith("http") else f"https://{target}"
                return self._open_website(url)

            # Check if it's an application
            if target in APP_MAPPINGS:
                return self._open_application(APP_MAPPINGS[target], target)

            # Try as a direct application name
            return self._open_application(target, target)

        return f"Unknown command: {command}. Try 'open <website>' or 'open <application>'."

    def _open_website(self, url: str) -> str:
        """
        Open a website in the default browser.

        Args:
            url: The URL to open.

        Returns:
            Success message.
        """
        try:
            logger.info(f"Opening website: {url}")
            webbrowser.open(url)
            return f"🌐 Opening website: {url}"
        except Exception as e:
            logger.error(f"Failed to open website: {e}")
            return f"❌ Failed to open website: {e}"

    def _open_application(self, app_path: str, app_name: str) -> str:
        """
        Launch a desktop application.

        Args:
            app_path: The executable path or command.
            app_name: Human-readable application name.

        Returns:
            Success message.
        """
        try:
            logger.info(f"Launching application: {app_name} ({app_path})")

            if self.system == "windows":
                # Use START for Windows
                if app_path.startswith("ms-"):
                    os.system(f"start {app_path}")
                else:
                    subprocess.Popen(
                        app_path,
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            elif self.system == "darwin":
                subprocess.Popen(["open", "-a", app_path])
            else:
                subprocess.Popen(
                    app_path,
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            return f"💻 Launched application: {app_name}"
        except FileNotFoundError:
            return f"❌ Application not found: {app_name}. Make sure it's installed and in your PATH."
        except Exception as e:
            logger.error(f"Failed to launch application: {e}")
            return f"❌ Failed to launch {app_name}: {e}"

    @staticmethod
    def _is_url(text: str) -> bool:
        """Check if text looks like a URL."""
        url_patterns = [
            r"^https?://",
            r"^www\.",
            r"\.\w{2,}$",  # ends with .com, .org, etc.
        ]
        return any(re.search(pattern, text) for pattern in url_patterns)
