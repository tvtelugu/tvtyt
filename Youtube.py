import os
import json
from googleapiclient.discovery import build
from github import Github

# Fetch API keys from environment variables
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# GitHub Authentication
repo = Github(ACCESS_TOKEN).get_repo("tvtelugu/tvtyt")

# Function to fetch live stream links
def fetch_live_streams(channel_id):
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            eventType="live",
            type="video"
        )
        response = request.execute()
        
        # Extracting video details
        live_streams = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            live_streams.append({"title": title, "url": f"https://www.youtube.com/watch?v={video_id}"})
        
        return live_streams

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# List of channels to track (replace with actual channel IDs)
channel_ids = ["adityamusic", "ETVJabardasth"]  # Update with actual IDs
all_streams = {channel_id: fetch_live_streams(channel_id) for channel_id in channel_ids}

# Convert to JSON and push to GitHub
json_data = json.dumps(all_streams, indent=2)

# Check if the file already exists in the repo
contents = None
try:
    contents = repo.get_contents("live_streams.json")
except:
    # File does not exist
    pass

if contents:
    # Update the file if it exists
    repo.update_file("live_streams.json", "Updated live streams list", json_data, contents.sha, branch="main")
else:
    # Create the file if it doesn't exist
    repo.create_file("live_streams.json", "Initial commit of live streams list", json_data, branch="main")

print("Live streams list updated successfully.")
