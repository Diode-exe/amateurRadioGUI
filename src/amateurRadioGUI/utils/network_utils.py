import os
import requests
import zipfile


class NetworkUtils:
    def __init__(self):
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

        # Point precisely to the data folder
        self.QUESTIONS_PATH = os.path.join(self.SCRIPT_DIR, "..", "data", "questions.txt")
        
        self.temp_path = os.path.join(self.SCRIPT_DIR, "..", "temp.zip")

    def download_questions(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check if the request was successful
            with open(self.temp_path, 'wb') as file:
                file.write(response.content)
            self.unzip_questions()
        except requests.RequestException as e:
            print(f"Error downloading questions: {e}")

    def unzip_questions(self):
        try:
            with zipfile.ZipFile(self.temp_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(self.SCRIPT_DIR, "..", "data"))
                try:
                    os.rename(os.path.join(self.SCRIPT_DIR, "..", "data", "amat_basic_quest_delim.txt"), self.QUESTIONS_PATH)
                except FileNotFoundError:
                    os.rename(os.path.join(self.SCRIPT_DIR, "..", "data", "amat_adv_quest_delim.txt"), self.QUESTIONS_PATH)

            os.remove(self.temp_path)  # Clean up the temporary zip file
        except zipfile.BadZipFile as e:
            print(f"Error unzipping questions: {e}")
