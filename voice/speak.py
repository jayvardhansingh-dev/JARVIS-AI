# ============================================================
# J.A.R.V.I.S — NEURAL VOICE SYSTEM
# Microsoft Edge Neural TTS
# Indian Male Voice: en-IN-PrabhatNeural
# ============================================================

import asyncio
import os
import re
import tempfile

import edge_tts
import pygame


# ------------------------------------------------------------
# JARVIS VOICE SETTINGS
# ------------------------------------------------------------

VOICE_NAME = "en-IN-PrabhatNeural"

# Slightly slower for a more controlled AI-assistant delivery
VOICE_SPEED = "-8%"

# Slightly deeper
VOICE_PITCH = "-2Hz"

# Maximum volume
VOICE_VOLUME = 1.0


class JarvisSpeaker:
    """JARVIS neural text-to-speech system."""

    def __init__(self):
        self.voice = VOICE_NAME
        self.speed = VOICE_SPEED
        self.pitch = VOICE_PITCH

        self.initialized = False

        try:
            pygame.mixer.init()
            self.initialized = True

            print("[✓] JARVIS neural voice initialized.")
            print(f"[✓] Voice: {self.voice}")

        except Exception as e:
            print(f"[!] Audio initialization error: {e}")

    # --------------------------------------------------------
    # CLEAN TEXT
    # --------------------------------------------------------

    def clean_text(self, text):
        """Remove unnecessary characters before speech."""

        if not text:
            return ""

        text = str(text)

        # Remove markdown formatting
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        text = re.sub(r"`(.*?)`", r"\1", text)

        # Remove URLs
        text = re.sub(r"https?://\S+", "", text)

        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------------------------
    # GENERATE AUDIO
    # --------------------------------------------------------

    async def _generate_audio(self, text, output_file):

        communicator = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.speed,
            pitch=self.pitch,
        )

        await communicator.save(output_file)

    # --------------------------------------------------------
    # PLAY AUDIO
    # --------------------------------------------------------

    def _play_audio(self, filename):

        try:

            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(VOICE_VOLUME)

            pygame.mixer.music.play()

            # Wait until speech finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(20)

        except Exception as e:

            print(f"[!] Audio playback error: {e}")

    # --------------------------------------------------------
    # SPEAK
    # --------------------------------------------------------

    def speak(self, text):

        text = self.clean_text(text)

        if not text:
            return

        print(f"JARVIS: {text}")

        if not self.initialized:
            print("[!] Audio system is not initialized.")
            return

        temp_file = None

        try:

            # Create temporary MP3
            fd, temp_file = tempfile.mkstemp(
                suffix=".mp3",
                prefix="jarvis_"
            )

            os.close(fd)

            # Generate speech
            asyncio.run(
                self._generate_audio(
                    text,
                    temp_file
                )
            )

            # Play speech
            self._play_audio(temp_file)

        except Exception as e:

            print(f"[!] Neural TTS error: {e}")

        finally:

            # Clean temporary file
            try:

                if temp_file and os.path.exists(temp_file):
                    os.remove(temp_file)

            except Exception:
                pass

    # --------------------------------------------------------
    # TEST VOICE
    # --------------------------------------------------------

    def test(self):

        print()
        print("=" * 55)
        print("        J.A.R.V.I.S NEURAL VOICE TEST")
        print("=" * 55)
        print(f"Voice : {self.voice}")
        print(f"Speed : {self.speed}")
        print(f"Pitch : {self.pitch}")
        print()

        self.speak(
            "Good evening, sir. "
            "I am JARVIS. "
            "Your personal artificial intelligence system. "
            "How may I assist you?"
        )

        print()
        print("[✓] Neural voice test completed.")

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    def stop(self):

        try:

            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()

            self.initialized = False

            print("[VOICE] Neural speaker stopped.")

        except Exception as e:

            print(f"[!] Speaker shutdown error: {e}")


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    speaker = JarvisSpeaker()

    try:

        speaker.test()

    except KeyboardInterrupt:

        print("\n[VOICE] Test interrupted.")

    finally:

        speaker.stop()