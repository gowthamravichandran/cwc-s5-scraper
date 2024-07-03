import os
import re
import requests
import json
import subprocess
from bs4 import BeautifulSoup



def get_dailymotion_video_info(video_id):
    base_url = "https://www.dailymotion.com/player/metadata/video/"
    req = requests.Request('GET', base_url, params={'video': video_id})
    prepared_req = req.prepare()
    api_url = prepared_req.url

    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch video info. Status code: {response.status_code}")
        return None


def download_video(video_url, output_path):
    video_id = video_url.split('/')[-1]
    video_info = get_dailymotion_video_info(video_id)

    if video_info:
        print(f"Video info: {json.dumps(video_info, indent=2)}")

        if 'qualities' in video_info:
            # Get the highest quality video URL
            qualities = video_info['qualities']
            best_quality = max(qualities.keys(), key=lambda x: int(x) if x.isdigit() else 0)
            video_download_url = qualities[best_quality][0]['url']
            print(video_download_url)
            # Download the video using ffmpeg
            file_name = f"{video_info.get('title', 'video')}.mp4"
            file_path = os.path.join(output_path, file_name)
            ffmpeg_command = [
                'ffmpeg',
                '-i', video_download_url,
                '-c', 'copy',
                '-bsf:a', 'aac_adtstoasc',
                file_path
            ]

            try:
                subprocess.run(ffmpeg_command, check=True)
                print(f"Video downloaded successfully: {file_path}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Failed to download video: {e}")
                return False
        else:
            print("No video qualities found in the API response")
    return False


def extract_dailymotion_video_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    iframe = soup.find('iframe', src=re.compile(r'dailymotion.com/embed'))

    if iframe:
        video_url = iframe['src']
        video_id = re.search(r'video/([^?]+)', video_url)
        if video_id:
            return f"https://www.dailymotion.com/video/{video_id.group(1)}"

    return None


def process_thirai_links(links, output_path):

    for link in links:
        print(f"Processing: {link}")
        video_url = extract_dailymotion_video_url(link)
        if video_url:
            print(f"Found Dailymotion video URL: {video_url}")
            success = download_video(video_url, output_path)
            if not success:
                print("Failed to download video")
        else:
            print("No Dailymotion video found on this page.")
        print("---")


# Example usage
# thirai_links = [
#     "https://globalnewsphere.com/the-us-will-require-automatic-emergency-braking-in-novel-vehicles/",
#     # Add other links here
# ]
#
# output_folder = "downloaded_videos"
#
# process_thirai_links(thirai_links, output_folder)