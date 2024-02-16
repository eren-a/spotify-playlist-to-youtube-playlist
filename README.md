# Spotify playlist to Youtube playlist

This script allows you to create a YouTube playlist based on the tracks from a specified Spotify playlist.

## Set up environment variables

Create a .env file in the same directory as the script and provide the following environment variables:
```
SPOTIPY_CLIENT_ID=
SPOTIPY_CLIENT_SECRET=
SPOTIPY_PLAYLIST_ID=
SPOTIPY_REDIRECT_URI=
SPOTIPY_USERNAME=
CLOUD_API_KEY=
CLOUD_REDIRECT_URI=
```

Ensure that you have the necessary credentials for Google Cloud API. The credentials.json file should be present.

## Run the script

```
python main.py
```

## Follow the Authentication Process
The script will guide you through the OAuth2 authentication process for Google Cloud. Follow the prompts to authenticate.

## Playlist Creation:
The script will fetch tracks from the specified Spotify playlist, search for corresponding YouTube videos, and create a new YouTube playlist. The process will be logged in the console.

