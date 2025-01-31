import feedparser
import time
import hashlib
from datetime import datetime, timedelta
import yhchat
import re
from bs4 import BeautifulSoup

FEED_URLS = [
    # "https://www.example.com/feed",
    # ...
]

PUSH_TOKEN = "984547385"  # bot token
PUSH_GROUP = "group"  # push群组ID
INTERVAL = 60  # 检查间隔，单位：秒
MAX_IMAGE_HEIGHT = 160  # 图片最大高度，单位：像素

last_entry_guids = {}


def check_rss_updates(feed_url):
    global last_entry_guids

    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        print(f"获取 RSS 订阅失败 ({feed_url}): {e}")
        return

    if not feed.entries:
        print(f"RSS 订阅中没有条目 ({feed_url})。")
        return


    latest_entry = feed.entries[0] 
    last_entry_guid = last_entry_guids.get(feed_url)
    if latest_entry.guid != last_entry_guid:
        title = latest_entry.title
        link = latest_entry.link
        published = latest_entry.published_parsed
        published_datetime = datetime(*published[:6])
        published_formatted = published_datetime.strftime("%Y-%m-%d %H:%M:%S")


        content = ""
        if hasattr(latest_entry, 'content'):
            content = latest_entry.content[0].value
        elif hasattr(latest_entry, 'summary'):
            content = latest_entry.summary

        """
        soup = BeautifulSoup(content, "html.parser")
        for img in soup.find_all("img"):
            if img.get('src'):
                img['style'] = f"max-height:{MAX_IMAGE_HEIGHT}px;"
        content = str(soup)
        """
        source = feed.feed.title
        text = f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>{content}<br><br>发布时间：{published_formatted}<br>来源：{source}"
        
        try:
            yhchat.push(PUSH_TOKEN, PUSH_GROUP, "html", {"text": text})
            print(f"已推送更新 ({feed_url}): {title}")
        except Exception as e:
            print(f"推送消息失败 ({feed_url}): {e}")

        last_entry_guids[feed_url] = latest_entry.guid  # 更新 last_entry_guid


if __name__ == "__main__":
    print("RSS 订阅推送已启动...")

    while True:
        for feed_url in FEED_URLS:
            check_rss_updates(feed_url)
        time.sleep(INTERVAL)
