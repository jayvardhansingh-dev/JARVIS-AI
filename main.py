# ============================================================
# J.A.R.V.I.S MAIN
# Full Voice Mode
# ============================================================

import os
import sys
import re

# ------------------------------------------------------------
# ROOT PATH
# ------------------------------------------------------------

JARVIS_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

if JARVIS_ROOT not in sys.path:
    sys.path.insert(0, JARVIS_ROOT)


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

from config import (
    ASSISTANT_NAME,
    WAKE_WORD,
    STARTUP_MESSAGE
)


# ------------------------------------------------------------
# CORE
# ------------------------------------------------------------

from core.brain import JarvisBrain
from core.memory import JarvisMemory
from core.command_engine import JarvisCommandEngine


# ------------------------------------------------------------
# TOOLS
# ------------------------------------------------------------

from tools.computer import JarvisComputer
from tools.browser import JarvisBrowser
from tools.system import JarvisSystem


# ------------------------------------------------------------
# VOICE
# ------------------------------------------------------------

from voice.listen import JarvisListener
from voice.speak import JarvisSpeaker


# ============================================================
# JARVIS
# ============================================================

class Jarvis:

    def __init__(self):

        print("\n" + "=" * 60)
        print("              J.A.R.V.I.S")
        print("       Just A Rather Very Intelligent System")
        print("=" * 60)

        # ----------------------------------------------------
        # LOAD AI
        # ----------------------------------------------------

        print("\n[1/7] Loading AI brain...")
        self.brain = JarvisBrain()

        # ----------------------------------------------------
        # LOAD MEMORY
        # ----------------------------------------------------

        print("[2/7] Loading memory...")
        self.memory = JarvisMemory()

        # ----------------------------------------------------
        # LOAD COMPUTER
        # ----------------------------------------------------

        print("[3/7] Loading computer...")
        self.computer = JarvisComputer()

        # ----------------------------------------------------
        # LOAD BROWSER
        # ----------------------------------------------------

        print("[4/7] Loading browser...")
        self.browser = JarvisBrowser()

        # ----------------------------------------------------
        # LOAD SYSTEM
        # ----------------------------------------------------

        print("[5/7] Loading system...")
        self.system = JarvisSystem()

        # ----------------------------------------------------
        # LOAD MICROPHONE
        # ----------------------------------------------------

        print("[6/7] Loading microphone...")
        self.listener = JarvisListener()

        # ----------------------------------------------------
        # LOAD SPEAKER
        # ----------------------------------------------------

        print("[7/7] Loading speaker...")
        self.speaker = JarvisSpeaker()

        # ----------------------------------------------------
        # COMMAND ENGINE
        # ----------------------------------------------------

        self.engine = JarvisCommandEngine(
            brain=self.brain,
            memory=self.memory,
            computer=self.computer,
            browser=self.browser,
            system=self.system
        )

        print("\n[✓] All systems initialized.")
        print("[✓] JARVIS is online.")


    # ========================================================
    # CLEAN TEXT FOR SPEECH
    # ========================================================

    def clean_for_speech(self, text):

        if not text:
            return ""

        text = str(text)

        # ----------------------------------------------------
        # Remove code blocks
        # ----------------------------------------------------

        text = re.sub(
            r"```[\s\S]*?```",
            "The code is displayed in the response.",
            text
        )

        # ----------------------------------------------------
        # Remove inline code markers
        # ----------------------------------------------------

        text = re.sub(
            r"`([^`]*)`",
            r"\1",
            text
        )

        # ----------------------------------------------------
        # Remove markdown headings
        # ----------------------------------------------------

        text = re.sub(
            r"#{1,6}\s*",
            "",
            text
        )

        # ----------------------------------------------------
        # Remove bold / italic markers
        # ----------------------------------------------------

        text = text.replace("**", "")
        text = text.replace("__", "")
        text = text.replace("*", "_")

        # ----------------------------------------------------
        # Markdown links
        # ----------------------------------------------------

        text = re.sub(
            r"\[([^\]]+)\]\([^)]+\)",
            r"\1",
            text
        )

        # ----------------------------------------------------
        # Remove URLs
        # ----------------------------------------------------

        text = re.sub(
            r"https?://\S+",
            "",
            text
        )

        # ----------------------------------------------------
        # Remove unnecessary symbols
        # ----------------------------------------------------

        symbols = [
            "•",
            "→",
            "✓",
            "✅",
            "🔹",
            "🔸",
            "⭐",
            "🚀"
        ]

        for symbol in symbols:
            text = text.replace(symbol, "")

        # ----------------------------------------------------
        # Convert common markdown separators
        # ----------------------------------------------------

        text = text.replace("---", " ")
        text = text.replace("###", " ")

        # ----------------------------------------------------
        # Clean whitespace
        # ----------------------------------------------------

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text


    # ========================================================
    # PREPARE FULL SPEECH
    # ========================================================

    def prepare_speech(self, text):

        clean = self.clean_for_speech(text)

        if not clean:
            return ""

        # ====================================================
        # NO WORD LIMIT
        # ====================================================
        #
        # JARVIS will speak the COMPLETE response.
        #
        # ====================================================

        return clean


    # ========================================================
    # SPEAK
    # ========================================================

    def speak(self, text):

        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        # ----------------------------------------------------
        # Print complete response
        # ----------------------------------------------------

        print(
            f"\n{ASSISTANT_NAME}: {text}"
        )

        # ----------------------------------------------------
        # Prepare complete response for speech
        # ----------------------------------------------------

        speech_text = self.prepare_speech(text)

        if not speech_text:
            return

        print(
            "\n[🔊 JARVIS SPEAKING]"
        )

        print(
            speech_text
        )

        # ----------------------------------------------------
        # Speak
        # ----------------------------------------------------

        try:

            self.speaker.speak(
                speech_text
            )

            print(
                "[✓] Speech finished."
            )

        except Exception as e:

            print(
                f"[Speaker Error] "
                f"{type(e).__name__}: {e}"
            )


    # ========================================================
    # MAIN LOOP
    # ========================================================

    def run(self):

        # ----------------------------------------------------
        # STARTUP
        # ----------------------------------------------------

        self.speak(
            STARTUP_MESSAGE
        )

        print("\n" + "-" * 60)

        print(
            "JARVIS is ready."
        )

        print(
            f"Wake word: {WAKE_WORD}"
        )

        print(
            "Say 'Jarvis' followed by a command."
        )

        print(
            "Say 'Jarvis' followed by your question."
        )

        print(
            "Say 'shutdown Jarvis' to exit."
        )

        print("-" * 60)


        # ====================================================
        # LISTENING LOOP
        # ====================================================

        while True:

            try:

                # ------------------------------------------------
                # LISTEN
                # ------------------------------------------------

                text = self.listener.listen()

                if not text:
                    continue

                print(
                    f"\nYOU: {text}"
                )


                # ------------------------------------------------
                # CHECK WAKE WORD
                # ------------------------------------------------

                if (
                    WAKE_WORD.lower()
                    not in text.lower()
                ):

                    print(
                        f"[Waiting for wake word: "
                        f"{WAKE_WORD}]"
                    )

                    continue


                # ------------------------------------------------
                # REMOVE WAKE WORD
                # ------------------------------------------------

                command = re.sub(
                    rf"\b{re.escape(WAKE_WORD)}\b",
                    "",
                    text,
                    flags=re.IGNORECASE
                ).strip()

                command = command.strip(
                    " ,.!?"
                )


                # ------------------------------------------------
                # ONLY WAKE WORD
                # ------------------------------------------------

                if not command:

                    self.speak(
                        "Yes, sir. I'm listening."
                    )

                    continue


                # ------------------------------------------------
                # DISPLAY COMMAND
                # ------------------------------------------------

                print(
                    f"\nJARVIS COMMAND: {command}"
                )


                # ------------------------------------------------
                # SEND TO COMMAND ENGINE
                # ------------------------------------------------

                response = self.engine.process(
                    command
                )

                print(
                    "[DEBUG] Engine response received."
                )


                # ------------------------------------------------
                # EXIT
                # ------------------------------------------------

                if response == "__EXIT__":

                    self.speak(
                        "Shutting down JARVIS. "
                        "Goodbye, sir."
                    )

                    break


                # ------------------------------------------------
                # SPEAK RESPONSE
                # ------------------------------------------------

                if response:

                    self.speak(
                        response
                    )

                else:

                    self.speak(
                        "I don't have a response "
                        "for that yet, sir."
                    )


            # ====================================================
            # CTRL+C
            # ====================================================

            except KeyboardInterrupt:

                print(
                    "\n\nJARVIS interrupted by user."
                )

                break


            # ====================================================
            # ERROR HANDLING
            # ====================================================

            except Exception as e:

                print(
                    f"\n[JARVIS ERROR] "
                    f"{type(e).__name__}: {e}"
                )

                try:

                    self.speak(
                        "I'm sorry, sir. "
                        "Something went wrong."
                    )

                except Exception:

                    pass


        # ====================================================
        # CLEANUP
        # ====================================================

        print(
            "\n[✓] Cleaning up..."
        )

        try:
            self.memory.close()
        except Exception:
            pass

        try:
            self.listener.close()
        except Exception:
            pass

        try:
            self.speaker.stop()
        except Exception:
            pass

        print(
            "[✓] JARVIS offline."
        )


# ============================================================
# START JARVIS
# ============================================================

if __name__ == "__main__":

    jarvis = Jarvis()

    jarvis.run()