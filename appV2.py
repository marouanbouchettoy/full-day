"""
Git Real Commit Generator Script (v2)

This script generates Git commits with real code fetched from your GitHub repositories.
It simulates realistic development activity by using actual code from your repos,
creating commits with random timestamps during specified dates, then pushes them.

Similar to app.py but commits real code instead of fake text.

Usage: python appV2.py
Requirements:
- Must be run in a valid Git repository.
- Remote 'origin' must be configured.
- Python 3.x with standard libraries.
- .env file with GITHUB_TOKEN and YOUR_USERNAME.
- Internet connection to fetch from GitHub API.
"""

import os
import subprocess
from random import randint, choice, random
from datetime import datetime, timedelta
import urllib.request
import json
import base64

# Define the start and end dates for generating commits (same as app.py)
START_DATE = datetime(2025, 12, 1)
END_DATE = datetime(2025, 12, 3)

# List of random commit messages to use (same as app.py)
COMMIT_MESSAGES = [
    "Improved performance.",
    "Fixed a bug in the system.",
    "Added a new feature.",
    "Refactored some code.",
    "Updated documentation.",
    "Optimized database queries.",
    "Removed deprecated functions.",
    "Enhanced UI components.",
    "Corrected typos in code.",
    "Improved logging mechanism."
]


def load_env_vars():
    """
    Load environment variables from .env file.
    """
    if not os.path.exists('.env'):
        print("Error: .env file not found.")
        exit(1)

    with open('.env') as f:
        for line in f:
            if line.strip() and '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


def fetch_user_repos(username, token):
    """
    Fetch public repositories for the user from GitHub API.

    Args:
        username (str): GitHub username.
        token (str): GitHub token for authentication.

    Returns:
        list: List of repository names.
    """
    url = f"https://api.github.com/users/{username}/repos"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # Filter for public repos with content
            repos = [repo['name'] for repo in data if not repo['private'] and repo['size'] > 0]
            print(f"Fetched {len(repos)} public repositories: {repos}")
            return repos
    except Exception as e:
        print(f"Error fetching repositories: {e}")
        return []


def fetch_readme_content(username, token, repo_name):
    """
    Fetch README content from a specific repository.

    Args:
        username (str): GitHub username.
        token (str): GitHub token.
        repo_name (str): Repository name.

    Returns:
        str or None: Decoded README content if found, else None.
    """
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
            return content
    except Exception:
        return None


def check_git_repository():
    """
    Verify that the current directory is a valid Git repository.
    """
    if not os.path.isdir(".git"):
        print("Error: This script must be run in a valid Git repository.")
        exit(1)


def generate_commits_for_date(date, repos, username, token, filename_counter):
    """
    Generate random commits for a given date using real code from repos.

    Args:
        date (datetime): The date to generate commits for.
        repos (list): List of repository names.
        username (str): GitHub username.
        token (str): GitHub token.
        filename_counter (list): Mutable counter for unique filenames.

    There is a 80% chance of having commits on any given day.
    Number of commits per day varies between 1 and 10.
    """
    if random() < 0.8 and repos:  # 80% probability of commits on this day
        num_commits = randint(1, 10)  # Random number of commits per day

        for _ in range(num_commits):
            # Generate random time (hour, minute, second)
            random_hour = randint(0, 23)
            random_minute = randint(0, 59)
            random_second = randint(0, 59)

            # Create commit datetime
            commit_datetime = datetime(
                date.year, date.month, date.day,
                random_hour, random_minute, random_second
            )
            commit_date_str = commit_datetime.strftime('%Y-%m-%dT%H:%M:%S')

            # Fetch real code: choose random repo and get its README
            repo_name = choice(repos)
            code = fetch_readme_content(username, token, repo_name)

            if code:
                # Save the fetched code to a unique file
                filename_counter[0] += 1
                filename = f"real_code_{repo_name}_{filename_counter[0]:04d}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)

                # Stage the new file
                subprocess.run(['git', 'add', filename], check=True)

                # Commit with specific date and random message
                commit_message = choice(COMMIT_MESSAGES)
                subprocess.run(
                    ['git', 'commit', '--date', commit_date_str, '-m', commit_message],
                    check=True
                )
                print(f"Committed {filename} from {repo_name} on {commit_date_str}")


def push_commits():
    """
    Push all commits to the remote 'origin' main branch.
    """
    try:
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("Successfully pushed all commits to remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error during push: {e}")


def main():
    """
    Main function to orchestrate the commit generation process.
    """
    load_env_vars()
    username = os.environ.get('YOUR_USERNAME')
    token = os.environ.get('GITHUB_TOKEN')

    if not username or not token:
        print("Error: YOUR_USERNAME and GITHUB_TOKEN must be set in .env")
        exit(1)

    check_git_repository()  # Ensure we're in a Git repo

    # Fetch user's public repositories
    repos = fetch_user_repos(username, token)
    if not repos:
        print("Error: No repositories found. Check your GitHub credentials or network.")
        exit(1)

    filename_counter = [0]  # Mutable counter for unique filenames

    # Iterate through each day in the date range
    current_date = START_DATE
    while current_date <= END_DATE:
        generate_commits_for_date(current_date, repos, username, token, filename_counter)
        current_date += timedelta(days=1)

    # Push all generated commits
    push_commits()


if __name__ == "__main__":
    main()
