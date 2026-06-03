import requests
import time
import random

# Credentials Replace these with your actual keys

APP_ID = "your_app_id_here"
API_KEY = "your_api_key_here"
DISCORD_WEBHOOK = "your_webhook_url_here"

# Filter
SEARCH_TERM = "retail"
LOCATION = "your_location_here"  # Set your city here
COUNTRY = "gb"
RESULTS_PER_PAGE = 50

# Excluded words from the search
EXCLUDED_WORDS = [
    "manager", "supervisor", "director", "head of",
    "senior", "lead", "specialist", "planner", "accountant",
    "merchandiser", "analyst", "recruiter", "talent"
]

def fetch_jobs():
    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    
    params = {
        "app_id": APP_ID,
        "app_key": API_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": SEARCH_TERM,
        "where": LOCATION,
        "distance": 10,
        "content-type": "application/json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    return data

def load_seen_jobs():
    try:
        with open("seen_jobs.txt", "r") as f:
            seen = set(f.read().splitlines())
            return seen
    except FileNotFoundError:
        return set()

def save_seen_jobs(seen):
    with open("seen_jobs.txt", "w") as f:
        f.write("\n".join(seen))

def send_discord_notification(job):
    message = (
        f"**New Job Alert!**\n"
        f"**Title:** {job['title']}\n"
        f"**Company:** {job['company']['display_name']}\n"
        f"**Location:** {job['location']['display_name']}\n"
        f"**Apply here:** {job['redirect_url']}"
    )
    
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=payload)

def main():
    print("GMAJ is running. Checking for jobs every hour...")
    
    while True:
        print("Checking for new jobs...")
        
        jobs = fetch_jobs()
        seen = load_seen_jobs()
        new_jobs = []
        
        # Guard rail against empty api returns
        if 'results' not in jobs:
            print("No results found or API error. Checking again next cycle.")
            time.sleep(3600)
            continue
        
        for job in jobs['results']:
            job_id = job['id']
            if job_id not in seen:
                # FIXED: Uses the LOCATION variable dynamically instead of hardcoded text
                if LOCATION.lower() not in job['location']['display_name'].lower():
                    continue
                
                title_lower = job['title'].lower()
                if any(word in title_lower for word in EXCLUDED_WORDS):
                    continue
                
                new_jobs.append(job)
                seen.add(job_id)
        
        save_seen_jobs(seen)
        
        print(f"Found {len(new_jobs)} new jobs this check")
        
        for job in new_jobs:
            send_discord_notification(job)
        
        print("Next check in 1 hour. Leave this terminal open.")
        time.sleep(3600)

main()