# Reddit content downloader

A python program to download videos from all comments of a specific Thread.

## Prerequisites

Run `pip install -r requirements.txt` to install project dependencies.

## Configuration

To make this works, you have to replace the values in `config.sample.json` with yours and save the file as `config.json`.

Check out [this guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to get your app's **client ID** and **secret**. 

Check out [this guide](https://github.com/reddit-archive/reddit/wiki/API#rules) to set up a correct **user agent**.

## Run

Use `python reddit_videos_downloader.py` to run the script and download the videos. This will create a `download/` folder with all downloaded videos.

Provide the thread link with the `-i` argument. For exemple :

`python reddit_videos_downloader.py -i https://www.reddit.com/r/AskReddit/comments/bjliax/what_is_your_favorite_video_on_the_internet_that/`