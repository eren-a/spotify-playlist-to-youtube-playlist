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


def search_youtube_video(cloud_api_key, query):
    # Build youtube api
    youtube = build('youtube', 'v3', developerKey=cloud_api_key)

    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=1
    )

    response = request.execute()

    video_id = response['items'][0]['id']['videoId']
    return video_id


def create_playlist(cloud_api_key, video_ids, playlist_title, cloud_redirect_uri):
    # OAuth2 authentication
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl'], redirect_uri=cloud_redirect_uri)
    credentials = flow.run_local_server(port=8888)

    # Build youtube api
    youtube = build('youtube', 'v3', developerKey=cloud_api_key,
                    credentials=credentials)

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
    username = os.environ.get("SPOTIPY_USERNAME")
    playlist_id = os.environ.get("SPOTIPY_PLAYLIST_ID")
    
    tracks = get_playlist_tracks(username, playlist_id)
    tracks = extract_playlist_tracks_info(tracks)

    cloud_api_key = os.environ.get("CLOUD_API_KEY")

    # Array of all video id's
    video_ids = []
    for track in tracks:
        video_ids.append(search_youtube_video(cloud_api_key, track))


    cloud_redirect_uri = os.environ.get("CLOUD_REDIRECT_URI")
    create_playlist(cloud_api_key, video_ids,
                    "Automated Spotify Playlist", cloud_redirect_uri)
    
    
