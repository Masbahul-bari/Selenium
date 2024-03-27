from bs4 import BeautifulSoup
import requests
import re
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime
import os  # Import os module for file and directory operations

video_ids = []
video_id = []

# ------------------getting channel ID from channel name--------------


# Take channel name as user input
channel_name = input("Enter the YouTube channel name: ")
url = f"https://www.youtube.com/{channel_name}"

# Make the request to the URL with appropriate cookies
soup = BeautifulSoup(requests.get(url, cookies={'CONSENT': 'YES+1'}).text, "html.parser")

# Search for the JSON data containing channel information
data_match = re.search(r"var ytInitialData = ({.*});", str(soup.prettify()))#.group(1)

# # Load the JSON data
# json_data = json.loads(data)

# # Extract the channel ID
# channel_ids = json_data['header']['c4TabbedHeaderRenderer']['channelId']

# print(f"Channel ID for {channel_name}: {channel_ids}")

if data_match:
    # Load the JSON data
    json_data = json.loads(data_match.group(1))

    # Extract the channel ID
    channel_ids = json_data['header']['c4TabbedHeaderRenderer']['channelId']

    print(f"Channel ID for {channel_name}: {channel_ids}")
else:
    print("Error: Unable to find channel ID.")
    exit()

# Make the request to the URL with appropriate cookies
#soup = BeautifulSoup(requests.get(url, cookies={'CONSENT': 'YES+1'}).text, "html.parser")

# Search for the JSON data containing channel information
#data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

# Load the JSON data
# json_data = json.loads(data)

# Extract the channel ID
# channel_ids = json_data['header']['c4TabbedHeaderRenderer']['channelId']

# print(f"Channel ID for {channel_name}: {channel_ids}")

# ------------getting video IDs from channel ID------------------------

# Set up the YouTube Data API

DEVELOPER_KEY = "AIzaSyBqEWhY-4ErABxe9rbS39Zk-BFX0XLErww"  # Replace with your API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Replace channel_id with the actual channel ID you want to get video IDs from
channel_id = channel_ids  # Fix the variable name

def get_authenticated_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_all_video_ids(service, channel_id):
    video_ids = []

    try:
        # Get the uploads playlist ID for the channel
        playlist_response = service.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        # Check if the "items" key is present in the response
        if "items" in playlist_response:
            uploads_playlist_id = playlist_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            # Get all videos in the uploads playlist
            playlist_items_response = service.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50  # Adjust based on your needs
            ).execute()

            while playlist_items_response:
                for item in playlist_items_response.get("items", []):  # Use get to handle cases where "items" key is not present
                    video_id = item["contentDetails"]["videoId"]
                    video_ids.append(video_id)

                # Check if there are more videos in the playlist
                next_page_token = playlist_items_response.get("nextPageToken")
                if next_page_token:
                    playlist_items_response = service.playlistItems().list(
                        part="contentDetails",
                        playlistId=uploads_playlist_id,
                        maxResults=50,
                        pageToken=next_page_token
                    ).execute()
                else:
                    break

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred while fetching video IDs:\n{e.content}")

    return video_ids


if __name__ == "__main__":
    # Authenticate and create the YouTube service
    youtube = get_authenticated_service()

    def get_video_details(service, video_id):
        try:
            request = service.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()

            # Extract video details
            video_details = response['items'][0]['snippet']
            statistics = response['items'][0]['statistics']

            title = video_details['title']
            channel_name = video_details['channelTitle']
            comment_count = statistics.get('commentCount', 0)
            like_count = statistics.get('likeCount', 0)
            dislike_count = statistics.get('dislikeCount', 0)
            upload_date = video_details['publishedAt']
            view_count = statistics.get('viewCount', 0)

            return title, channel_name, comment_count, like_count, dislike_count, upload_date, view_count

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred while fetching video details:\n{e.content}")
            return None, None, None, None, None, None, None
    
    def get_video_comments(service, **kwargs):
        comments = []
        nextPageToken = None

        try:
            while True:
                # Make request for comments
                results = service.commentThreads().list(**kwargs, pageToken=nextPageToken).execute()

                # Extract comments from the response
                for item in results['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)

                    # Check for replies
                    reply_count = item['snippet']['totalReplyCount']
                    if reply_count > 0:
                        reply_comments = get_reply_comments(service, item['id'])
                        comments.extend(reply_comments)

                # Check if there are more comments
                nextPageToken = results.get('nextPageToken')
                if not nextPageToken:
                    break

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred while fetching comments:\n{e.content}")

        return comments
    
    def get_reply_comments(service, parent_id):
        replies = []
        try:
            results = service.comments().list(
                part="snippet",
                parentId=parent_id,
                textFormat="plainText"
            ).execute()

            for item in results['items']:
                reply = item['snippet']['textDisplay']
                replies.append(reply)

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred while fetching reply comments:\n{e.content}")

        return replies

    # Create a folder to store Excel files
    folder_path = f'{channel_name}_videos_data'
    create_folder_if_not_exists(folder_path)

    # Iterate over each video ID
    for video_id in get_all_video_ids(youtube, channel_id):

        try:
            # Get video details
            title, channel_name, comment_count, like_count, dislike_count, upload_date, view_count = get_video_details(youtube, video_id)

            if title is not None:
                # Check if comments are disabled for the video
                if comment_count == 0:
                    print(f"Comments are disabled futtoronor the video with ID: {video_id}")
                    continue

                # Get all comments for the video
                comments = get_video_comments(youtube, part="snippet", videoId=video_id, textFormat="plainText")

                # Create a DataFrame for video details and comments
                data = {
                    'Video Title': [title],
                    'Channel Name': [channel_name],
                    'Comment Count': [comment_count],
                    'Like Count': [like_count],
                    'Dislike Count': [dislike_count],
                    'Upload Date': [upload_date],
                    'View Count': [view_count],
                    'Comments': ['\n'.join(comments)]  # Combine all comments into a single string
                }

                video_data_df = pd.DataFrame(data)

                # Write each DataFrame to a new Excel file within the specified folder
                # file_path = os.path.join(folder_path, f'{video_id}_video_data.xlsx')
                file_path = os.path.join(folder_path, f'{video_id}_video_data.json')
                # video_data_df.to_excel(file_path, index=False)
                video_data_df.to_json(file_path, orient='records')


                # Print video details
                print(f"Video Title: {title}")
                print(f"Channel Name: {channel_name}")
                print(f"Comment Count: {comment_count}")
                print(f"Like Count: {like_count}")
                print(f"Dislike Count: {dislike_count}")
                print(f"Upload Date: {upload_date}")
                print(f"View Count: {view_count}")

                print(f"\nDetails and comments for video ID {video_id} exported to the file {file_path}")

            else:
                print(f"No video details found for video ID: {video_id}")

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
