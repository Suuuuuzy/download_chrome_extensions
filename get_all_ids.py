import requests, json, threading, os, time, sys, getopt
from tqdm import tqdm
import json
import config
from xml.etree.ElementTree import fromstring
from pebble import ThreadPool
import re
import os

def get_inner_elems(doc):
    """Get inner element."""
    return fromstring(doc).iterfind(r".//{{{}}}loc".format(
        config.const_sitemap_scheme()))


def is_generic_url(url):
    """Check if URL is a generic extension URL."""
    """The urls with a language parameter attached return a subset"""
    """of the ids that get returned by the plain urls, therefore we"""
    """skip urls with a language parameter."""

    return re.match(r"^{}\?shard=\d+$".format(
        config.const_sitemap_url()), url)


def iterate_shard(shard_url):
    if is_generic_url(shard_url):
        shard = requests.get(shard_url, timeout=10).text
        # print('shard', shard)
        for inner_elem in get_inner_elems(shard):
            overview_url = inner_elem.text
            yield re.search("[a-z]{32}", overview_url).group(0)


def process_shard(shard_url):
    return list(iterate_shard(shard_url))


def get_new_ids(known_ids, max_ids=None):
    """Crawl extension ids available in Chrome store."""

    shard_urls = [shard_elem.text for shard_elem in get_inner_elems(
        requests.get(config.const_sitemap_url(), timeout=10).text)]
    print('shard_urls', len(shard_urls))
    with ThreadPool(16) as pool:
        future = pool.map(process_shard, shard_urls, chunksize=1)
        iterator = future.result()

        returned_ids = 0
        while True:
            try:
                for extid in next(iterator):
                    if extid not in known_ids:
                        yield extid
                        returned_ids += 1
                        if max_ids is not None and returned_ids >= max_ids:
                            pool.stop()
                            return
            except StopIteration:
                return

filename = 'known_ids.txt'
if os.path.isfile(filename):
    with open(filename) as f:
        known_ids = json.load(f)
else:
    known_ids = []

discovered_ids = list(get_new_ids(known_ids, 100000))
known_ids.extend(discovered_ids)
known_ids = list(set(known_ids))
print(len(known_ids))
with open(filename, 'w') as f:
    json.dump(known_ids, f)
print(len(known_ids))

