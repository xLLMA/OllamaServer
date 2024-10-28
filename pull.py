import requests
import re
import subprocess
import sys

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    GREY = '\033[90m'
    CYAN = '\033[96m'
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
            unique_libs = list(set(target_links))
            return [(lib.split('/')[-1], f"https://ollama.com{lib}") for lib in unique_libs]

        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}Error fetching libraries: {e}{Colors.RESET}")
            return []

    def display_libraries(self):
        """Display available libraries with their IDs."""
        print(f"{Colors.GREEN}Available Libraries:{Colors.RESET}")
        for index, (repo_name, repo_url) in enumerate(self.all_libs, start=1):
            print(f"[{Colors.GREEN}{index}{Colors.RESET}] "
                  f"{Colors.MAGENTA}{repo_name.upper()}{Colors.RESET} :"
                  f"{Colors.CYAN} {repo_url}{Colors.RESET}")

    def pull_lib(self):
        """Pull Ollama Library."""
        repo_name, repo_url = None, None
        self.display_libraries()
        print(f"\n[+] Enter Library {Colors.RED}Number{Colors.RESET} To Pull Library:")

        # get pull number (input)
        try:
            pull_number = int(input("[-] Pull > "))
            # update repo_name and repo_url
            if pull_number in range(1, len(self.all_libs) + 1):
                repo_name = self.all_libs[pull_number - 1][0]
                repo_url = self.all_libs[pull_number - 1][1]
                print(f"{Colors.CYAN}Library:{Colors.RESET} {repo_name}"
                      f"\n{Colors.CYAN}Pulling:{Colors.RESET} {repo_url}")
            else:
                print(f"{Colors.RED}Invalid selection. Please choose a number from the list.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")

        return repo_name, repo_url


# ----------------------------------------
lib = Libs()
repo_name, repo_url = lib.pull_lib()
with open("repo.txt", "w") as fs:
    fs.write(f"{repo_name}")
