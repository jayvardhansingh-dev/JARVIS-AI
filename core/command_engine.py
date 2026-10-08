# ============================================================
# J.A.R.V.I.S COMMAND ENGINE 2.0
# ============================================================

import re


class JarvisCommandEngine:

    def __init__(
        self,
        brain,
        memory,
        computer,
        browser,
        system
    ):
        self.brain = brain
        self.memory = memory
        self.computer = computer
        self.browser = browser
        self.system = system

    # ========================================================
    # MAIN COMMAND PROCESSOR
    # ========================================================

    def process(self, text):

        text = text.strip()

        if not text:
            return "I didn't hear anything, sir."

        print(f"\nYOU: {text}")

        lower = text.lower().strip()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if lower in [
            "exit",
            "quit",
            "shutdown jarvis",
            "stop jarvis",
            "goodbye",
            "go offline"
        ]:
            return "__EXIT__"

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        response = self.memory_command(text)

        if response:
            return response

        # ----------------------------------------------------
        # COMPUTER
        # ----------------------------------------------------

        response = self.computer_command(text)

        if response:
            return response

        # ----------------------------------------------------
        # BROWSER
        # ----------------------------------------------------

        response = self.browser_command(text)

        if response:
            return response

        # ----------------------------------------------------
        # SYSTEM
        # ----------------------------------------------------

        response = self.system_command(text)

        if response:
            return response

        # ----------------------------------------------------
        # AI BRAIN
        # ----------------------------------------------------

        try:
            response = self.brain.process(text)

            return response

        except Exception as e:
            print(f"[Brain Error] {e}")

            return (
                "I'm sorry, sir. "
                "I couldn't process that command."
            )

    # ========================================================
    # MEMORY COMMANDS
    # ========================================================

    def memory_command(self, text):

        lower = text.lower().strip()

        # ----------------------------------------------------
        # REMEMBER
        # ----------------------------------------------------

        patterns = [
            r"remember that (.+)",
            r"remember (.+)",
            r"save that (.+)",
            r"save this (.+)",
            r"store that (.+)"
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                memory_text = match.group(1).strip()

                if memory_text:

                    self.memory.remember(
                        memory_text
                    )

                    return (
                        "I've saved that to my memory, sir."
                    )

        # ----------------------------------------------------
        # SHOW MEMORIES
        # ----------------------------------------------------

        if (
            "what do you remember" in lower
            or "show my memories" in lower
            or "show memories" in lower
            or "list my memories" in lower
            or lower == "my memories"
        ):

            memories = self.memory.get_memories()

            if not memories:
                return (
                    "I don't have any saved memories yet, sir."
                )

            response = "Here are your memories, sir:\n"

            for item in memories[:10]:

                if isinstance(item, (tuple, list)):

                    if len(item) >= 2:
                        response += f"- {item[1]}\n"
                    else:
                        response += f"- {item[0]}\n"

                else:
                    response += f"- {item}\n"

            return response

        # ----------------------------------------------------
        # SEARCH MEMORY
        # ----------------------------------------------------

        match = re.search(
            r"(?:search memory for|find in memory)\s+(.+)",
            text,
            re.IGNORECASE
        )

        if match:

            query = match.group(1).strip()

            try:

                results = self.memory.search(query)

                if not results:
                    return (
                        f"I couldn't find anything about "
                        f"{query}, sir."
                    )

                response = (
                    f"I found these memories about "
                    f"{query}:\n"
                )

                for item in results[:10]:

                    if isinstance(item, (tuple, list)):

                        if len(item) >= 2:
                            response += f"- {item[1]}\n"
                        else:
                            response += f"- {item[0]}\n"

                    else:
                        response += f"- {item}\n"

                return response

            except Exception as e:

                print(f"[Memory Error] {e}")

                return (
                    "I couldn't search my memory, sir."
                )

        # ----------------------------------------------------
        # CLEAR MEMORY
        # ----------------------------------------------------

        if (
            lower == "clear all memories"
            or lower == "clear my memories"
            or lower == "delete all memories"
        ):

            self.memory.clear()

            return (
                "All saved memories have been cleared, sir."
            )

        return None

    # ========================================================
    # COMPUTER COMMANDS
    # ========================================================

    def computer_command(self, text):

        lower = text.lower().strip()

        # ----------------------------------------------------
        # OPEN / LAUNCH APPLICATION
        # ----------------------------------------------------

        match = re.match(
            r"^(?:open|launch|start|run)\s+(.+)$",
            text,
            re.IGNORECASE
        )

        if match:

            app_name = match.group(1).strip()

            website_names = [
                "youtube",
                "google",
                "github",
                "chatgpt"
            ]

            if app_name.lower() not in website_names:

                try:

                    success = self.computer.open_app(
                        app_name
                    )

                    if success:
                        return (
                            f"Opening {app_name}, sir."
                        )

                    return (
                        f"I couldn't open "
                        f"{app_name}, sir."
                    )

                except Exception as e:

                    print(
                        f"[Computer Error] {e}"
                    )

                    return (
                        f"I couldn't open "
                        f"{app_name}, sir."
                    )

        # ----------------------------------------------------
        # SCREENSHOT
        # ----------------------------------------------------

        if (
            "take a screenshot" in lower
            or "take screenshot" in lower
            or "capture screen" in lower
            or "capture the screen" in lower
        ):

            try:

                self.computer.screenshot()

                return (
                    "Screenshot captured, sir."
                )

            except Exception as e:

                print(
                    f"[Screenshot Error] {e}"
                )

                return (
                    "I couldn't capture the screenshot, sir."
                )

        # ----------------------------------------------------
        # VOLUME UP
        # ----------------------------------------------------

        if (
            "increase volume" in lower
            or "volume up" in lower
            or "turn volume up" in lower
            or "make volume louder" in lower
        ):

            self.computer.volume_up()

            return "Volume increased, sir."

        # ----------------------------------------------------
        # VOLUME DOWN
        # ----------------------------------------------------

        if (
            "decrease volume" in lower
            or "volume down" in lower
            or "turn volume down" in lower
            or "make volume lower" in lower
        ):

            self.computer.volume_down()

            return "Volume decreased, sir."

        # ----------------------------------------------------
        # MUTE
        # ----------------------------------------------------

        if (
            lower == "mute"
            or "mute volume" in lower
            or "mute the volume" in lower
        ):

            self.computer.volume_mute()

            return "Volume muted, sir."

        # ----------------------------------------------------
        # LOCK COMPUTER
        # ----------------------------------------------------

        if (
            "lock computer" in lower
            or "lock the computer" in lower
            or "lock my pc" in lower
            or "lock pc" in lower
        ):

            self.computer.lock_computer()

            return "Locking the computer, sir."

        return None

    # ========================================================
    # BROWSER COMMANDS
    # ========================================================

    def browser_command(self, text):

        lower = text.lower().strip()

        # ----------------------------------------------------
        # YOUTUBE
        # ----------------------------------------------------

        if lower in [
            "open youtube",
            "launch youtube",
            "start youtube"
        ]:

            self.browser.open_youtube()

            return "Opening YouTube, sir."

        # ----------------------------------------------------
        # GOOGLE
        # ----------------------------------------------------

        if lower in [
            "open google",
            "launch google",
            "start google"
        ]:

            self.browser.open_google()

            return "Opening Google, sir."

        # ----------------------------------------------------
        # GITHUB
        # ----------------------------------------------------

        if lower in [
            "open github",
            "launch github",
            "start github"
        ]:

            self.browser.open_github()

            return "Opening GitHub, sir."

        # ----------------------------------------------------
        # CHATGPT
        # ----------------------------------------------------

        if lower in [
            "open chatgpt",
            "launch chatgpt",
            "start chatgpt"
        ]:

            self.browser.open_chatgpt()

            return "Opening ChatGPT, sir."

        # ----------------------------------------------------
        # GOOGLE SEARCH
        # ----------------------------------------------------

        match = re.search(
            r"(?:search google for|google search for|"
            r"search for|search)\s+(.+)",
            text,
            re.IGNORECASE
        )

        if match:

            query = match.group(1).strip()

            if query:

                self.browser.google_search(query)

                return (
                    f"Searching Google for "
                    f"{query}, sir."
                )

        # ----------------------------------------------------
        # YOUTUBE SEARCH
        # ----------------------------------------------------

        match = re.search(
            r"(?:search youtube for|youtube search for|"
            r"youtube search)\s+(.+)",
            text,
            re.IGNORECASE
        )

        if match:

            query = match.group(1).strip()

            if query:

                self.browser.youtube_search(query)

                return (
                    f"Searching YouTube for "
                    f"{query}, sir."
                )

        # ----------------------------------------------------
        # WIKIPEDIA
        # ----------------------------------------------------

        match = re.search(
            r"(?:search wikipedia for|wikipedia search for|"
            r"wikipedia)\s+(.+)",
            text,
            re.IGNORECASE
        )

        if match:

            query = match.group(1).strip()

            if query:

                self.browser.wikipedia_search(query)

                return (
                    f"Searching Wikipedia for "
                    f"{query}, sir."
                )

        return None

    # ========================================================
    # SYSTEM COMMANDS
    # ========================================================

    def system_command(self, text):

        lower = text.lower().strip()

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        if (
            "what time is it" in lower
            or "what is the time" in lower
            or "current time" in lower
            or "tell me the time" in lower
            or lower == "time"
        ):

            return (
                f"The current time is "
                f"{self.system.get_time()}, sir."
            )

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if (
            "what is today's date" in lower
            or "what's today's date" in lower
            or "what is the date" in lower
            or "current date" in lower
            or "tell me the date" in lower
            or lower == "date"
        ):

            return (
                f"Today's date is "
                f"{self.system.get_date()}, sir."
            )

        # ----------------------------------------------------
        # CPU
        # ----------------------------------------------------

        if (
            "cpu usage" in lower
            or "processor usage" in lower
            or "cpu status" in lower
            or "how much cpu" in lower
        ):

            cpu = self.system.get_cpu_usage()

            return (
                f"CPU usage is {cpu} percent, sir."
            )

        # ----------------------------------------------------
        # RAM
        # ----------------------------------------------------

        if (
            "ram usage" in lower
            or "memory usage" in lower
            or "how much ram" in lower
        ):

            ram = self.system.get_ram_usage()

            return (
                f"RAM usage is {ram} percent, sir."
            )

        # ----------------------------------------------------
        # BATTERY
        # ----------------------------------------------------

        if "battery" in lower:

            battery = self.system.get_battery()

            return (
                f"Battery level is "
                f"{battery} percent, sir."
            )

        # ----------------------------------------------------
        # SYSTEM STATUS
        # ----------------------------------------------------

        if (
            "system status" in lower
            or "system information" in lower
            or "system report" in lower
            or "how is the system" in lower
        ):

            return (
                f"System status: "
                f"{self.system.get_status()}"
            )

        # ----------------------------------------------------
        # UPTIME
        # ----------------------------------------------------

        if (
            "system uptime" in lower
            or "computer uptime" in lower
            or "how long has the computer been running" in lower
        ):

            return (
                f"The system has been running for "
                f"{self.system.get_uptime()}, sir."
            )

        return None