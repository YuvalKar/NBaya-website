import requests
import json
import os
from datetime import datetime

# Configuration
# Secrets will be injected via GitHub Actions environment variables
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
OUTPUT_FILE = 'discord_update.json'

def fetch_latest_message():
    if not DISCORD_TOKEN or not CHANNEL_ID:
        print("Error: Missing environment variables (DISCORD_TOKEN or CHANNEL_ID).")
        return

    headers = {
        'Authorization': f'Bot {DISCORD_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Fetch the last message from the channel
    url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=1'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        messages = response.json()

        if not messages:
            print("No messages found in the channel.")
            return

        latest_msg = messages[0]
        
        # Construct the minimal data we need for the frontend
        # Message ID is needed to build the link: https://discord.com/channels/{guild_id}/{channel_id}/{message_id}
        # Note: We need Guild ID (Server ID) for the link, or just use the invite link.
        # Let's try to extract relevant info.
        
        data = {
            "content": latest_msg.get('content', ''),
            "date": latest_msg.get('timestamp', datetime.now().isoformat()),
            "author": latest_msg.get('author', {}).get('username', 'N-Baya'),
            "id": latest_msg.get('id')
        }

        # Write to JSON file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully updated {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error fetching Discord message: {e}")

if __name__ == "__main__":
    fetch_latest_message()