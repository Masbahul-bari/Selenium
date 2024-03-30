from bs4 import BeautifulSoup
import requests
import re
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import os

# Function to authenticate and create the YouTube service
def get_authenticated_service(api_key):
    return build("youtube", "v3", developerKey=api_key)

# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to get all video IDs from a channel
def get_all_video_ids(service, channel_id):
    video_ids = []

    try:
        # Get the uploads playlist ID for the channel
        playlist_response = service.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        if "items" in playlist_response:
            uploads_playlist_id = playlist_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            # Get all videos in the uploads playlist
            playlist_items_response = service.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50
            ).execute()

            while playlist_items_response:
                for item in playlist_items_response.get("items", []):
                    video_id = item["contentDetails"]["videoId"]
                    video_ids.append(video_id)

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

# Function to get video details
def get_video_details(service, video_id):
    try:
        request = service.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        video_details = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']

        title = video_details['title']
        channel_name = video_details['channelTitle']
        comment_count = statistics.get('commentCount', 0)
        like_count = statistics.get('likeCount', 0)
        dislike_count = statistics.get('dislikeCount', 0)
        upload_date = video_details['publishedAt']
        view_count = statistics.get('viewCount', 0)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        description = video_details.get('description', '')

        return title, channel_name, comment_count, like_count, dislike_count, upload_date, view_count, video_url, description

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred while fetching video details:\n{e.content}")
        return None, None, None, None, None, None, None, None, None

# Function to get video comments
def get_video_comments(service, video_id, video_details):
    all_comments_data = {
        'type': 'Video',
        'source': 'YouTube',
        'post_url': video_details[7],
        'post_title': video_details[0],
        'posted_at': {'date': video_details[5]},
        'post_text': video_details[8],
        'post_topic': {'status': '', 'topic': {'label': '', 'score': ''}},
        'comments': [],
        'reactions': {'Total': video_details[6], 'Sad': '', 'Love': '', 'Wow': '', 'Like': video_details[3],
                      'Haha': '', 'Angry': '', 'Care': ''},
        'featured_image': [''],
        'total_comments': video_details[2],
        'percent_comments': '',
        'total_shares': '',
        'vitality_score': '',
        'checksum': ''
    }

    try:
        kwargs = {
            'part': 'snippet',
            'videoId': video_id,
            'maxResults': 100
        }

        while True:
            # Make request for comments
            results = service.commentThreads().list(**kwargs).execute()

            # Extract comments from the response
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                commenter_name = comment['authorDisplayName']
                commenter_profile_url = f"https://www.youtube.com/channel/{comment['authorChannelId']['value']}"
                comment_text = comment['textDisplay']

                # Add comment to comments list
                comment_data = {
                    'user_name': commenter_name,
                    'user_profile_url': commenter_profile_url,
                    'comment_text': comment_text,
                    'comments_replies': []
                }

                # Check for replies
                reply_count = item['snippet']['totalReplyCount']
                if reply_count > 0:
                    reply_comments = get_reply_comments(service, item['id'])
                    for reply in reply_comments:
                        reply_commenter_name = reply['authorDisplayName']
                        reply_profile_url = f"https://www.youtube.com/channel/{reply['authorChannelId']['value']}"
                        reply_text = reply['textDisplay']
                        comment_data['comments_replies'].append({
                            'user_name': reply_commenter_name,
                            'Replier_profile_url': reply_profile_url,
                            'Reply Text': reply_text
                        })

                all_comments_data['comments'].append(comment_data)

            # Check if there are more comments
            nextPageToken = results.get('nextPageToken')
            if not nextPageToken:
                break
            kwargs['pageToken'] = nextPageToken

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred while fetching comments:\n{e.content}")

    return all_comments_data


# Function to get reply comments
def get_reply_comments(service, parent_id):
    replies = []

    try:
        results = service.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText"
        ).execute()

        for item in results['items']:
            replies.append(item['snippet'])

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred while fetching reply comments:\n{e.content}")

    return replies

if __name__ == "__main__":
    # YouTube API key
    API_KEY = "AIzaSyBqEWhY-4ErABxe9rbS39Zk-BFX0XLErww"

    # Take channel name as user input
    channel_name = input("Enter the YouTube channel name: ")
    url = f"https://www.youtube.com/{channel_name}"
    soup = BeautifulSoup(requests.get(url, cookies={'CONSENT': 'YES+1'}).text, "html.parser")
    data_match = re.search(r"var ytInitialData = ({.*});", str(soup.prettify()))

    if data_match:
        json_data = json.loads(data_match.group(1))
        channel_id = json_data['header']['c4TabbedHeaderRenderer']['channelId']
        print(f"Channel ID for {channel_name}: {channel_id}")
    else:
        print("Error: Unable to find channel ID.")
        exit()

    # Authenticate and create the YouTube service
    youtube = get_authenticated_service(API_KEY)

    # Create a folder to store JSON files
    folder_path = f'{channel_name}_videos_data'
    create_folder_if_not_exists(folder_path)

    # Iterate over each video ID
    for video_id in get_all_video_ids(youtube, channel_id):

        try:
            # Get video details
            video_details = get_video_details(youtube, video_id)

            if video_details[0] is not None:
                # Check if comments are disabled for the video
                if video_details[2] == 0:
                    print(f"Comments are disabled for the video with ID: {video_id}")
                    continue

                # Get all comments for the video
                all_comments_data = get_video_comments(youtube, video_id, video_details)

                # Write all comments to a single JSON file
                all_comments_file_path = os.path.join(folder_path, f'{video_id}_all_comments.json')
                with open(all_comments_file_path, 'w') as json_file:
                    json.dump(all_comments_data, json_file, indent=4)

                print(f"\nAll comments for video ID {video_id} exported to the file {all_comments_file_path}")

            else:
                print(f"No video details found for video ID: {video_id}")

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
