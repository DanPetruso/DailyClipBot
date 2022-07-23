import scraper
import tweepy

import os
from os import listdir

def tweet():
    (title, channel) = scraper.download_clip()

    # data here deleted so no one steals my login info
    consumer_key = ''
    consumer_secret = ''
    bearer_token = r""
    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    clip = ""
    dir = os.getcwd()
    for file_name in listdir(dir):
        if file_name.endswith('.mp4'):
            clip = dir + "\\" + file_name

    # uploading clip in chunks since mp4 files are large then using the media data to post tweet with clip
    print("Uploading video to twitter...")
    media = api.media_upload(filename = clip, chunked = True, media_category = "TweetVideo")

    status = title + "\n\n-" + channel

    media_ids = [media.media_id_string]
    api.update_status(media_ids=media_ids, status=status)
    print("Clip uploaded")

if __name__ == '__main__':
    tweet()