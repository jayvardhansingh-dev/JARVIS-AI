# ============================================================
# JARVIS SYSTEM CONTROLLER
# ============================================================

import os
import sys
import time
import platform
import subprocess
from datetime import datetime

import psutil


class JarvisSystem:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # SYSTEM INFORMATION
    # --------------------------------------------------------

    def get_system_info(self):

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node()
        }

    # --------------------------------------------------------
    # CPU
    # --------------------------------------------------------

    def get_cpu_usage(self):

        return round(psutil.cpu_percent(interval=1), 1)

    # --------------------------------------------------------
    # RAM
    # --------------------------------------------------------

    def get_ram_usage(self):

        return round(psutil.virtual_memory().percent, 1)

    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    def get_battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            return "not available"

        return round(battery.percent, 1)

    # --------------------------------------------------------
    # DISK
    # --------------------------------------------------------

    def get_disk_usage(self):

        disk = psutil.disk_usage("C:\\")

        return round(disk.percent, 1)

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    def get_time(self):

        return datetime.now().strftime("%I:%M %p")

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    def get_date(self):

        return datetime.now().strftime("%d %B %Y")

    # --------------------------------------------------------
    # UPTIME
    # --------------------------------------------------------

    def get_uptime(self):

        boot_time = psutil.boot_time()
        current_time = time.time()

        uptime_seconds = current_time - boot_time

        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)

        return f"{hours} hours {minutes} minutes"

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    def get_status(self):

        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()

        battery = self.get_battery()

        return (
            f"CPU {cpu} percent, "
            f"RAM {ram} percent, "
            f"Battery {battery} percent."
        )

    # --------------------------------------------------------
    # OPEN SYSTEM FOLDERS
    # --------------------------------------------------------

    def open_folder(self, folder):

        folders = {
            "desktop": os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            ),

            "documents": os.path.join(
                os.path.expanduser("~"),
                "Documents"
            ),

            "downloads": os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            ),

            "pictures": os.path.join(
                os.path.expanduser("~"),
                "Pictures"
            )
        }

        path = folders.get(folder.lower())

        if path and os.path.exists(path):

            os.startfile(path)

            return True

        return False

    # --------------------------------------------------------
    # LOCK COMPUTER
    # --------------------------------------------------------

    def lock_computer(self):

        if platform.system() == "Windows":

            subprocess.run(
                ["rundll32.exe", "user32.dll,LockWorkStation"],
                check=False
            )

            return True

        return False

    # --------------------------------------------------------
    # SHUTDOWN
    # --------------------------------------------------------

    def shutdown(self):

        if platform.system() == "Windows":

            subprocess.run(
                ["shutdown", "/s", "/t", "30"],
                check=False
            )

            return True

        return False

    # --------------------------------------------------------
    # CANCEL SHUTDOWN
    # --------------------------------------------------------

    def cancel_shutdown(self):

        if platform.system() == "Windows":

            subprocess.run(
                ["shutdown", "/a"],
                check=False
            )

            return True

        return False


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    system = JarvisSystem()

    print("=" * 50)
    print("       JARVIS SYSTEM TEST")
    print("=" * 50)

    print("\nOS:", platform.system())
    print("CPU:", system.get_cpu_usage(), "%")
    print("RAM:", system.get_ram_usage(), "%")
    print("Battery:", system.get_battery())
    print("Time:", system.get_time())
    print("Date:", system.get_date())
    print("Uptime:", system.get_uptime())

    print("\nSystem Status:")
    print(system.get_status())