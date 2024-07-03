import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def get_episode_links(url):
    print(f"get_episode_links{url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='regular-post')
    print(f"found articles: {len(articles)}")
    episodes = []
    for article in articles:
        title_element = article.find('h3', class_='entry-title')
        if title_element and title_element.a:
            title = title_element.a.text.strip()
            link = title_element.a['href']
            date_match = re.search(r'(\d{2}-\d{2}-\d{4})', title)
            date = datetime.strptime(date_match.group(1), '%d-%m-%Y').date() if date_match else None
            episodes.append({'title': title, 'link': link, 'date': date})
    print(f"returning {len(episodes)} episodes")
    return episodes


def get_episode_content(episode_url):
    print(f"get_episode_content({episode_url})")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(episode_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    entry_content = soup.find('div', class_='entry-content')
    print("finding thirai links")
    thirai_links = []
    if entry_content:
        thirai_sections = entry_content.find_all('h4', class_='wp-block-heading')
        for section in thirai_sections:
            thirai_name = section.text.strip()
            next_figure = section.find_next('figure')
            if next_figure and next_figure.a:
                link = next_figure.a['href']
                thirai_links.append({'name': thirai_name, 'link': link})
    print(f"returning {len(thirai_links)} thirai_links")
    return thirai_links


def scrape_cooku_with_comali_s5():
    base_url = "https://www.tamildhool.net/vijay-tv/vijay-tv-show/cooku-with-comali-s5/"
    print("getting episode links")
    episodes = get_episode_links(base_url)

    for episode in episodes:
        print(f"getting thirai link for episode {episode['title']}")
        episode['thirai_links'] = get_episode_content(episode['link'])

    return episodes


