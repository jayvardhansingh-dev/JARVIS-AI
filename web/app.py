# ============================================================
# J.A.R.V.I.S — PREMIUM LOCAL AI CONTROL CENTER
# ============================================================
# Developed by Jayvardhan Singh
# Version 4.0
# ============================================================

import os
import sys
import platform
import threading
import atexit
import re
import webbrowser

from datetime import datetime

import psutil

from flask import Flask, render_template, jsonify, request


# ============================================================
# PROJECT PATH
# ============================================================

WEB_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(WEB_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

try:
    from core.brain import JarvisBrain
except Exception as error:
    print("[BRAIN IMPORT ERROR]", error)
    JarvisBrain = None


try:
    from core.memory import JarvisMemory
except Exception as error:
    print("[MEMORY IMPORT ERROR]", error)
    JarvisMemory = None


try:
    from core.command_engine import JarvisCommandEngine
except Exception as error:
    print("[COMMAND ENGINE IMPORT ERROR]", error)
    JarvisCommandEngine = None


try:
    from tools.computer import JarvisComputer
except Exception as error:
    print("[COMPUTER IMPORT ERROR]", error)
    JarvisComputer = None


try:
    from tools.browser import JarvisBrowser
except Exception as error:
    print("[BROWSER IMPORT ERROR]", error)
    JarvisBrowser = None


try:
    from tools.system import JarvisSystem
except Exception as error:
    print("[SYSTEM IMPORT ERROR]", error)
    JarvisSystem = None


try:
    from voice.speak import JarvisSpeaker
except Exception as error:
    print("[VOICE IMPORT ERROR]", error)
    JarvisSpeaker = None


# ============================================================
# FLASK
# ============================================================

app = Flask(
    __name__,
    template_folder=os.path.join(
        WEB_DIR,
        "templates"
    ),
    static_folder=os.path.join(
        WEB_DIR,
        "static"
    )
)


# ============================================================
# INFORMATION
# ============================================================

APP_NAME = "J.A.R.V.I.S"

APP_FULL_NAME = (
    "JUST A RATHER VERY INTELLIGENT SYSTEM"
)

DEVELOPER = "Jayvardhan Singh"

VERSION = "4.0"

MODE = "LOCAL AI CONTROL CENTER"


# ============================================================
# GLOBAL OBJECTS
# ============================================================

brain = None
memory = None
computer = None
browser = None
system = None
engine = None
speaker = None


# ============================================================
# INITIALIZE BRAIN
# ============================================================

if JarvisBrain:

    try:
        brain = JarvisBrain()
        print("[✓] AI BRAIN ONLINE")

    except Exception as error:
        print("[BRAIN ERROR]", error)


# ============================================================
# INITIALIZE MEMORY
# ============================================================

if JarvisMemory:

    try:
        memory = JarvisMemory()
        print("[✓] MEMORY ONLINE")

    except Exception as error:
        print("[MEMORY ERROR]", error)


# ============================================================
# INITIALIZE COMPUTER
# ============================================================

if JarvisComputer:

    try:
        computer = JarvisComputer()
        print("[✓] COMPUTER CONTROL ONLINE")

    except Exception as error:
        print("[COMPUTER ERROR]", error)


# ============================================================
# INITIALIZE BROWSER
# ============================================================

if JarvisBrowser:

    try:
        browser = JarvisBrowser()
        print("[✓] BROWSER CONTROL ONLINE")

    except Exception as error:
        print("[BROWSER ERROR]", error)


# ============================================================
# INITIALIZE SYSTEM
# ============================================================

if JarvisSystem:

    try:
        system = JarvisSystem()
        print("[✓] SYSTEM CONTROL ONLINE")

    except Exception as error:
        print("[SYSTEM ERROR]", error)


# ============================================================
# INITIALIZE COMMAND ENGINE
# ============================================================

if JarvisCommandEngine:

    try:

        engine = JarvisCommandEngine(
            brain=brain,
            memory=memory,
            computer=computer,
            browser=browser,
            system=system
        )

        print("[✓] COMMAND ENGINE ONLINE")

    except Exception as error:

        print("[COMMAND ENGINE ERROR]")
        print(error)


# ============================================================
# INITIALIZE VOICE
# ============================================================

if JarvisSpeaker:

    try:

        speaker = JarvisSpeaker()

        print("[✓] WINDOWS VOICE ONLINE")

    except Exception as error:

        print("[VOICE ERROR]", error)


# ============================================================
# VOICE LOCK
# ============================================================

speaker_lock = threading.Lock()


# ============================================================
# CLEAN VOICE TEXT
# ============================================================

def clean_for_voice(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"```[\s\S]*?```",
        "I have provided the code in the response.",
        text
    )

    text = re.sub(
        r"`([^`]*)`",
        r"\1",
        text
    )

    text = re.sub(
        r"#+\s*",
        "",
        text
    )

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")

    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    text = re.sub(
        r"https?://\S+",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# ASYNC SPEECH
# ============================================================

def speak_async(text):

    if speaker is None:
        return

    text = clean_for_voice(text)

    if not text:
        return

    def worker():

        try:

            with speaker_lock:
                speaker.speak(text)

        except Exception as error:

            print(
                "[VOICE ERROR]",
                type(error).__name__,
                error
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# ============================================================
# NORMALIZE COMMAND
# ============================================================

def normalize_command(text):

    text = str(text).lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = text.strip(
        " .,!?;:"
    )

    # Remove wake word if user says it
    text = re.sub(
        r"^jarvis[\s,.:;-]*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ============================================================
# DIRECT LOCAL COMMAND ROUTER
# ============================================================

def execute_local_command(user_text):

    """
    Executes known Windows/browser commands directly.

    Returns:
        (handled, response)
    """

    command = normalize_command(
        user_text
    )

    print(
        "[LOCAL COMMAND CHECK]",
        command
    )


    # ========================================================
    # YOUTUBE
    # ========================================================

    if command in (
        "open youtube",
        "launch youtube",
        "start youtube",
        "go to youtube",
        "open youtube website"
    ):

        try:

            if browser and hasattr(
                browser,
                "open_youtube"
            ):

                result = browser.open_youtube()

                if result is False:
                    return True, "I couldn't open YouTube, sir."

            else:

                webbrowser.open(
                    "https://www.youtube.com"
                )

            return True, "Opening YouTube, sir."


        except Exception as error:

            print(
                "[YOUTUBE ERROR]",
                error
            )

            return True, (
                "I couldn't open YouTube, sir."
            )


    # ========================================================
    # GOOGLE
    # ========================================================

    if command in (
        "open google",
        "launch google",
        "start google",
        "go to google"
    ):

        try:

            if browser and hasattr(
                browser,
                "open_google"
            ):

                result = browser.open_google()

                if result is False:
                    return True, "I couldn't open Google, sir."

            else:

                webbrowser.open(
                    "https://www.google.com"
                )

            return True, "Opening Google, sir."


        except Exception as error:

            print(
                "[GOOGLE ERROR]",
                error
            )

            return True, (
                "I couldn't open Google, sir."
            )


    # ========================================================
    # GITHUB
    # ========================================================

    if command in (
        "open github",
        "launch github",
        "start github",
        "go to github"
    ):

        try:

            if browser and hasattr(
                browser,
                "open_github"
            ):

                result = browser.open_github()

                if result is False:
                    return True, "I couldn't open GitHub, sir."

            else:

                webbrowser.open(
                    "https://github.com"
                )

            return True, "Opening GitHub, sir."


        except Exception as error:

            print(
                "[GITHUB ERROR]",
                error
            )

            return True, (
                "I couldn't open GitHub, sir."
            )


    # ========================================================
    # CHATGPT
    # ========================================================

    if command in (
        "open chatgpt",
        "launch chatgpt",
        "start chatgpt"
    ):

        try:

            if browser and hasattr(
                browser,
                "open_chatgpt"
            ):

                result = browser.open_chatgpt()

                if result is False:
                    return True, "I couldn't open ChatGPT, sir."

            else:

                webbrowser.open(
                    "https://chatgpt.com"
                )

            return True, "Opening ChatGPT, sir."


        except Exception as error:

            print(
                "[CHATGPT ERROR]",
                error
            )

            return True, (
                "I couldn't open ChatGPT, sir."
            )


    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    google_match = re.match(
        r"^(?:search google for|google search for|search for)\s+(.+)$",
        command
    )

    if google_match:

        query = google_match.group(1).strip()

        try:

            if browser and hasattr(
                browser,
                "search_google"
            ):

                browser.search_google(
                    query
                )

            else:

                webbrowser.open(
                    "https://www.google.com/search?q="
                    + query.replace(" ", "+")
                )

            return True, (
                f"Searching Google for {query}, sir."
            )


        except Exception as error:

            print(
                "[GOOGLE SEARCH ERROR]",
                error
            )

            return True, (
                "I couldn't perform the Google search, sir."
            )


    # ========================================================
    # YOUTUBE SEARCH
    # ========================================================

    youtube_match = re.match(
        r"^(?:search youtube for|youtube search for)\s+(.+)$",
        command
    )

    if youtube_match:

        query = youtube_match.group(1).strip()

        try:

            if browser and hasattr(
                browser,
                "search_youtube"
            ):

                browser.search_youtube(
                    query
                )

            else:

                webbrowser.open(
                    "https://www.youtube.com/results?search_query="
                    + query.replace(" ", "+")
                )

            return True, (
                f"Searching YouTube for {query}, sir."
            )


        except Exception as error:

            print(
                "[YOUTUBE SEARCH ERROR]",
                error
            )

            return True, (
                "I couldn't perform the YouTube search, sir."
            )


    # ========================================================
    # SCREENSHOT
    # ========================================================

    if command in (
        "take screenshot",
        "take a screenshot",
        "screenshot",
        "capture screen",
        "capture screenshot"
    ):

        try:

            if computer and hasattr(
                computer,
                "screenshot"
            ):

                result = computer.screenshot()

                print(
                    "[SCREENSHOT]",
                    result
                )

                return True, (
                    "Screenshot captured, sir."
                )

            return True, (
                "Screenshot control is unavailable, sir."
            )


        except Exception as error:

            print(
                "[SCREENSHOT ERROR]",
                error
            )

            return True, (
                "I couldn't capture the screen, sir."
            )


    # ========================================================
    # VOLUME UP
    # ========================================================

    if command in (
        "volume up",
        "increase volume",
        "turn volume up",
        "louder"
    ):

        try:

            if computer:

                computer.volume_up()

            return True, "Increasing the volume, sir."


        except Exception as error:

            print(
                "[VOLUME ERROR]",
                error
            )

            return True, (
                "I couldn't change the volume, sir."
            )


    # ========================================================
    # VOLUME DOWN
    # ========================================================

    if command in (
        "volume down",
        "decrease volume",
        "turn volume down",
        "lower volume"
    ):

        try:

            if computer:

                computer.volume_down()

            return True, "Decreasing the volume, sir."


        except Exception as error:

            print(
                "[VOLUME ERROR]",
                error
            )

            return True, (
                "I couldn't change the volume, sir."
            )


    # ========================================================
    # MUTE
    # ========================================================

    if command in (
        "mute",
        "mute volume",
        "mute sound"
    ):

        try:

            if computer:

                computer.volume_mute()

            return True, "Volume muted, sir."


        except Exception as error:

            print(
                "[MUTE ERROR]",
                error
            )

            return True, (
                "I couldn't mute the volume, sir."
            )


    # ========================================================
    # LOCK COMPUTER
    # ========================================================

    if command in (
        "lock computer",
        "lock my computer",
        "lock pc",
        "lock the computer"
    ):

        try:

            if computer and hasattr(
                computer,
                "lock_computer"
            ):

                computer.lock_computer()

            elif system and hasattr(
                system,
                "lock_computer"
            ):

                system.lock_computer()

            else:

                return True, (
                    "Computer locking is unavailable, sir."
                )

            return True, (
                "Locking the computer, sir."
            )


        except Exception as error:

            print(
                "[LOCK ERROR]",
                error
            )

            return True, (
                "I couldn't lock the computer, sir."
            )


    # ========================================================
    # TIME
    # ========================================================

    if command in (
        "what time is it",
        "what is the time",
        "tell me the time",
        "current time",
        "time"
    ):

        try:

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            return True, (
                f"The current time is {current_time}, sir."
            )

        except Exception:

            return True, (
                "I couldn't determine the time, sir."
            )


    # ========================================================
    # DATE
    # ========================================================

    if command in (
        "what is the date",
        "what date is it",
        "today's date",
        "current date",
        "date"
    ):

        try:

            current_date = datetime.now().strftime(
                "%d %B %Y"
            )

            return True, (
                f"Today's date is {current_date}, sir."
            )

        except Exception:

            return True, (
                "I couldn't determine the date, sir."
            )


    # ========================================================
    # CPU
    # ========================================================

    if command in (
        "cpu usage",
        "cpu status",
        "what is my cpu usage",
        "check cpu"
    ):

        try:

            cpu = psutil.cpu_percent(
                interval=0.2
            )

            return True, (
                f"CPU usage is {round(cpu)} percent, sir."
            )

        except Exception:

            return True, (
                "I couldn't read the CPU usage, sir."
            )


    # ========================================================
    # RAM
    # ========================================================

    if command in (
        "ram usage",
        "memory usage",
        "ram status",
        "check ram"
    ):

        try:

            ram = psutil.virtual_memory().percent

            return True, (
                f"RAM usage is {round(ram)} percent, sir."
            )

        except Exception:

            return True, (
                "I couldn't read the RAM usage, sir."
            )


    # ========================================================
    # BATTERY
    # ========================================================

    if command in (
        "battery status",
        "check battery",
        "battery"
    ):

        try:

            battery = psutil.sensors_battery()

            if battery:

                return True, (
                    f"Battery level is "
                    f"{round(battery.percent)} percent, sir."
                )

            return True, (
                "This computer does not report battery information, sir."
            )

        except Exception:

            return True, (
                "I couldn't read the battery status, sir."
            )


    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    if command in (
        "system status",
        "computer status",
        "system information",
        "computer information",
        "check system"
    ):

        try:

            cpu = psutil.cpu_percent(
                interval=0.2
            )

            ram = psutil.virtual_memory().percent

            battery = psutil.sensors_battery()

            if battery:
                battery_text = (
                    f"{round(battery.percent)} percent"
                )
            else:
                battery_text = "not available"


            return True, (
                f"System is online, sir. "
                f"CPU usage is {round(cpu)} percent, "
                f"RAM usage is {round(ram)} percent, "
                f"and battery is {battery_text}."
            )

        except Exception:

            return True, (
                "I couldn't read the complete system status, sir."
            )


    # ========================================================
    # OPEN APPLICATION
    # ========================================================

    app_match = re.match(
        r"^(?:open|launch|start|run)\s+(.+)$",
        command
    )

    if app_match:

        app_name = app_match.group(1).strip()

        # Don't intercept known websites
        known_sites = (
            "youtube",
            "google",
            "github",
            "chatgpt"
        )

        if app_name not in known_sites:

            try:

                if computer and hasattr(
                    computer,
                    "open_app"
                ):

                    result = computer.open_app(
                        app_name
                    )

                    if result is False:

                        return True, (
                            f"I couldn't open {app_name}, sir."
                        )

                    return True, (
                        f"Opening {app_name}, sir."
                    )

            except Exception as error:

                print(
                    "[APP OPEN ERROR]",
                    error
                )

                return True, (
                    f"I couldn't open {app_name}, sir."
                )


    # ========================================================
    # NOT A DIRECT COMMAND
    # ========================================================

    return False, None


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        app_name=APP_NAME,
        app_full_name=APP_FULL_NAME,
        developer=DEVELOPER,
        version=VERSION,
        mode=MODE
    )


# ============================================================
# STATUS
# ============================================================

@app.route("/api/status")
def status():

    try:

        cpu = psutil.cpu_percent(
            interval=0.1
        )

        ram = psutil.virtual_memory().percent

        battery_info = (
            psutil.sensors_battery()
        )

        battery = (
            battery_info.percent
            if battery_info
            else None
        )

        now = datetime.now()

        return jsonify({

            "status": "ONLINE",

            "cpu": cpu,

            "ram": ram,

            "battery": battery,

            "time": now.strftime(
                "%H:%M:%S"
            ),

            "date": now.strftime(
                "%d %B %Y"
            ),

            "os": platform.system(),

            "developer": DEVELOPER,

            "version": VERSION,

            "mode": MODE,

            "voice": speaker is not None,

            "ai": brain is not None,

            "memory": memory is not None,

            "computer": computer is not None,

            "browser": browser is not None,

            "system_control": system is not None,

            "command_engine": engine is not None

        })


    except Exception as error:

        print(
            "[STATUS ERROR]",
            error
        )

        return jsonify({

            "status": "ERROR",

            "cpu": 0,

            "ram": 0,

            "battery": None,

            "time": "--:--:--",

            "date": "Unavailable",

            "os": platform.system(),

            "developer": DEVELOPER,

            "version": VERSION,

            "mode": MODE,

            "voice": False,

            "ai": False,

            "memory": False,

            "computer": False,

            "browser": False,

            "system_control": False,

            "command_engine": False

        }), 500


# ============================================================
# CHAT
# ============================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            message = ""

        else:

            message = data.get(
                "message",
                ""
            )


        message = str(
            message
        ).strip()


        if not message:

            response = (
                "Please enter a message, sir."
            )

            return jsonify({

                "success": False,

                "response": response,

                "reply": response,

                "spoken": False

            }), 400


        print()
        print(
            "=" * 70
        )

        print(
            "[WEB USER]"
        )

        print(
            message
        )


        # ====================================================
        # 1. DIRECT LOCAL COMMAND
        # ====================================================

        handled, local_response = (
            execute_local_command(
                message
            )
        )


        if handled:

            print(
                "[LOCAL COMMAND EXECUTED]"
            )

            print(
                local_response
            )


            speak_async(
                local_response
            )


            return jsonify({

                "success": True,

                "response": local_response,

                "reply": local_response,

                "spoken":
                    speaker is not None,

                "mode":
                    "LOCAL COMPUTER CONTROL",

                "command":
                    True

            })


        # ====================================================
        # 2. EXISTING COMMAND ENGINE
        # ====================================================

        if engine is not None:

            print(
                "[COMMAND ENGINE]"
            )

            response = engine.process(
                message
            )


        # ====================================================
        # 3. AI FALLBACK
        # ====================================================

        elif brain is not None:

            print(
                "[AI FALLBACK]"
            )

            response = brain.process(
                message
            )


        else:

            response = (
                "My AI systems are currently "
                "unavailable, sir."
            )


        # ====================================================
        # EXIT
        # ====================================================

        if response == "__EXIT__":

            response = (
                "Shutting down JARVIS. "
                "Goodbye, sir."
            )


        # ====================================================
        # CLEAN RESPONSE
        # ====================================================

        if response is None:

            response = (
                "I was unable to generate "
                "a response, sir."
            )


        response = str(
            response
        ).strip()


        if not response:

            response = (
                "I don't have a response "
                "for that yet, sir."
            )


        print(
            "[JARVIS]"
        )

        print(
            response
        )


        # ====================================================
        # VOICE
        # ====================================================

        speak_async(
            response
        )


        # ====================================================
        # RETURN
        # ====================================================

        return jsonify({

            "success": True,

            "response": response,

            "reply": response,

            "spoken":
                speaker is not None,

            "mode":
                "COMMAND ENGINE + AI",

            "developer":
                DEVELOPER,

            "version":
                VERSION

        })


    except Exception as error:

        print()
        print(
            "=" * 70
        )

        print(
            "[CHAT ERROR]"
        )

        print(
            type(error).__name__,
            ":",
            error
        )

        print(
            "=" * 70
        )


        response = (
            "I'm sorry, sir. "
            "Something went wrong."
        )


        speak_async(
            response
        )


        return jsonify({

            "success": False,

            "response": response,

            "reply": response,

            "spoken":
                speaker is not None,

            "mode":
                "ERROR",

            "error":
                str(error)

        }), 500


# ============================================================
# CLEAR CHAT
# ============================================================

@app.route(
    "/api/chat/clear",
    methods=["POST"]
)
def clear_chat():

    try:

        if brain is not None:

            if hasattr(
                brain,
                "clear_conversation"
            ):

                brain.clear_conversation()

            elif hasattr(
                brain,
                "conversation"
            ):

                brain.conversation = []


        return jsonify({

            "success": True,

            "message":
                "Conversation cleared."

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# MEMORY
# ============================================================

@app.route("/api/memory")
def get_memory():

    try:

        if memory is None:

            return jsonify({

                "success": False,

                "memories": []

            }), 500


        memories = memory.get_memories()


        return jsonify({

            "success": True,

            "memories": memories

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "memories": [],

            "error":
                str(error)

        }), 500


# ============================================================
# HEALTH
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({

        "healthy": True,

        "application":
            APP_NAME,

        "ai":
            brain is not None,

        "voice":
            speaker is not None,

        "memory":
            memory is not None,

        "computer":
            computer is not None,

        "browser":
            browser is not None,

        "system":
            system is not None,

        "command_engine":
            engine is not None,

        "local_control":
            True,

        "developer":
            DEVELOPER,

        "version":
            VERSION,

        "mode":
            MODE

    })


# ============================================================
# INFO
# ============================================================

@app.route("/api/info")
def info():

    return jsonify({

        "name":
            APP_NAME,

        "full_name":
            APP_FULL_NAME,

        "developer":
            DEVELOPER,

        "version":
            VERSION,

        "mode":
            MODE,

        "platform":
            platform.platform(),

        "python":
            platform.python_version(),

        "ai_available":
            brain is not None,

        "voice_available":
            speaker is not None,

        "memory_available":
            memory is not None,

        "computer_available":
            computer is not None,

        "browser_available":
            browser is not None,

        "system_available":
            system is not None,

        "command_engine_available":
            engine is not None,

        "local_commands":
            True

    })


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "success": False,

        "error":
            "Endpoint not found.",

        "application":
            APP_NAME

    }), 404


# ============================================================
# CLEANUP
# ============================================================

def cleanup():

    print(
        "\n[JARVIS] Shutting down..."
    )


    if speaker is not None:

        try:
            speaker.stop()
        except Exception:
            pass


    if memory is not None:

        try:
            memory.close()
        except Exception:
            pass


    print(
        "[✓] JARVIS stopped."
    )


atexit.register(
    cleanup
)


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "=" * 70
    )

    print(
        "                    J.A.R.V.I.S"
    )

    print(
        "          JUST A RATHER VERY"
    )

    print(
        "          INTELLIGENT SYSTEM"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Developer : {DEVELOPER}"
    )

    print(
        f"Version   : {VERSION}"
    )

    print(
        f"Mode      : {MODE}"
    )

    print()

    print(
        "AI              :",
        "ONLINE" if brain else "OFFLINE"
    )

    print(
        "Voice           :",
        "ONLINE" if speaker else "OFFLINE"
    )

    print(
        "Memory          :",
        "ONLINE" if memory else "OFFLINE"
    )

    print(
        "Computer Control:",
        "ONLINE" if computer else "OFFLINE"
    )

    print(
        "Browser Control :",
        "ONLINE" if browser else "OFFLINE"
    )

    print(
        "System Control  :",
        "ONLINE" if system else "OFFLINE"
    )

    print(
        "Command Engine  :",
        "ONLINE" if engine else "OFFLINE"
    )

    print(
        "Local Commands  : ONLINE"
    )

    print()

    print(
        "Dashboard : http://127.0.0.1:5000"
    )

    print()

    print(
        "=" * 70
    )

    print()


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True,

        use_reloader=False,

        threaded=True

    )