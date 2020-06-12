import os
import sys
from bs4 import BeautifulSoup as BS
import urllib.request as urq
from urllib.parse import unquote
from urllib.error import HTTPError


def build_user_agent():
    agent = urq.build_opener()
    agent.addheaders = [
        ('User-agent',
         'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.1')
    ]
    urq.install_opener(agent)


def get_images(url_file, prefix, start_no):
    fp = open(url_file, "r")
    urls = fp.readlines()

    if not os.path.exists("downloads"):
        os.mkdir("downloads")
    prefix = "downloads/" + prefix

    for url in urls:
        url = url[:-1]
        print("Downloading image from ", url)
        filename = prefix + str(start_no)
        try:
            urq.urlretrieve(url, filename=filename)
            print("Downloaded ", filename)
            start_no += 1
        except HTTPError as e:
            print(e)
            print("Error on dowloading ", url)


def get_img_link(url):
    murl = url.split("mediaurl=")[1]
    img = murl.split("&")[0]
    return unquote(img)


def parse_href(links, key, prefix):
    print("Parsing links and storing it in \"urls.txt\"")
    fp = open("urls.txt", "w")
    for link in links:
        href = link["href"]
        if key in href:
            url = get_img_link(prefix+href)
            fp.write(url+"\n")
    print("parsing urls completed")


def get_img_index_links(html_file):
    fp = open(html_file, "r")
    html_text = fp.read()
    fp.close()
    soup = BS(html_text, "html.parser")
    links = soup.find_all("a")
    key = "/images/search?view"
    prefix = "https://www.bing.com"
    parse_href(links, key, prefix)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <html_file>")
        sys.exit(0)

    html_file = sys.argv[1]
    get_img_index_links(html_file)
    build_user_agent()
    get_images("urls.txt", "image", 1)
