import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from googleapiclient.discovery import build
import google_auth_oauthlib.flow

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
        playlist_info.append(f"{name} - {', '.join(artists)}")

    return playlist_info


def search_youtube_video(api_key, query):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key

    # Build the YouTube API service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Make a search request
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=1
    )

    response = request.execute()

    video_id = response['items'][0]['id']['videoId']
    return video_id


def create_playlist(api_key, video_ids, playlist_title, youtube_redirect_uri):
    # OAuth2 authentication

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl'], redirect_uri=youtube_redirect_uri)
    credentials = flow.run_local_server(port=8080)

    youtube = build('youtube', 'v3', developerKey=api_key,
                    credentials=credentials)

    # Create a new playlist
    playlist_request = youtube.playlists().insert(
        part='snippet',
        body={
            'snippet': {
                'title': playlist_title,
                'description': 'Playlist created via YouTube API'
            }
        }
    )
    playlist_response = playlist_request.execute()

    new_playlist_id = playlist_response['id']

    # Add videos to the playlist
    for video_id in video_ids:
        playlist_item_request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': new_playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        playlist_item_request.execute()

    print(f'Playlist created with ID: {new_playlist_id}')
    print(f'Videos added to the playlist.')


if __name__ == "__main__":
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
    username = os.environ.get("SPOTIPY_USERNAME")
    playlist_id = os.environ.get("SPOTIPY_PLAYLIST_ID")

    if not all([client_id, client_secret, redirect_uri, username, playlist_id]):
        print("Please set the following environment variables: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME, SPOTIPY_PLAYLIST_ID, SPOTIPY_USERNAME")
        exit(1)

    # Set Spotify API credentials
    # os.environ["SPOTIPY_CLIENT_ID"] = client_id
    # os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
    # os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

    tracks = get_playlist_tracks(username, playlist_id)
    tracks = extract_playlist_tracks_info(tracks)

    print(tracks)

    # search each track individually
    api_key = os.environ.get("YOUTUBE_API_KEY")

    video_ids = []
    for track in tracks:
        video_ids.append(search_youtube_video(api_key, track))

    # todo uri doesnt work
    youtube_redirect_uri = os.environ.get("YOUTUBE_REDIRECT_URI")
    create_playlist(api_key, video_ids,
                    "Automated Playlist pog", youtube_redirect_uri)
