import praw
import json
import os
import sys
import argparse
import re
from urllib.parse import urlparse, parse_qs

from praw.models import MoreComments
from pathlib import Path

import youtube_dl

LENGHT_YOUTUBE_V_PARAMETER = 11

YOUTUBE_DOWNLOAD_OPTIONS = {
    'format':'mp4', 
    'outtmpl': f'./download/%(title)s.%(ext)s'
}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='Thread link')
    args = vars(parser.parse_args())

    if args['i'] is not None:
        return args['i']
    else:
        return None
        
def download_youtube_video(url):
    with youtube_dl.YoutubeDL(YOUTUBE_DOWNLOAD_OPTIONS) as ydl:
        try:
            ydl.download([url])
        except youtube_dl.utils.DownloadError as download_error:
            print(f'ERROR : Cannot download {url} : {download_error}')
            
def download_all_videos(thread_url):
    config = json.load(open('config.json', 'r'))
    reddit = praw.Reddit(client_id=config['clientId'],
                        client_secret=config['clientSecret'],
                        user_agent=config['userAgent'])
    try:
        submission = reddit.submission(url=thread_url)
    except praw.exceptions.ClientException:
        print('ERROR : The input url is not correct. Please provide a valid Reddot thread.')
        sys.exit(0)

    p = Path(f'./download')
    if not p.exists():
        os.makedirs(f'./download')



    # https://praw.readthedocs.io/en/latest/tutorials/comments.html
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue

        # comment_content = str(comment.body.encode("utf-8"))
        comment_content = str(comment.body)
        all_urls = []
        urls_http = re.findall(r'(https?://[^\s]+)', comment_content)
        urls_https = re.findall(r'(http?://[^\s]+)', comment_content)

        if urls_http is not None:
            all_urls = all_urls + urls_http
        if urls_https is not None:
            all_urls = all_urls + urls_https

        print(all_urls)

        for url in all_urls:
            parsed_url = urlparse(url)
            if parsed_url.netloc == 'www.youtube.com':
                
                # Sometimes, we have some thingyes after v=ABCDEFGHIJ paramter, so we remove them.
                query_fix = parsed_url.query[0:len('v=') + LENGHT_YOUTUBE_V_PARAMETER]
                parsed_url = parsed_url._replace(query=query_fix)

                download_youtube_video(parsed_url.geturl())

            elif parsed_url.netloc == 'youtube.be':
                download_youtube_video(parsed_url.geturl())
                
def main():
    thread_url = get_args()

    download_all_videos(thread_url)

main()