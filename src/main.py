# This is a sample Python script.
import homepage_scraper
import os
import thirailinks
import datetime
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    output_folder = 'Cooku with Comali/Season 5/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    episodes = homepage_scraper.scrape_cooku_with_comali_s5()
    # Print the results
    for episode in episodes:
        print(f"Title: {episode['title']}")
        print(f"Date: {episode['date']}")
        print(f"Episode Link: {episode['link']}")
        print("Thirai Links:")
        thirai_links = []
        for thirai in episode['thirai_links']:
            print(f"  {thirai['name']}: {thirai['link']}")
            thirai_links.append(thirai['link'])
        print("---")
        print(thirai_links)
        episode_date = episode['date']
        if episode_date < datetime.date(2024, 6, 15):
            print(f"Skipping episode {episode_date} before Jun 15")
            continue
        output_path = output_folder + f"CookuWithComali - {episode_date}.mp4"
        thirailinks.process_thirai_links(thirai_links, output_path)
