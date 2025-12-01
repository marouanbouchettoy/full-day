"""
Git Commit Generator Script

This script generates random Git commits between specified start and end dates.
It simulates development activity by creating commits with random timestamps and messages,
then pushes the commits to the remote repository.

Usage: python app.py
Requirements:
- Must be run in a valid Git repository.
- Remote 'origin' must be configured.
- Python 3.x with standard libraries.
"""

import os
import subprocess
from random import randint, choice, random
from datetime import datetime, timedelta

# Define the start and end dates for generating commits
START_DATE = datetime(2025, 12, 1)
END_DATE = datetime(2025, 12, 3)

# List of random commit messages to use
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


def check_git_repository():
    """
    Verify that the current directory is a valid Git repository.

    Exits the script if the .git directory is not found.
    """
    if not os.path.isdir(".git"):
        print("Error: This script must be run in a valid Git repository.")
        exit(1)


def generate_commits_for_date(date):
    """
    Generate random commits for a given date.

    Args:
        date (datetime): The date to generate commits for.

    There is a 80% chance of having commits on any given day.
    Number of commits per day varies between 1 and 10.
    """
    if random() < 0.8:  # 80% probability of commits on this day
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

            # Append a line to file.txt to create a change
            with open('file.txt', 'a') as file:
                file.write(f'Commit on {commit_date_str}\n')

            # Stage the changes
            subprocess.run(['git', 'add', '.'], check=True)

            # Commit with specific date and random message
            commit_message = choice(COMMIT_MESSAGES)
            subprocess.run(
                ['git', 'commit', '--date', commit_date_str, '-m', commit_message],
                check=True
            )


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
    check_git_repository()  # Ensure we're in a Git repo

    # Iterate through each day in the date range
    current_date = START_DATE
    while current_date <= END_DATE:
        generate_commits_for_date(current_date)
        current_date += timedelta(days=1)

    # Push all generated commits
    push_commits()


if __name__ == "__main__":
    main()
