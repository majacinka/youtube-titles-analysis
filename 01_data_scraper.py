import os
from googleapiclient.discovery import build
import csv
from isodate import parse_duration

# API key and parameters
api_key = "paste_api_key"
channel_id = "paste_channel_id"

# Build youtube client
youtube = build("youtube", "v3", developerKey=api_key)

# Fetch Channel Details
request = youtube.channels().list(part="contentDetails", id=channel_id)
response = request.execute()
playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Iterate through playlist
videos = []
nextPageToken = None
video_count = 0
max_videos = 40

while True:
    playlist_request = youtube.playlistItems().list(
        part="snippet", playlistId=playlist_id, maxResults=50, pageToken=nextPageToken
    )
    playlist_response = playlist_request.execute()

    video_ids = [
        item["snippet"]["resourceId"]["videoId"] for item in playlist_response["items"]
    ]
    video_request = youtube.videos().list(
        part="snippet,contentDetails,statistics", id=",".join(video_ids)
    )
    video_response = video_request.execute()

    for video in video_response["items"]:
        title = video["snippet"]["title"]
        views = video["statistics"].get("viewCount")
        duration = parse_duration(video["contentDetails"]["duration"])
        duration_in_seconds = int(duration.total_seconds())
        videos.append((title, views, duration_in_seconds))
        video_count += 1
        if video_count >= max_videos:
            break

    nextPageToken = playlist_response.get("nextPageToken")
    if not nextPageToken:
        break

    with open("yd.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Check if file is empty to decide whether to write headers
        file.seek(0, os.SEEK_END)
        if file.tell() == 0:
            writer.writerow(
                ["title", "views", "duration"]
            )  # Writing the header only if the file is empty

        for title, views, duration_in_seconds in videos:
            writer.writerow([title, views, duration_in_seconds])
