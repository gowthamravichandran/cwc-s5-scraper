import requests
from bs4 import BeautifulSoup
import re
import yt_dlp
import os
import json
import requests

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



def get_dailymotion_video_info(video_id):

    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    print(api_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cookie': 'v1st=5E19518A0E0379048E7766AFCD9B5E9B; ts=257075; usprivacy=1---; dmvk=6680bb7beacf3; _TEST_=1; uid_dm=373df28f-3a15-f888-09d5-4ed1c15d6d0c; lang=en_US; client_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhaWQiOiJmMWEzNjJkMjg4YzFiOTgwOTljNyIsInJvbCI6ImNhbi1tYW5hZ2UtcGFydG5lcnMtcmVwb3J0cyBjYW4tcmVhZC12aWRlby1zdHJlYW1zIGNhbi1zcG9vZi1jb3VudHJ5IGNhbi1hZG9wdC11c2VycyBjYW4tcmVhZC1jbGFpbS1ydWxlcyBjYW4tbWFuYWdlLWNsYWltLXJ1bGVzIGNhbi1tYW5hZ2UtdXNlci1hbmFseXRpY3MgY2FuLXJlYWQtbXktdmlkZW8tc3RyZWFtcyBjYW4tZG93bmxvYWQtbXktdmlkZW9zIGFjdC1hcyBhbGxzY29wZXMgYWNjb3VudC1jcmVhdG9yIGNhbi1yZWFkLWFwcGxpY2F0aW9ucyIsInNjbyI6InJlYWQgd3JpdGUgZGVsZXRlIGVtYWlsIHVzZXJpbmZvIGZlZWQgbWFuYWdlX3ZpZGVvcyBtYW5hZ2VfY29tbWVudHMgbWFuYWdlX3BsYXlsaXN0cyBtYW5hZ2VfdGlsZXMgbWFuYWdlX3N1YnNjcmlwdGlvbnMgbWFuYWdlX2ZyaWVuZHMgbWFuYWdlX2Zhdm9yaXRlcyBtYW5hZ2VfbGlrZXMgbWFuYWdlX2dyb3VwcyBtYW5hZ2VfcmVjb3JkcyBtYW5hZ2Vfc3VidGl0bGVzIG1hbmFnZV9mZWF0dXJlcyBtYW5hZ2VfaGlzdG9yeSBpZnR0dCByZWFkX2luc2lnaHRzIG1hbmFnZV9jbGFpbV9ydWxlcyBkZWxlZ2F0ZV9hY2NvdW50X21hbmFnZW1lbnQgbWFuYWdlX2FuYWx5dGljcyBtYW5hZ2VfcGxheWVyIG1hbmFnZV9wbGF5ZXJzIG1hbmFnZV91c2VyX3NldHRpbmdzIG1hbmFnZV9jb2xsZWN0aW9ucyBtYW5hZ2VfYXBwX2Nvbm5lY3Rpb25zIG1hbmFnZV9hcHBsaWNhdGlvbnMgbWFuYWdlX2RvbWFpbnMgbWFuYWdlX3BvZGNhc3RzIiwibHRvIjoiWXpSWVExcGFkRmhmVlRZX0ZsYzJURnMwTUFRRFNobFBHaWNGSHciLCJhaW4iOjEsImFkZyI6MSwiaWF0IjoxNzE5NzEzMzUxLCJleHAiOjE3MTk3NDg5MDIsImRtdiI6IjEiLCJhdHAiOiJicm93c2VyIiwiYWRhIjoid3d3LmRhaWx5bW90aW9uLmNvbSIsInZpZCI6IjVFMTk1MThBMEUwMzc5MDQ4RTc3NjZBRkNEOUI1RTlCIiwiZnRzIjoyNTcwNzUsImNhZCI6MiwiY3hwIjoyLCJjYXUiOjIsImtpZCI6IkFGODQ5REQ3M0E1ODYzQ0Q3RDk3RDBCQUIwNzIyNDNCIn0.U8zXWqSrQrrTq1KdLH7GtmrVz9hb5RdPtvB5Tzjzm7s; dmaid=f1a4236c-bb7c-4dd6-8749-41d892afa558; ff=on'


    }
    response = requests.get(api_url, headers=headers)
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

            # Download the video
            response = requests.get(video_download_url, stream=True)
            if response.status_code == 200:
                file_name = f"{video_info.get('title', 'video')}.mp4"
                file_path = os.path.join(output_path, file_name)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Video downloaded successfully: {file_path}")
                return True
            else:
                print(f"Failed to download video. Status code: {response.status_code}")
        else:
            print("No video qualities found in the API response")
    return False


def process_thirai_links(thirai_links, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for link in thirai_links:
        print(f"Processing: {link}")
        video_url = extract_dailymotion_video_url(link)
        if video_url:
            print(f"Found Dailymotion video URL: {video_url}")
            success = download_video(video_url, output_folder)
            if not success:
                print("Failed to download video")
        else:
            print("No Dailymotion video found on this page.")
        print("---")


# The extract_dailymotion_video_url function remains the same as in your previous code

# Example usage
thirai_links = [
    "https://globalnewsphere.com/the-us-will-require-automatic-emergency-braking-in-novel-vehicles/",
    # Add other links here
]

output_folder = "downloaded_videos"

process_thirai_links(thirai_links, output_folder)