# core/memory.py

import sqlite3
import os
from datetime import datetime

from config import MEMORY_FILE


class JarvisMemory:
    """
    SQLite-based memory system for JARVIS.

    JARVIS can:
    - Save memories
    - Retrieve memories
    - Search memories
    - Delete memories
    - Clear all memories
    """

    def __init__(self, database_path=MEMORY_FILE):

        self.database_path = database_path

        # Create data folder if it doesn't exist
        folder = os.path.dirname(database_path)

        if folder:
            os.makedirs(folder, exist_ok=True)

        self.connection = sqlite3.connect(self.database_path)

        self.create_table()

    # ==========================================
    # DATABASE SETUP
    # ==========================================

    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        self.connection.commit()

    # ==========================================
    # SAVE MEMORY
    # ==========================================

    def remember(self, memory):

        memory = memory.strip()

        if not memory:
            return False

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO memories (memory, created_at)
            VALUES (?, ?)
        """, (
            memory,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        self.connection.commit()

        return True

    # ==========================================
    # GET ALL MEMORIES
    # ==========================================

    def get_memories(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, memory, created_at
            FROM memories
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    # ==========================================
    # SEARCH MEMORY
    # ==========================================

    def search(self, keyword):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, memory, created_at
            FROM memories
            WHERE memory LIKE ?
            ORDER BY id DESC
        """, (
            f"%{keyword}%",
        ))

        return cursor.fetchall()

    # ==========================================
    # DELETE MEMORY
    # ==========================================

    def delete(self, memory_id):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM memories
            WHERE id = ?
        """, (
            memory_id,
        ))

        self.connection.commit()

        return cursor.rowcount > 0

    # ==========================================
    # CLEAR ALL MEMORY
    # ==========================================

    def clear(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM memories
        """)

        self.connection.commit()

    # ==========================================
    # CLOSE DATABASE
    # ==========================================

    def close(self):

        if self.connection:
            self.connection.close()


# ==========================================
# TEST MEMORY SYSTEM
# ==========================================

if __name__ == "__main__":

    memory = JarvisMemory()

    print("=" * 50)
    print("        JARVIS MEMORY TEST")
    print("=" * 50)

    while True:

        print("\n1. Remember something")
        print("2. Show memories")
        print("3. Search memories")
        print("4. Delete memory")
        print("5. Clear all memories")
        print("6. Exit")

        choice = input("\nChoose: ")

        # --------------------------------------
        # REMEMBER
        # --------------------------------------

        if choice == "1":

            text = input("What should I remember? ")

            if memory.remember(text):
                print("JARVIS: Memory stored, sir.")
            else:
                print("JARVIS: I couldn't store that memory.")

        # --------------------------------------
        # SHOW MEMORIES
        # --------------------------------------

        elif choice == "2":

            memories = memory.get_memories()

            if not memories:

                print("JARVIS: I don't have any memories yet.")

            else:

                print("\nJARVIS MEMORY:\n")

                for memory_id, text, created in memories:

                    print(
                        f"[{memory_id}] "
                        f"{text} "
                        f"({created})"
                    )

        # --------------------------------------
        # SEARCH
        # --------------------------------------

        elif choice == "3":

            keyword = input("Search for: ")

            results = memory.search(keyword)

            if not results:

                print("JARVIS: I couldn't find anything.")

            else:

                print("\nSearch results:\n")

                for memory_id, text, created in results:

                    print(
                        f"[{memory_id}] "
                        f"{text} "
                        f"({created})"
                    )

        # --------------------------------------
        # DELETE
        # --------------------------------------

        elif choice == "4":

            try:

                memory_id = int(
                    input("Memory ID to delete: ")
                )

                if memory.delete(memory_id):

                    print("JARVIS: Memory deleted, sir.")

                else:

                    print("JARVIS: Memory not found.")

            except ValueError:

                print("JARVIS: Please enter a valid ID.")

        # --------------------------------------
        # CLEAR
        # --------------------------------------

        elif choice == "5":

            confirm = input(
                "Are you sure? Type YES: "
            )

            if confirm == "YES":

                memory.clear()

                print(
                    "JARVIS: All memories have been cleared."
                )

            else:

                print("JARVIS: Cancelled.")

        # --------------------------------------
        # EXIT
        # --------------------------------------

        elif choice == "6":

            memory.close()

            print(
                "\nJARVIS: Memory system offline. Goodbye, sir."
            )

            break

        else:

            print("JARVIS: Invalid option.")