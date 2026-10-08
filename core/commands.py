# core/commands.py

import os
import subprocess
import webbrowser
import datetime
import platform
from pathlib import Path


class JarvisCommands:
    """
    Command engine for JARVIS.

    Handles basic computer and system actions.
    """

    def __init__(self):
        self.system = platform.system()

    # ==========================================
    # OPEN APPLICATION
    # ==========================================

    def open_application(self, application):

        application = application.lower().strip()

        applications = {

            "notepad": "notepad.exe",

            "calculator": "calc.exe",

            "paint": "mspaint.exe",

            "cmd": "cmd.exe",

            "command prompt": "cmd.exe",

            "explorer": "explorer.exe",

            "file explorer": "explorer.exe",
        }

        if application not in applications:
            return f"Sir, I don't know how to open {application} yet."

        try:

            subprocess.Popen(
                applications[application]
            )

            return f"Opening {application}, sir."

        except Exception as error:

            return f"Unable to open {application}: {error}"

    # ==========================================
    # OPEN WEBSITE
    # ==========================================

    def open_website(self, url):

        if not url.startswith(("http://", "https://")):

            url = "https://" + url

        try:

            webbrowser.open(url)

            return f"Opening {url}, sir."

        except Exception as error:

            return f"Unable to open the website: {error}"

    # ==========================================
    # GOOGLE SEARCH
    # ==========================================

    def search_google(self, query):

        if not query.strip():

            return "Sir, what should I search for?"

        search_url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        webbrowser.open(search_url)

        return f"Searching Google for {query}, sir."

    # ==========================================
    # OPEN YOUTUBE
    # ==========================================

    def open_youtube(self):

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "Opening YouTube, sir."

    # ==========================================
    # CURRENT TIME
    # ==========================================

    def get_time(self):

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return f"Sir, the current time is {current_time}."

    # ==========================================
    # CURRENT DATE
    # ==========================================

    def get_date(self):

        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return f"Today is {current_date}, sir."

    # ==========================================
    # SYSTEM INFORMATION
    # ==========================================

    def system_information(self):

        system_name = platform.system()
        system_version = platform.version()
        machine = platform.machine()
        processor = platform.processor()

        return (
            f"System: {system_name}\n"
            f"Version: {system_version}\n"
            f"Machine: {machine}\n"
            f"Processor: {processor}"
        )

    # ==========================================
    # OPEN FOLDER
    # ==========================================

    def open_folder(self, folder_path):

        path = Path(folder_path).expanduser()

        if not path.exists():

            return f"Sir, I couldn't find the folder {folder_path}."

        try:

            os.startfile(path)

            return f"Opening {folder_path}, sir."

        except Exception as error:

            return f"Unable to open the folder: {error}"

    # ==========================================
    # TAKE SCREENSHOT
    # ==========================================

    def take_screenshot(self):

        try:

            from PIL import ImageGrab

            screenshot = ImageGrab.grab()

            filename = (
                "jarvis_screenshot_"
                + datetime.datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
                + ".png"
            )

            screenshot.save(filename)

            return f"Screenshot saved as {filename}, sir."

        except ImportError:

            return (
                "Screenshot feature requires "
                "the Pillow package."
            )

        except Exception as error:

            return f"Unable to take screenshot: {error}"


# ==========================================
# TEST COMMAND SYSTEM
# ==========================================

if __name__ == "__main__":

    jarvis = JarvisCommands()

    print("=" * 50)
    print("       JARVIS COMMAND SYSTEM TEST")
    print("=" * 50)

    while True:

        print("\n1. Open Notepad")
        print("2. Open Calculator")
        print("3. Open YouTube")
        print("4. Google Search")
        print("5. Get Time")
        print("6. Get Date")
        print("7. System Information")
        print("8. Screenshot")
        print("9. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            print(jarvis.open_application("notepad"))

        elif choice == "2":

            print(jarvis.open_application("calculator"))

        elif choice == "3":

            print(jarvis.open_youtube())

        elif choice == "4":

            query = input("Search for: ")

            print(
                jarvis.search_google(query)
            )

        elif choice == "5":

            print(jarvis.get_time())

        elif choice == "6":

            print(jarvis.get_date())

        elif choice == "7":

            print(jarvis.system_information())

        elif choice == "8":

            print(jarvis.take_screenshot())

        elif choice == "9":

            print(
                "JARVIS: Command system shutting down, sir."
            )

            break

        else:

            print("JARVIS: Invalid command.")