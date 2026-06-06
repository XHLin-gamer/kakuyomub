from gevent import monkey
monkey.patch_all()

import re
from kakuyomub.main import main as download

url = input("Paste the kakuyomu.jp novel URL: ").strip()

match = re.search(r'/works/(\d+)', url)
if not match:
    print("Couldn't find a work ID in that URL. Make sure it looks like: https://kakuyomu.jp/works/16817330668128729529")
    exit(1)

work_id = match.group(1)
print(f"Downloading work {work_id}...")
download(work_id)
print("Done! The EPUB has been saved in the current folder.")
