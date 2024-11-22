#!/usr/bin/env python
import requests
import html
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
endpoint = "https://tickets.public.gr/_api/search?q="
url_endpoint = "https://tickets.public.gr"

# List of search terms
search_terms = [
    "larisa",
    "larissa",
    "λαρισα",
    "λάρισα",
    "λαρισσα",
    "λάρισσα",
]

# Dictionary to store unique events
unique_events = {}

# Function to send messages via Telegram
def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

# Fetch and collect unique events
for term in search_terms:
    search_url = endpoint + term
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        events = data.get("results", {}).get("events", [])
        for event in events:
            event_id = event["resultId"]
            if event_id not in unique_events:
                unique_events[event_id] = event
    else:
        print(f"Error fetching data for search term '{term}': {response.status_code}")

# Build the message
message_lines = []
print("Found events:")
for event in unique_events.values():
    title = html.escape(event["title"])
    url = url_endpoint + event["url"]
    print(f" - {event['title']}: {url}")
    message_lines.append(f' - <a href="{url}">{title}</a>')

# Join all message lines
message = "\n".join(message_lines)

# Split message if it exceeds Telegram"s character limit
MAX_MESSAGE_LENGTH = 4096
if len(message) > MAX_MESSAGE_LENGTH:
    messages = []
    current_message = ""
    for line in message_lines:
        if len(current_message) + len(line) + 1 < MAX_MESSAGE_LENGTH:
            current_message += line + "\n"
        else:
            messages.append(current_message)
            current_message = line + "\n"
    if current_message:
        messages.append(current_message)
else:
    messages = [message]

# Send messages
for msg in messages:
    send_telegram_message(bot_token, chat_id, msg)
