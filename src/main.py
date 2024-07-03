import homepage_scraper
import os
import thirailinks
from datetime import datetime
import re


def get_available_episode_dates(directory):
    episode_dates = []
    date_pattern = r'\d{4}-\d{2}-\d{2}'

    # Create list of episode dates
    for filename in os.listdir(directory):
        match = re.search(date_pattern, filename)
        if match:
            date_str = match.group()
            available_episode_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            episode_dates.append(available_episode_date)

    # Sort the list of dates
    episode_dates.sort()

    return episode_dates


if __name__ == '__main__':
    print(f'Starting execution on: {datetime.now()}')
    output_folder = '/app/tv/Cooku with Comali/Season 5/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    available_episode_dates = get_available_episode_dates(output_folder)
    episodes = homepage_scraper.scrape_cooku_with_comali_s5(available_episode_dates)

    # Print the results
    for episode in episodes:
        print(f"Title: {episode['title']}")
        print(f"Date: {episode['date']}")
        print(f"Episode Link: {episode['link']}")
        if "thirai_links" in episode:
            print("Thirai Links:")
            thirai_links = []
            for thirai in episode['thirai_links']:
                print(f"  {thirai['name']}: {thirai['link']}")
                thirai_links.append(thirai['link'])
            print("---")
            output_path = output_folder + f"CookuWithComali - {episode['date']}.mp4"
            thirailinks.process_thirai_links(thirai_links, output_path)
    print(f'Finishing execution on: {datetime.now()}')