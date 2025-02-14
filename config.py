import os
from pathlib import Path

# ===== USER INPUT REQUIRED =====
# Replace 'your_discogs_username' with your actual Discogs username
DISCOGS_USERNAME = "your_discogs_username"

# Replace 'your_discogs_token' with your actual Discogs API token
DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN", "your_discogs_token")

# Replace 'your_computer_username' with your actual computer username if needed for file paths
BASE_DIR = Path("/Users/your_computer_username/Documents/AI Programs/Discogs Deal Finder")
CACHE_DIR = BASE_DIR / "cache"
DEALS_JSON_PATH = BASE_DIR / "deals.json"

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Marketplace scan configuration
MARKETPLACE_SCAN_INTERVAL = 3600  # How often to scan marketplace (in seconds)
PRICE_HISTORY_UPDATE_INTERVAL = 604800  # How often to update price history (7 days in seconds)

# Deal filtering & ranking criteria
MAX_TOTAL_PRICE = 200  # Hard filter (excluding shipping)
MIN_WANT_HAVE_RATIO = 2  # Scaling factor (higher is better)
MAX_SHIPPING_OVERSEAS = 15  # Hard filter (except for high-priority releases)
MAX_SHIPPING_LOCAL = 8  # Hard filter (except for high-priority releases)
TIME_SINCE_LAST_SOLD_YEARS = 3  # Multiplier (longer = better deal)

# Acceptable record conditions (ordered best to worst)
ACCEPTABLE_CONDITIONS = ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)"]

# List of high-priority releases (to be manually populated)
HIGH_PRIORITY_RELEASES = [
    # Example: "123456", "789012"
]
