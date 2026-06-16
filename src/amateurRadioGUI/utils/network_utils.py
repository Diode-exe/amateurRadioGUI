"""Utility functions for network operations in the amateur radio GUI application,
such as downloading and unzipping question files."""

import os
import zipfile
import requests


class NetworkUtils:
    """Utility class for handling network operations related to question files."""
    def __init__(self):
        """Initialize the NetworkUtils class and set up paths for question files."""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Point precisely to the data folder
        self.questions_path = os.path.join(self.script_dir, "..", "data", "questions.txt")

        self.temp_path = os.path.join(self.script_dir, "..", "temp.zip")

    def download_questions(self, url):
        """Download a zip file containing questions from the specified URL and unzip it."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check if the request was successful
            with open(self.temp_path, 'wb') as file:
                file.write(response.content)
            self.unzip_questions()
        except requests.RequestException as e:
            print(f"Error downloading questions: {e}")

    def unzip_questions(self):
        """Unzip the downloaded questions file and move it to the data directory."""
        try:
            with zipfile.ZipFile(self.temp_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(self.script_dir, "..", "data"))
                try:
                    os.rename(os.path.join(self.script_dir, "..", "data", "amat_basic_quest_delim.txt"), self.questions_path)
                except FileNotFoundError:
                    os.rename(os.path.join(self.script_dir, "..", "data", "amat_adv_quest_delim.txt"), self.questions_path)

            os.remove(self.temp_path)  # Clean up the temporary zip file
        except zipfile.BadZipFile as e:
            print(f"Error unzipping questions: {e}")
