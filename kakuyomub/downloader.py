import grequests
from .episode import Episodes
from loguru import logger

class Downloader():
    def __init__(self, episodes : list[Episodes], size = 30) -> None:
        self.episodes = episodes
        self.html_files = []
        self.urls = []
        self.size = size
        
    def handle_error(self, request, exception):
        logger.error(f"Download fail : {request.url}")
        
    def download(self):
        for episode in self.episodes:
            self.urls.append(episode.get_url())
        self.requests = (grequests.get(url) for url in self.urls)
        self.responses = grequests.map(self.requests, size=self.size)
        for idx, response in enumerate(self.responses):
            self.episodes[idx].set_content(response.text)

            
if __name__ == '__main__':
    urls = [
        'https://kakuyomu.jp/works/16816927862239228940/episodes/16816927862239574472',
        'https://kakuyomu.jp/works/16816927862239228940/episodes/16816927862266993369'
    ]
    
    episodes = [Episodes('16816927862239228940','16816927862239574472') for url in urls]
    
    downloader = Downloader(episodes)
    
    downloader.download()
    
    for episode in episodes:
        print(episode.html_file)