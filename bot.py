import os
import twitter
import dotenv
import json
import random
from pathlib import Path

dotenv.load_dotenv()
ARCHIVE_PATH = os.getenv('ARCHIVE_PATH')
ARCHIVE_URL = os.getenv('ARCHIVE_URL')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


def reset_queue():
    queue = []
    extensions = ('jpg', 'jpeg', 'png', 'gif')
    for ext in extensions:
        queue.extend(str(p.relative_to(ARCHIVE_PATH)) for p in Path(ARCHIVE_PATH).glob('**/*.' + ext))
    random.shuffle(queue)
    return queue


def next_pic():
    try:
        with open('queue.json', 'r') as queue_handle:
            queue = json.load(queue_handle)
            if len(queue) == 0:
                queue = reset_queue()
    except IOError:
        queue = reset_queue()
    pic = queue[0]
    queue = queue[1:]
    with open('queue.json', 'w') as queue_handle:
        json.dump(queue, queue_handle)
    return Path(pic)


def main():
    pic_path = next_pic()
    pic_fullpath = Path(ARCHIVE_PATH).joinpath(pic_path)
    pic_dir_url = ARCHIVE_URL + str(pic_path.parent).replace('\\', '/').replace(' ', '%20')

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)
    status = api.PostUpdate(
        'Found in folder: ' + pic_dir_url,
        media=open(pic_fullpath, 'rb')
    )
    print(status)


if __name__ == '__main__':
    main()
