"""
Contains functions to read both the Achievement Hunter Website (and their other pages)
and a Youtube channel 'videos' page.
"""

import datetime
import json

import requests
from bs4 import BeautifulSoup

def latest_youtube(channels, size=5):
    """
    Takes a Youtube channel link or list of Youtube channel links and pulls out a specified
    amount of the most recent videos from those pages
    """

    if isinstance(channels, str):
        channels = [channels]

    # Initiate variables
    title = []
    url = []
    date_uploaded = []
    created_at = []

    # Iterating over a list of channel names
    for channel in channels:
        # Grab the HTML from the channel page and make it easily readable for python
        page_html = requests.get(channel)
        html_text = page_html.text
        soup = BeautifulSoup(html_text, 'lxml')

        channel_name = soup.find_all('title')[0].text.split()[0]
        video_list = soup.find_all('div', {"class": "yt-lockup-content"})[0:size]

        for video in video_list:
            # Seperate the video information
            video_attrs = video.contents[1].contents[0]
            video_upload = video.contents[3].find_all('li')[1].text

            # Add to container lists
            title.append(video_attrs["title"])
            url.append('http://www.youtube.com/' + video_attrs["href"])
            date_uploaded.append(video_upload)
            created_at.append(datetime.datetime.now())

    return {"name": "YouTube", "title": title, "url": url,
            "uploaded": date_uploaded, "created": created_at}

def latest_achievement_hunter(size=5):
    """
    Pulls the latest videos from the achievement hunter website
    filtering out a few of my least favorites
    """

    #Initialize variables
    title = []
    url = []
    date_uploaded = []
    created_at = []

    # Grab the html from the website and make it easily readable by python
    page_html = requests.get('http://achievementhunter.roosterteeth.com/')
    html_text = page_html.text
    soup = BeautifulSoup(html_text, "lxml")

    video_list = json.loads(str(soup.find(id="recent-carousel-comment").contents[1]))

    not_wanted_videos = ["Off Topic", "AHWU", "Last Call", "Let's Watch", "Shenanigans",
                         "Heroes & Halfwits", "Heroes & Halfwits Post Show"]

    filtered_video_list = [video for video in video_list if video["show_name"]
                           not in not_wanted_videos]

    for video in filtered_video_list[0:min([len(filtered_video_list), size])]:
        title.append(video["title"])
        url.append(video["url"])
        date_uploaded.append(video["published_at"]["date"])
        created_at.append(datetime.datetime.now())

    return {"name": "Achievement Hunter", "title": title, "url": url,
            "uploaded": date_uploaded, "created": created_at}
