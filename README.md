# Job Alert Tracker

A Python script that queries the Adzuna Jobs API hourly and sends new entry-level job listings to a Discord channel via webhook.

## How it works
- Polls the Adzuna API for relevant listings on a configurable schedule
- Filters out senior, management, and specialist roles automatically
- Tracks previously seen listings to avoid duplicate notifications
- Delivers new listings to Discord via webhook

## Setup
1. Get a free API key from developer.adzuna.com
2. Create a Discord webhook in your server settings
3. Add your credentials to the top of `main.py`
4. Run with: `python main.py`

## Concepts demonstrated
- REST API integration using the Requests library
- Webhook automation
- File-based persistence for deduplication
- Keyword filtering and data cleaning
- Automated scheduling via polling loop
