import sys
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve
mods = {"%2f": "/", "%3a": ":", "%2520": " "}


def pretty(html_file):
    fp = open(html_file, "r")
    html_text = fp.read()
    fp.close()

    soup = BS(html_text, "html.parser")
    html = soup.prettify()
    fp = open("pretty_google.html", "w")
    fp.write(html)
    fp.close()


def get_images(url_file):
    fp = open(url_file, "r")
    urls = fp.readlines()
    for i, url in enumerate(urls):
        print(urlretrieve(url, filename="image"+str(i)))
        break


def get_img_link(url):
    murl = url.split("mediaurl=")[1]
    img = murl.split("&")[0]
    for key, value in mods.items():
        img = img.replace(key, value)
        img = img.replace(key.upper(), value)
    fp = open("urls.txt", "a")
    fp.write(img)


def parse_href(links, key, prefix):
    for link in links:
        href = link["href"]
        if key in href:
            get_img_link(prefix+href)


def get_img_index_links(html_file):
    fp = open(html_file, "r")
    html_text = fp.read()
    fp.close()
    soup = BS(html_text, "html.parser")
    links = soup.find_all("a")
    google = soup.find("base")
    if google:
        key = "/imgres/imgurl?"
        prefix = "https://www.google.com"
    else:
        key = "/images/search?view"
        prefix = "https://www.bing.com"
    parse_href(links, key, prefix)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <html_file>")
        sys.exit(0)

    html_file = sys.argv[1]
    # pretty(html_file)
    # get_img_index_links(html_file)
    get_images(html_file)
