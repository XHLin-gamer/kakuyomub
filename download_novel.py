from gevent import monkey
monkey.patch_all()

import re
from kakuyomub.main import main as download

url = input("Paste the kakuyomu.jp novel URL: ")
# Remove all whitespace and non-printable characters
url = re.sub(r'\s+', '', url)

# Accept either a full URL or just the numeric ID
match = re.search(r'/works/(\d+)', url) or re.fullmatch(r'\d+', url)
if not match:
    print(f"Couldn't find a work ID. Got: {repr(url)}")
    print("Expected something like: https://kakuyomu.jp/works/16817330668128729529")
    exit(1)

work_id = match.group(1) if match.lastindex else match.group(0)
print(f"Downloading work {work_id}...")
download(work_id)
print("Done! The EPUB has been saved in the current folder.")
