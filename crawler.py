import requests
import queue
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def check_scheme(scheme):
    return scheme in ('http', 'https')

seeds = ['https://cs.purdue.edu']
visited_set = set([])
crawl_frontier = queue.Queue()
for seed_url in seeds:
    crawl_frontier.put(seed_url)
while not crawl_frontier.empty():
    url_to_visit = crawl_frontier.get()
    try:
        r = requests.get(url_to_visit)
    except Exception as e:
        print(e)
        continue
    print(url_to_visit)
    visited_set.add(url_to_visit)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        parsed_url_object = urlparse(link.get('href'))
        if parsed_url_object.scheme == '' or parsed_url_object.netloc == '' or \
                not check_scheme(parsed_url_object.scheme):
            continue
        try:
            minimal_url = parsed_url_object.scheme + '://' + parsed_url_object.netloc
        except:
            print("EXCEPTION!!!", parsed_url_object.scheme, parsed_url_object.netloc)
        if minimal_url not in visited_set:
            visited_set.add(minimal_url)
            crawl_frontier.put(minimal_url)

    if crawl_frontier.qsize() > 500:
        break
