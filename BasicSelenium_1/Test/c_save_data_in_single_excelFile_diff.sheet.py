from bs4 import BeautifulSoup
import requests
import re
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime

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

# ------------getting video IDs from channel ID------------------------

# Set up the YouTube Data API

DEVELOPER_KEY = "AIzaSyBqEWhY-4ErABxe9rbS39Zk-BFX0XLErww"  # Replace with your API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Replace channel_id with the actual channel ID you want to get video IDs from
channel_id = channel_ids  # Fix the variable name

def get_authenticated_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

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

    try:
        # Get all video IDs for the specified channel
        all_video_ids = get_all_video_ids(youtube, channel_id)

        # Print the video IDs
        print("Video IDs collection done")

        # Create an Excel writer object
        # excel_writer = pd.ExcelWriter('videos_data_1.xlsx', engine='xlsxwriter')
        excel_writer = pd.ExcelWriter(f'{channel_name}_videos_data.xlsx', engine='xlsxwriter')

 
        # Iterate over each video ID
        for video_id in all_video_ids:
            # Get video details
            title, channel_name, comment_count, like_count, dislike_count, upload_date, view_count = get_video_details(youtube, video_id)

            if title is not None:
                # Check if comments are disabled for the video
                if comment_count == 0:
                    print(f"Comments are disabled for the video with ID: {video_id}")
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
                    'View Count': [view_count]
                }

                # Add each comment to the DataFrame
                for i, comment in enumerate(comments):
                    data[f'Comment_{i+1}'] = [comment]

                video_data_df = pd.DataFrame(data)

                # Get current date and time for sheet name
                current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Write each DataFrame to a new sheet within the same Excel writer
                video_data_df.to_excel(excel_writer, sheet_name=video_id, index=False)

                # Print video details
                print(f"Video Title: {title}")
                print(f"Channel Name: {channel_name}")
                print(f"Comment Count: {comment_count}")
                print(f"Like Count: {like_count}")
                print(f"Dislike Count: {dislike_count}")
                print(f"Upload Date: {upload_date}")
                print(f"View Count: {view_count}")

                print(f"\nDetails and comments for video ID {video_id} exported to the sheet {video_id}")

            else:
                print(f"No video details found for video ID: {video_id}")

        # Save the Excel file
        excel_writer._save()
        print("Excel file saved successfully.")

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
