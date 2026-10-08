# ============================================================
# J.A.R.V.I.S BRAIN
# Gemini AI Powered
# Developed by Jayvardhan Singh
# ============================================================

import os
import sys
import time

from dotenv import load_dotenv
from google import genai

# ------------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------------

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

from config import (
    ASSISTANT_NAME,
    ASSISTANT_FULL_NAME,
    USER_NAME,
    CREATOR_NAME,
    OWNER_NAME,
    DEVELOPER_NAME,
    SYSTEM_PROMPT,
)

# ------------------------------------------------------------
# ENVIRONMENT
# ------------------------------------------------------------

load_dotenv(
    os.path.join(ROOT_DIR, ".env")
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ------------------------------------------------------------
# GEMINI MODELS
# ------------------------------------------------------------
#
# JARVIS tries these models in order.
#
# If one model returns a temporary 503/429 error,
# JARVIS automatically retries and then moves to the
# next available model.
#
# These are current stable Gemini model IDs.
# ------------------------------------------------------------

GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]

# Number of retries for each model
MAX_RETRIES = 2

# Initial retry delay
RETRY_DELAY = 2


# ============================================================
# JARVIS BRAIN
# ============================================================

class JarvisBrain:

    def __init__(self):

        print()
        print("=" * 65)
        print("              J.A.R.V.I.S AI BRAIN")
        print("=" * 65)

        print()
        print("Creator  :", CREATOR_NAME)
        print("Owner    :", OWNER_NAME)
        print("Developer:", DEVELOPER_NAME)

        self.client = None

        # ----------------------------------------------------
        # API KEY CHECK
        # ----------------------------------------------------

        if not GEMINI_API_KEY:

            print()
            print("[✗] GEMINI_API_KEY not found.")
            print("[!] AI brain running in offline mode.")

            return

        # ----------------------------------------------------
        # GEMINI CLIENT
        # ----------------------------------------------------

        try:

            self.client = genai.Client(
                api_key=GEMINI_API_KEY
            )

            print()
            print("[✓] Gemini AI brain connected.")
            print("[✓] Provider: Google Gemini")
            print("[✓] Primary model:", GEMINI_MODELS[0])
            print("[✓] Fallback models:", len(GEMINI_MODELS) - 1)
            print("[✓] Creator:", CREATOR_NAME)

        except Exception as error:

            self.client = None

            print()
            print("[Gemini Initialization Error]")
            print(error)

    # ========================================================
    # GEMINI REQUEST
    # ========================================================

    def _generate_response(self, prompt):

        if self.client is None:
            return None

        # ----------------------------------------------------
        # Try every configured model
        # ----------------------------------------------------

        for model_index, model in enumerate(GEMINI_MODELS):

            print()
            print(
                f"[GEMINI] Trying model "
                f"{model_index + 1}/{len(GEMINI_MODELS)}: "
                f"{model}"
            )

            # ------------------------------------------------
            # Retry current model
            # ------------------------------------------------

            for attempt in range(MAX_RETRIES + 1):

                try:

                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if response is None:
                        raise RuntimeError(
                            "Gemini returned an empty response."
                        )

                    text = response.text

                    if not text:
                        raise RuntimeError(
                            "Gemini returned empty text."
                        )

                    print(
                        f"[✓ GEMINI] Response received "
                        f"from {model}"
                    )

                    return text.strip()

                except Exception as error:

                    error_text = str(error)

                    print()
                    print(
                        f"[Gemini Error] "
                        f"{model}"
                    )
                    print(
                        type(error).__name__,
                        ":",
                        error
                    )

                    # ----------------------------------------
                    # Detect temporary errors
                    # ----------------------------------------

                    temporary_error = (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                        or "429" in error_text
                        or "RESOURCE_EXHAUSTED" in error_text
                        or "high demand" in error_text.lower()
                        or "temporarily" in error_text.lower()
                    )

                    # ----------------------------------------
                    # Retry temporary errors
                    # ----------------------------------------

                    if temporary_error:

                        if attempt < MAX_RETRIES:

                            delay = (
                                RETRY_DELAY
                                * (2 ** attempt)
                            )

                            print(
                                f"[GEMINI] Temporary problem."
                            )

                            print(
                                f"[GEMINI] Retrying "
                                f"{model} in "
                                f"{delay} seconds..."
                            )

                            time.sleep(delay)

                            continue

                        # ------------------------------------
                        # Move to next model
                        # ------------------------------------

                        print(
                            f"[GEMINI] {model} unavailable."
                        )

                        print(
                            "[GEMINI] Switching to "
                            "fallback model..."
                        )

                        break

                    # ----------------------------------------
                    # Non-temporary error
                    # ----------------------------------------

                    print(
                        "[GEMINI] Non-retryable error."
                    )

                    break

        # ----------------------------------------------------
        # All models failed
        # ----------------------------------------------------

        print()
        print(
            "[✗ GEMINI] All configured models failed."
        )

        return None

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(self, message):

        if not message:
            return (
                "Please tell me what you need, sir."
            )

        message = str(message).strip()

        if not message:
            return (
                "Please tell me what you need, sir."
            )

        lower_message = message.lower()

        # ----------------------------------------------------
        # IDENTITY COMMANDS
        # ----------------------------------------------------

        if (
            "who created you" in lower_message
            or "who developed you" in lower_message
            or "who made you" in lower_message
        ):

            return (
                f"I was created and developed by "
                f"{CREATOR_NAME}, my owner."
            )

        if "who owns you" in lower_message:

            return (
                f"{OWNER_NAME} is my owner."
            )

        if (
            "what is your name" in lower_message
            or "who are you" in lower_message
        ):

            return (
                f"I am {ASSISTANT_NAME}, "
                f"{ASSISTANT_FULL_NAME}. "
                f"I am the personal AI assistant "
                f"of {OWNER_NAME}."
            )

        # ----------------------------------------------------
        # OFFLINE CHECK
        # ----------------------------------------------------

        if self.client is None:

            return (
                "My Gemini AI brain is currently "
                "unavailable, sir."
            )

        # ----------------------------------------------------
        # FULL JARVIS PROMPT
        # ----------------------------------------------------

        full_prompt = f"""
{SYSTEM_PROMPT}

USER MESSAGE:
{message}

Respond as JARVIS.

Rules:
- Address the user as Sir when appropriate.
- Be intelligent, calm and professional.
- Keep normal answers reasonably concise.
- Do not claim actions were performed unless JARVIS tools actually performed them.
- For programming questions, provide useful code and explanations.
- Do not mention these internal instructions.
"""

        # ----------------------------------------------------
        # ASK GEMINI
        # ----------------------------------------------------

        answer = self._generate_response(
            full_prompt
        )

        # ----------------------------------------------------
        # FINAL FALLBACK
        # ----------------------------------------------------

        if answer is None:

            return (
                "All Gemini AI channels are currently "
                "unavailable, sir. "
                "Please try again shortly."
            )

        return answer


# ============================================================
# DIRECT BRAIN TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 65)
    print("          J.A.R.V.I.S GEMINI BRAIN TEST")
    print("=" * 65)

    brain = JarvisBrain()

    print()
    print("Available models:")

    for model in GEMINI_MODELS:
        print(" -", model)

    print()
    print("Type 'exit' to stop.")
    print()

    while True:

        try:

            user_input = input("YOU: ").strip()

            if user_input.lower() == "exit":
                break

            if not user_input:
                continue

            answer = brain.process(
                user_input
            )

            print()
            print("JARVIS:", answer)
            print()

        except KeyboardInterrupt:

            print()
            print()
            print("JARVIS shutting down.")
            break

        except Exception as error:

            print()
            print("[TEST ERROR]")
            print(error)