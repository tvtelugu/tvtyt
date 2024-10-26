import json
import os
from googleapiclient.discovery import build
from github import Github

# YouTube API Key and GitHub Token from environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Match the secret name
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")   # Match the secret name
REPO_NAME = "tvtelugu/tvtyt"  # Your repository name

# Initialize APIs
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)

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
        print(f"An error occurred while fetching live streams: {e}")
        return []

# List of channels to track (replace with actual channel IDs)
channel_ids = [
    "@adityamusic",  # Replace with actual channel ID for Aditya Music
    "@ETVJabardasth"   # Replace with actual channel ID for ETV Jabardasth
]

all_streams = {channel_id: fetch_live_streams(channel_id) for channel_id in channel_ids}

# Convert to JSON and prepare to push to GitHub
json_data = json.dumps(all_streams, indent=2)
print("JSON data to upload:", json_data)

# Attempt to create or update the live_streams.json file
try:
    contents = repo.get_contents("live_streams.json")
    # Update the file if it exists
    print("Updating existing file...")
    repo.update_file("live_streams.json", "Updated live streams list", json_data, contents.sha, branch="main")
except Exception as e:
    print(f"Error updating file: {e}. Creating new file...")
    # If the file does not exist, create it
    repo.create_file("live_streams.json", "Initial commit of live streams list", json_data, branch="main")

print("Live streams list updated successfully.")
