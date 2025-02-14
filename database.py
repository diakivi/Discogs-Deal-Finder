import json
from config import DEALS_JSON_PATH

class Database:
    def __init__(self):
        self.file_path = DEALS_JSON_PATH
    
    def save_deals(self, deals):
        """ Saves the filtered and ranked deals to a JSON file. """
        with open(self.file_path, "w") as file:
            json.dump(deals, file, indent=4)
    
    def load_deals(self):
        """ Loads deals from the JSON file. Returns an empty list if the file doesn't exist. """
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
