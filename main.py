import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess

# Loading the environment variables from .env file
load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# using the Spotipy API to authenticate with the users Spotify account
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                     client_id=client_id,
                     client_secret=client_secret
                     ))

# Setting the download directory (you can change this to your preferred directory)
download_dir = os.path.expanduser('~/Desktop')

choice = input("Do you want to download a Spotify playlist or a single song? (1 for playlist, 2 for song): ").strip()

if choice == '1':
    
    playlist_url = input("Enter the Spotify playlist URL: ").strip()

    res = sp.playlist_tracks(playlist_url)

    # Iterate through the tracks in the playlist and download them
    for item in res['items']:
        if item['track'] is not None:
            # Extracting track information
            track = item["track"]
            name = track["name"]
            artist = track["artists"][0]["name"]
            query = f"{name} {artist}"

            print(f"Downloading: {query}")
            
            # Using yt-dlp to download the track as mp3
            subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", os.path.join(download_dir, "%(title)s.%(ext)s"),
            f"ytsearch1:{query}"
        ])
        else:
            print("No track found in this item, skipping...")
            
elif choice == '2':
    
    # Ask user for song and artist
    song = input("Enter song name: ").strip()
    artist = input("Enter artist name: ").strip()
    query = f"{song} {artist}"

    print(f"Downloading: {query}")

    subprocess.run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", os.path.join(download_dir, "%(title)s.%(ext)s"),
        f"ytsearch1:{query}"
    ])