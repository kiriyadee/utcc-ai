import os

import requests
from pytube import YouTube


def download_youtube_audio(url, output_path=None):
    try:
        # Validate URL first
        try:
            response = requests.head(url)
            response.raise_for_status()
        except requests.RequestException:
            raise ValueError("Invalid YouTube URL provided")

        # Create YouTube object with additional options to handle errors
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise ValueError("No audio stream found for this video")
        
        if not output_path:
            output_path = os.getcwd()
            
        # Download the audio
        out_file = audio_stream.download(output_path=output_path)
        
        # Convert to mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        return new_file
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
