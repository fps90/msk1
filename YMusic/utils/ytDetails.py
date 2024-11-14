import os
import glob
import random
import json
import asyncio
import yt_dlp
from youtubesearchpython import VideosSearch, PlaylistsSearch
from urllib.parse import urlparse, parse_qs

def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Choosen File : {cookie_txt_file}\n')
    return cookie_txt_file

async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_txt_file(),
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

async def searchYt(query):
    try:
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()
        if not result["result"]:
            return None, None, None
        title = result["result"][0]["title"]
        duration = result["result"][0]["duration"]
        link = result["result"][0]["link"]
        
        duration_parts = duration.split(':')
        duration_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration_parts)))
        
        return title, duration_seconds, link
    except Exception as e:
        print(f"Error in searchYt: {e}")
        return None, None, None

async def download_audio(link, file_name):
    output_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join(output_path, f'{file_name}.%(ext)s'),
        'cookiefile': cookie_txt_file(),  
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'buffer-size': '16M',
        'quiet': True,  # Hide output unless there's an error
    }

    try:
        # Start downloading in a background task
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([link]))

        output_file = os.path.join(output_path, f'{file_name}.mp3')
        if not os.path.exists(output_file):
            raise Exception(f"File not downloaded successfully: {output_file}")
        
        return output_file, file_name, None  # Return title and duration if needed
    except Exception as e:
        print(f"Error in download_audio: {e}")
        return None, None, None

async def download_video(link, file_name):
    output_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, f'{file_name}.%(ext)s'),
        'cookiefile': cookie_txt_file(),  
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'buffer-size': '16M',
        'quiet': True,
    }

    try:
        # Start downloading in a background task
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([link]))

        output_file = os.path.join(output_path, f'{file_name}.mp4')
        if not os.path.exists(output_file):
            raise Exception(f"File not downloaded successfully: {output_file}")
        
        return output_file, file_name, None  # Return title and duration if needed
    except Exception as e:
        print(f"Error in download_video: {e}")
        return None, None, None

def searchPlaylist(query):
    query = str(query)
    playlistResult = PlaylistsSearch(query, limit=1)
    Result = playlistResult.result()
    if not Result["result"] == []:
        title = Result["result"][0]["title"]
        videoCount = Result["result"][0]["videoCount"]
        link = Result["result"][0]["link"]
        return title, videoCount, link
    return None, None, None

def extract_playlist_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get('list', [None])[0]
    return playlist_id

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path[1:]
    else:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
    return video_id
