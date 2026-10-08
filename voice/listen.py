# voice/listen.py

import os
import sys

# Add JARVIS root directory to Python path
JARVIS_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if JARVIS_ROOT not in sys.path:
    sys.path.insert(0, JARVIS_ROOT)

import speech_recognition as sr

from config import WAKE_WORD


class JarvisListener:

    def __init__(self):

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    # ==========================================
    # CALIBRATE
    # ==========================================

    def calibrate(self):

        print("JARVIS: Calibrating microphone...")

        try:

            with self.microphone as source:

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

            print("JARVIS: Microphone ready.")

        except Exception as error:

            print(
                f"JARVIS: Microphone calibration failed: {error}"
            )

    # ==========================================
    # LISTEN
    # ==========================================

    def listen(self):

        try:

            with self.microphone as source:

                print("\n🎤 JARVIS is listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            print("JARVIS: Processing...")

            text = self.recognizer.recognize_google(
                audio
            )

            text = text.strip()

            print(f"You: {text}")

            return text

        except sr.WaitTimeoutError:

            print("JARVIS: No speech detected.")
            return None

        except sr.UnknownValueError:

            print("JARVIS: I couldn't understand that.")
            return None

        except sr.RequestError as error:

            print(
                f"JARVIS: Speech service error: {error}"
            )

            return None

        except Exception as error:

            print(
                f"JARVIS: Microphone error: {error}"
            )

            return None

    # ==========================================
    # WAKE WORD
    # ==========================================

    def wait_for_wake_word(self):

        print(
            f'\nJARVIS: Say "{WAKE_WORD}" to activate.'
        )

        while True:

            text = self.listen()

            if not text:
                continue

            if WAKE_WORD.lower() in text.lower():

                print(
                    "JARVIS: Wake word detected."
                )

                return True


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("       JARVIS LISTENER TEST")
    print("=" * 50)

    listener = JarvisListener()

    listener.calibrate()

    print("\nSay something...")

    result = listener.listen()

    if result:

        print(
            f"\nJARVIS received: {result}"
        )