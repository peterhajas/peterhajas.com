#!/usr/bin/env python3
import json
import requests
import time
from datetime import datetime
import os

URL = 'https://api.nebo.global/userlocation/v2/1TTBKZ1K3NZ1O1XD1F9J1D2KVXW'
DATA_FILE = '/data/scraped_data.json'
INTERVAL_MINUTES = 15

def load_existing_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def scrape_endpoint():
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        
        # Load existing data
        all_data = load_existing_data()
        
        # Add new entry with timestamp
        new_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': response.json()
        }
        
        all_data.append(new_entry)
        
        # Save back to file
        save_data(all_data)
        
        print(f"Successfully scraped and saved data at {new_entry['timestamp']}")
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    print(f"Starting ladylor scraper - will fetch every {INTERVAL_MINUTES} minutes")
    
    while True:
        scrape_endpoint()
        print(f"Sleeping for {INTERVAL_MINUTES} minutes...")
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == '__main__':
    main()