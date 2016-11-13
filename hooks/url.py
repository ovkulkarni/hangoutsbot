import asyncio
import settings
import bs4
import re
import json

from requests import get, post, exceptions


class URLHook(object):

    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def get_short_url(self, url):
        try:
            r = post("https://www.googleapis.com/urlshortener/v1/url",
                     params={"key": settings.GOOGLE_API_KEY}, json=({"longUrl": url}), headers={'Content-Type': 'application/json'})
            data = json.loads(r.text)
            return data["id"]
        except exceptions.MissingSchema:
            shorten("http://" + url)
        except:
            return url

    def get_url_title(self, url):
        r = get(url)
        html = bs4.BeautifulSoup(r.text, 'html.parser')
        title = ""
        if html.title:
            title = html.title.text
        else:
            title = r.headers['content-type']
        return title

    @asyncio.coroutine
    def run(self, bot, conversation, user, text):
        matcher = re.compile(r"{}".format(self.regex))
        urls = []
        for word in text.split():
            if matcher.match(word):
                urls.append(matcher.match(word).group(1))
        for url in urls:
            message = "** {} ** - {}".format(self.get_url_title(url), self.get_short_url(url))
            yield from bot.send_message(conversation, message)


hook = URLHook("url", ".*(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+).*")
