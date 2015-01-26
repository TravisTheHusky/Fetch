#The Title Block
print("-----------------------\n        Fetch\n E621 Pool Downloader\nWritten by TravisHusky\ntravishusky.tumblr.com\n-----------------------")

#Load Modules
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os

harvest_list = []

#Spider fetches all of the links to all of the images in the pool
def spider(poolid):
    url = 'https://e621.net/pool/show/' + str(poolid)
    source = requests.get(url)
    source_decoded = source.text
    soup = BeautifulSoup(source_decoded)
    for link in soup.findAll('a', {'class': 'tooltip-thumb'}):
        href = link.get('href')
        harvest_list.append('https://e621.net/' + href)

#fetch_image downloads the full size image from the page spider provides
def fetch_image(target_array, pid):
    name = 1
    try:
        os.stat(pid)
    except:
        os.mkdir(pid)
    for x in target_array:
        print('Downloading image ' + str(name) + ' of ' + str(len(target_array)))
        image_page_raw = requests.get(x)
        image_page_decoded = image_page_raw.text
        image_link_location = re.search('<li>Size: <a href="(.+?)" id=', image_page_decoded)
        image_link = image_link_location.group(1)
        file_type = image_link[-4:]
        urllib.request.urlretrieve(image_link, pid + '/' + str(name) + file_type)
        name = name + 1
    print('All images have been successfully downloaded from pool ' + pid)

#The Pool ID is the numbers on the end of the url
print('The Pool ID is the last digits at the end of the url')
print('Example: https://e621.net/post/show/XXXXX - The Xs would be the Pool ID')
pid = input('Pool ID: ')
print('-----------------------')
spider(pid)
numberoflinks = len(harvest_list)
print(str(numberoflinks) + ' images found... Fetching')
print('-----------------------')
fetch_image(harvest_list, pid)
