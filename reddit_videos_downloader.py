import praw
import json
import os
import sys
import argparse

from praw.models import MoreComments
from pathlib import Path

import youtube_dl

LENGHT_YOUTUBE_V_PARAMETER = 11

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='Thread link')
    args = vars(parser.parse_args())

    if args['i'] is not None:
        return args['i']
    else:
        return None
        
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

        commentContent = str(comment.body.encode("utf-8"))
        if 'youtube' in commentContent:
            index_youtube = commentContent.find("youtube")
            index_beg = commentContent.find('http', 0, index_youtube)
            index_end = commentContent.find('?v=', index_beg) + len('?v=') + LENGHT_YOUTUBE_V_PARAMETER

            if index_end != -1:
                youtubeUrl = commentContent[index_beg:index_end] 
                print('Downloading %s...' % youtubeUrl)
                ydl_opts = {
                    'format':'mp4', 
                    'outtmpl': f'./download/%(title)s.%(ext)s'
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    try:
                        ydl.download([youtubeUrl])
                    except youtube_dl.utils.DownloadError as download_error:
                        print(f'Cannot download {youtubeUrl}')

def main():
    thread_url = get_args()

    download_all_videos(thread_url)

main()