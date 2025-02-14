import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta
from config import DISCOGS_USERNAME, DISCOGS_TOKEN, CACHE_DIR

class DiscogsAPI:
    def __init__(self):
        self.base_url = "https://api.discogs.com"
        self.headers = {"Authorization": f"Discogs token={DISCOGS_TOKEN}"}
        self.price_cache = {}
        self.cache_expiry = timedelta(weeks=1)

    def get_wanted_releases(self):
        url = f"{self.base_url}/users/{DISCOGS_USERNAME}/wants"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("wants", [])
        return []

    def get_price_history(self, release_id):
        cache_file = CACHE_DIR / f"{release_id}_prices.json"
        if cache_file.exists():
            with open(cache_file, "r") as file:
                cached_data = json.load(file)
                if datetime.now().timestamp() - cached_data["timestamp"] < self.cache_expiry.total_seconds():
                    return cached_data
        
        url = f"https://www.discogs.com/sell/release/{release_id}?sort=price,asc"
        response = requests.get(url)
        time.sleep(2)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        price_history_section = soup.find("div", class_="price_history")
        if not price_history_section:
            return None
        
        try:
            min_price = float(price_history_section.find("span", class_="price_min").text.replace("$", "").strip())
            median_price = float(price_history_section.find("span", class_="price_median").text.replace("$", "").strip())
            max_price = float(price_history_section.find("span", class_="price_max").text.replace("$", "").strip())
        except (AttributeError, ValueError):
            return None
        
        price_data = {
            "min": min_price,
            "median": median_price,
            "max": max_price,
            "timestamp": datetime.now().timestamp()
        }
        with open(cache_file, "w") as file:
            json.dump(price_data, file, indent=4)
        return price_data
