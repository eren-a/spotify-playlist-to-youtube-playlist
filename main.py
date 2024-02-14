import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from googleapiclient.discovery import build


load_dotenv()


def get_playlist_tracks(username, playlist_id):
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope, username=username))

    results = sp.playlist_tracks(playlist_id)
    return results['items']


def extract_playlist_tracks_info(tracks):
    playlist_info = []
    for track in tracks:
        name = track['track']['name']
        artists = [artist['name'] for artist in track['track']['artists']]
        playlist_info.append({'name': name, 'artists': artists})

    return playlist_info


def search_youtube_video(api_key, query, max_results=5):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key

    # Build the YouTube API service
    youtube = build('youtube', 'v3')

    # Make a search request
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=max_results
    )

    response = request.execute()

    # Print video details
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        print(f"Video Title: {title}, Video ID: {video_id}")


if __name__ == "__main__":
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
    username = os.environ.get("SPOTIPY_USERNAME")
    playlist_id = os.environ.get("SPOTIPY_PLAYLIST_ID")

    if not all([client_id, client_secret, redirect_uri, username, playlist_id]):
        print("Please set the following environment variables: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME, SPOTIPY_PLAYLIST_ID, SPOTIPY_USERNAME, YOUTUBE_API_KEY, GOOGLE_APPLICATION_CREDENTIALS")
        exit(1)

    # Set Spotify API credentials
    os.environ["SPOTIPY_CLIENT_ID"] = client_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
    os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

    tracks = get_playlist_tracks(username, playlist_id)
    tracks = extract_playlist_tracks_info(tracks)

    # search each track individually
    api_key = os.environ.get("YOUTUBE_API_KEY")
    search_youtube_video(api_key, tracks[0], 3)
    
    # add the songs to a playlist 
