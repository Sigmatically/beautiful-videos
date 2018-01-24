"""
Contains functions to read both the Achievement Hunter Website (and their other pages)
and a Youtube channel 'videos' page.
"""

import datetime
import requests
from bs4 import BeautifulSoup

def latest_youtube(channel, size=5):
    """
    Takes a Youtube channel link or list of Youtube channel links and pulls out a specified
    amount of the most recent videos from those pages
    """

    # Initiate variables
    title = []
    url = []
    date_uploaded = []
    created_at = []

    # Grab the HTML from the channel page and make it easily readable for python
    page_html = requests.get(channel)
    html_text = page_html.text
    soup = BeautifulSoup(html_text)

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

    return {"name": channel_name, "title": title, "url": url,
            "uploaded": date_uploaded, "created": created_at}
