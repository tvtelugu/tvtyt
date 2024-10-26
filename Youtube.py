import os
import json
import requests
from github import Github
from googleapiclient.discovery import build

# Replace with your API keys
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

# List of channel usernames
CHANNELS = ["adityamusic", "ETVJabardasth"]  # Add more usernames as needed

def get_channel_id(username):
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=id&forUsername={username}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items'][0]['id']
    return None

def get_live_streams(channel_id):
    url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def main():
    live_streams = {}
    
    for username in CHANNELS:
        channel_id = get_channel_id(username)
        if channel_id:
            streams = get_live_streams(channel_id)
            live_streams[username] = streams

    # Save the results to a JSON file
    with open("live_streams.json", "w") as f:
        json.dump(live_streams, f, indent=4)

    # Upload the JSON file to GitHub
    g = Github(ACCESS_TOKEN)
    repo = g.get_user().get_repo("tvtyt")
    with open("live_streams.json", "r") as f:
        json_data = f.read()
    
    try:
        repo.create_file("live_streams.json", "Update live streams", json_data, branch="main")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
