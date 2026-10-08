# ============================================================
# JARVIS COMPUTER CONTROLLER
# ============================================================

import os
import subprocess
import time

import pyautogui
import psutil


class JarvisComputer:

    def __init__(self):
        pyautogui.PAUSE = 0.2


    # ========================================================
    # OPEN APPLICATION
    # ========================================================

    def open_app(self, app_name):

        apps = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "cmd": ["cmd.exe"],
    "explorer": ["explorer.exe"],
    "file explorer": ["explorer.exe"],

    # Spotify
    "spotify": ["spotify"]
}

        app = app_name.lower().strip()

        if app not in apps:
            print(f"[JARVIS] Unknown application: {app_name}")
            return False

        try:

            subprocess.Popen(apps[app])

            print(f"[JARVIS] Opening {app_name}...")

            return True

        except Exception as e:

            print(f"[Computer Error] {e}")

            return False


    # ========================================================
    # MOUSE
    # ========================================================

    def move_mouse(self, x, y):

        pyautogui.moveTo(x, y)


    def click(self):

        pyautogui.click()


    def double_click(self):

        pyautogui.doubleClick()


    def right_click(self):

        pyautogui.rightClick()


    # ========================================================
    # TYPE
    # ========================================================

    def type_text(self, text):

        pyautogui.write(text, interval=0.02)


    # ========================================================
    # KEYBOARD
    # ========================================================

    def press(self, key):

        pyautogui.press(key)


    def hotkey(self, *keys):

        pyautogui.hotkey(*keys)


    # ========================================================
    # SCREENSHOT
    # ========================================================

    def screenshot(self):

        folder = "data/screenshots"

        os.makedirs(folder, exist_ok=True)

        filename = time.strftime(
            "screenshot_%Y%m%d_%H%M%S.png"
        )

        path = os.path.join(
            folder,
            filename
        )

        image = pyautogui.screenshot()

        image.save(path)

        print(f"[JARVIS] Screenshot saved: {path}")

        return path


    # ========================================================
    # SCREEN INFORMATION
    # ========================================================

    def get_screen_size(self):

        return pyautogui.size()


    def get_mouse_position(self):

        return pyautogui.position()


    # ========================================================
    # VOLUME
    # ========================================================

    def volume_up(self):

        pyautogui.press("volumeup")


    def volume_down(self):

        pyautogui.press("volumedown")


    def volume_mute(self):

        pyautogui.press("volumemute")


    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    def get_system_status(self):

        return {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("C:\\").percent
        }


    # ========================================================
    # LOCK COMPUTER
    # ========================================================

    def lock_computer(self):

        subprocess.run(
            [
                "rundll32.exe",
                "user32.dll,LockWorkStation"
            ],
            check=False
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    computer = JarvisComputer()

    print("=" * 50)
    print("       JARVIS COMPUTER TEST")
    print("=" * 50)

    print("\nScreen size:")
    print(computer.get_screen_size())

    print("\nMouse position:")
    print(computer.get_mouse_position())

    print("\nSystem status:")
    print(computer.get_system_status())

    print("\nComputer controller ready.")