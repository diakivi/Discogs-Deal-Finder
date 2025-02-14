import json
import time
from scraper import DiscogsAPI
from config import DEALS_JSON_PATH, MAX_TOTAL_PRICE, MIN_WANT_HAVE_RATIO, MAX_SHIPPING_OVERSEAS, MAX_SHIPPING_LOCAL, TIME_SINCE_LAST_SOLD_YEARS, ACCEPTABLE_CONDITIONS, HIGH_PRIORITY_RELEASES

class DealFinder:
    def __init__(self):
        self.api = DiscogsAPI()
    
    def calculate_deal_score(self, release, item, price_history):
        score = 0
        
        # Hard filters
        if item['condition'] not in ACCEPTABLE_CONDITIONS:
            return None
        if item['price'] > MAX_TOTAL_PRICE:
            return None
        if item['shipping'] > (MAX_SHIPPING_OVERSEAS if item['location'] != 'USA' else MAX_SHIPPING_LOCAL):
            return None
        
        # Price vs. Historical Median (Filter + Multiplier)
        if item['price'] < price_history['median'] * 0.8:
            score += (price_history['median'] - item['price']) / price_history['median'] * 10
        else:
            return None
        
        # Want-to-Have Ratio (Multiplier)
        want_have_ratio = release['want'] / max(release['have'], 1)
        if want_have_ratio >= MIN_WANT_HAVE_RATIO:
            score += want_have_ratio * 2
        
        # Time Since Last Sold (Multiplier)
        years_since_last_sold = release.get('years_since_last_sold', 0)
        if years_since_last_sold >= TIME_SINCE_LAST_SOLD_YEARS:
            score += (years_since_last_sold - TIME_SINCE_LAST_SOLD_YEARS) * 2
        
        # High-Priority Release (Multiplier)
        if release['id'] in HIGH_PRIORITY_RELEASES:
            score *= 1.5
            if years_since_last_sold >= TIME_SINCE_LAST_SOLD_YEARS or years_since_last_sold == 0:
                return item  # Overrides other filters
        
        return item if score > 0 else None
    
    def find_good_deals(self):
        print("Fetching wantlist from Discogs...")
        wanted_releases = self.api.get_wanted_releases()
        print(f"Found {len(wanted_releases)} releases in wantlist")
        good_deals = []
        
        for release in wanted_releases:
            price_history = self.api.get_price_history(release['id'])
            if not price_history:
                continue
            
            listings = self.api.get_listings(release['id'])
            for item in listings:
                deal = self.calculate_deal_score(release, item, price_history)
                if deal:
                    good_deals.append(deal)
        
        # Sort deals by highest score
        good_deals.sort(key=lambda x: x['price'])
        
        # Save to JSON
        with open(DEALS_JSON_PATH, "w") as file:
            json.dump(good_deals, file, indent=4)
        
        return good_deals
