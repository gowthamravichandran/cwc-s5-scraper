# This is a sample Python script.
import homepage_scraper
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    episodes = homepage_scraper.scrape_cooku_with_comali_s5()
    # Print the results
    for episode in episodes:
        print(f"Title: {episode['title']}")
        print(f"Date: {episode['date']}")
        print(f"Episode Link: {episode['link']}")
        print("Thirai Links:")
        for thirai in episode['thirai_links']:
            print(f"  {thirai['name']}: {thirai['link']}")
        print("---")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
