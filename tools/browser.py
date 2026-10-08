# tools/browser.py

import webbrowser
from urllib.parse import quote_plus


class JarvisBrowser:
    """
    Browser control system for JARVIS.

    Handles:
    - Opening websites
    - Google searches
    - YouTube searches
    - Opening common websites
    - Searching specific websites
    """

    def __init__(self):
        self.browser = webbrowser.get()

    # ==========================================
    # OPEN URL
    # ==========================================

    def open_url(self, url):

        if not url:
            return "Sir, please provide a website."

        url = url.strip()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:

            self.browser.open_new_tab(url)

            return f"Opening {url}, sir."

        except Exception as error:

            return f"Unable to open website: {error}"

    # ==========================================
    # GOOGLE SEARCH
    # ==========================================

    def google_search(self, query):

        if not query.strip():
            return "Sir, what should I search for?"

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        try:

            self.browser.open_new_tab(url)

            return f"Searching Google for {query}, sir."

        except Exception as error:

            return f"Google search failed: {error}"

    # ==========================================
    # YOUTUBE SEARCH
    # ==========================================

    def youtube_search(self, query):

        if not query.strip():
            return "Sir, what should I search on YouTube?"

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        try:

            self.browser.open_new_tab(url)

            return (
                f"Searching YouTube for "
                f"{query}, sir."
            )

        except Exception as error:

            return f"YouTube search failed: {error}"

    # ==========================================
    # OPEN YOUTUBE
    # ==========================================

    def open_youtube(self):

        return self.open_url(
            "https://www.youtube.com"
        )

    # ==========================================
    # OPEN GOOGLE
    # ==========================================

    def open_google(self):

        return self.open_url(
            "https://www.google.com"
        )

    # ==========================================
    # OPEN GITHUB
    # ==========================================

    def open_github(self):

        return self.open_url(
            "https://github.com"
        )

    # ==========================================
    # OPEN CHATGPT
    # ==========================================

    def open_chatgpt(self):

        return self.open_url(
            "https://chatgpt.com"
        )

    # ==========================================
    # SEARCH GITHUB
    # ==========================================

    def github_search(self, query):

        if not query.strip():
            return "Sir, what should I search on GitHub?"

        url = (
            "https://github.com/search?q="
            + quote_plus(query)
            + "&type=repositories"
        )

        try:

            self.browser.open_new_tab(url)

            return (
                f"Searching GitHub for "
                f"{query}, sir."
            )

        except Exception as error:

            return f"GitHub search failed: {error}"

    # ==========================================
    # SEARCH WIKIPEDIA
    # ==========================================

    def wikipedia_search(self, query):

        if not query.strip():
            return "Sir, what should I search on Wikipedia?"

        url = (
            "https://en.wikipedia.org/wiki/Special:Search?search="
            + quote_plus(query)
        )

        try:

            self.browser.open_new_tab(url)

            return (
                f"Searching Wikipedia for "
                f"{query}, sir."
            )

        except Exception as error:

            return (
                f"Wikipedia search failed: "
                f"{error}"
            )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    browser = JarvisBrowser()

    print("=" * 50)
    print("       JARVIS BROWSER TEST")
    print("=" * 50)

    while True:

        print("\n1. Open Google")
        print("2. Google Search")
        print("3. Open YouTube")
        print("4. YouTube Search")
        print("5. Open GitHub")
        print("6. GitHub Search")
        print("7. Open ChatGPT")
        print("8. Wikipedia Search")
        print("9. Open URL")
        print("10. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            print(browser.open_google())

        elif choice == "2":

            query = input("Search: ")

            print(
                browser.google_search(query)
            )

        elif choice == "3":

            print(browser.open_youtube())

        elif choice == "4":

            query = input("YouTube search: ")

            print(
                browser.youtube_search(query)
            )

        elif choice == "5":

            print(browser.open_github())

        elif choice == "6":

            query = input("GitHub search: ")

            print(
                browser.github_search(query)
            )

        elif choice == "7":

            print(browser.open_chatgpt())

        elif choice == "8":

            query = input("Wikipedia search: ")

            print(
                browser.wikipedia_search(query)
            )

        elif choice == "9":

            url = input("URL: ")

            print(
                browser.open_url(url)
            )

        elif choice == "10":

            print(
                "JARVIS: Browser system offline, sir."
            )

            break

        else:

            print("JARVIS: Invalid command.")