#!/usr/bin/env python

import os
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import hashlib

def get_pic(number_imgs, timespan):
    """Returns a list of the specified number of top images over the specified
    timeframe from wallbase.cc
    """
    url = "http://wallbase.cc/toplist"
    opts = {
        'section':'wallpapers', 'q':'', 'res_opt':'gteq', 
        'res':'1920x1080', 'aspect':'1.77', 'purity':'100', 
        'board':'21', 'thpp':number_imgs, 'ts':timespan
    }
    htmltext = requests.get(url, params = opts)
    page_urls = []
    img_urls = []
    soup = BeautifulSoup(htmltext.content)
    results = soup.findAll("a")
    
    for r in results:
        if "http://wallbase.cc/wallpaper/" in r['href']:
            page_urls.append(r['href'])

    for p in page_urls:
        wp_page = requests.get(p)
        wp_soup = BeautifulSoup(wp_page.content)
        wp_results = wp_soup.findAll("img")
        for res in wp_results:
            if "http://wallpapers.wallbase.cc/" in res['src']:
                img_urls.append(res['src'])

    return img_urls

def save_pic(url):
    """Saves a file to disk when given a URL"""
    save_path = sys.argv[1]
    hs = hashlib.md5(url.encode('UTF-8')).hexdigest()
    file_ext = url.split(".")[-1]
    to_save = (save_path + hs + "." + file_ext)
    if to_save != "":
        if os.path.isfile(to_save):
            print(hs + "." + str(file_ext) + "\texists, skipping...")
        else:
            print(hs + "." + str(file_ext) + "\tdownloading...")
            urllib.request.urlretrieve(url, to_save)

if __name__ == "__main__":
    for img in get_pic(32, "3d"):
        save_pic(img)