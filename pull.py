import requests, re


class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'


class Libs:
    def __init__(self):
        self.all_libs = self.get_libs()

    @staticmethod
    def get_libs() -> list:
        """Fetch libraries from ollama library page."""
        url_fine = "https://ollama.com/library"
        try:
            # Send GET request to the URL
            req = requests.get(url_fine, timeout=5)
            req.raise_for_status()
            pattern = r'href="(/library[^"]+)"'
            target_links = re.findall(pattern, req.text)

            # -- list of unique libraries
            unique_libs = list(sorted(target_links))
            return [(lib.split('/')[-1], f"https://ollama.com{lib}") for lib in unique_libs]

        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}Error fetching libraries: {e}{Colors.RESET}")
            return []

    def display_libraries(self):
        """Display available libraries with their IDs."""
        print(f"{Colors.GREEN}Available Libraries:{Colors.RESET}")
        for repo_name, repo_url in self.all_libs:
            print(f"{Colors.GREEN}>{Colors.RESET} {Colors.MAGENTA}{repo_name}{Colors.RESET} : {repo_url}")


if __name__ == "__main__":
    LIBS = Libs()
    LIBS.display_libraries()
