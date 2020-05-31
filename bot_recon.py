import os
import twitter
import dotenv
import json
import random
import sys
import re
from pathlib import Path

dotenv.load_dotenv()
ARCHIVE_PATH = os.getenv('ARCHIVE_PATH')
ARCHIVE_URL = os.getenv('ARCHIVE_URL')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

regex = re.compile('(.*)\nFound in f', re.I)

def main():
    files = set()
    human_tweets = set()
    no_match = set()

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      tweet_mode='extended')

    total = api.GetUser(screen_name='ValveArchive').statuses_count
    print('Total Existing Tweets: ' + str(total))

    tl = []
    batch_size = 200

    for i in range(0, total, batch_size):
        if len(tl) > 0 and last_id == tl[-1].id:
            print('Reached end of feed. Terminating.')
            tl.pop()
            break
        if i != 0:
            last_id = tl[-1].id
        else:
            last_id = None
        print('Count: {count}/{total}. Querying {incr} more tweets. Max ID: {max_id}'.format(
            count=len(tl), total=total, incr=batch_size, max_id=last_id
        ))
        tl.extend(api.GetUserTimeline(screen_name='ValveArchive', include_rts=False, count=batch_size, max_id=last_id))
        
    print(str(len(tl)) + " total tweets")
    for tweet in tl:
        if "Valve Archive" in tweet.source:
            result = regex.match(tweet.full_text)
            if result:
                #if result[1] in files:
                #    print('DUPLICATE File: {id} {text}'.format(id=tweet.id, text=tweet.full_text))
                #else:
                files.add(result[1])
            else:
                no_match.add(tweet.full_text)
        else:
            human_tweets.add(tweet.full_text)

    print(str(len(files)) + " file paths")
    print(str(len(human_tweets)) + " human tweets")
    print(str(len(no_match)) + " non-matching tweets")

    tweets = {}
    tweets['files'] = list(files)
    tweets['human_tweets'] = list(human_tweets)
    tweets['no_match'] = list(no_match)

    with open('tweets.json', 'w') as f:
        json.dump(tweets, f, indent='\t')
    

if __name__ == '__main__':
    main()
