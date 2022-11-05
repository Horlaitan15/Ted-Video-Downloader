import urllib.request
from bs4 import BeautifulSoup
import re
import requests
import sys
from tqdm import tqdm
import pyfiglet



font = pyfiglet.figlet_format('TED Talk Video Downloader.')
print(font)
# Get url from CLI
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    sys.exit("Error: please enter the ted talk url.")

# Open the provided link to get the needed info.
res = urllib.request.urlopen(url).read()

# Instantiate the BeautifulSoup object.
soup = BeautifulSoup(res, 'lxml')

# Get the ele,ent that contains the video link.
main = soup.find("script", id="__NEXT_DATA__").contents

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}
# Get the video link.
video_link = re.findall(r"https://[\S]+mp4", str(main))[0]

# The name of the file to save the downloaded video.
file_name = video_link.split("/")[-1]

# Download video using the request library.
vid_content = 	requests.get(video_link, headers=headers, stream=True)

vid_size = int(vid_content.headers['content-length'])

print("Download about to start!")
# Save video content.
with open(file_name, 'wb') as con:
    for data in tqdm(iterable=vid_content.iter_content(chunk_size=1024), total = vid_size/1024, unit = 'KB'):
        con.write(data)

print("Download Complete!")
