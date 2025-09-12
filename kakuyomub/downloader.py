import grequests
from .episode import Episodes
from loguru import logger

class Downloader():
    def __init__(self, episodes : list[Episodes], size = 30) -> None:
        self.episodes = episodes
        self.html_files = []
        self.urls = []
        self.size = size
        # add the user-agent to the header to bypass cloudfront; Thx leecming82 :)
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
        
    def handle_error(self, request, exception):
        logger.error(f"Download fail : {request.url}")
        
    def download(self):
        for episode in self.episodes:
            self.urls.append(episode.get_url())
        self.requests = (grequests.get(url, headers = self.header) for url in self.urls)
        self.responses = grequests.map(self.requests, size=self.size)
        for idx, response in enumerate(self.responses):
            self.episodes[idx].set_content(response.text)

            
if __name__ == '__main__':
    urls = [
        'https://kakuyomu.jp/works/16818093088208501166/episodes/16818093088315544074',
        'https://kakuyomu.jp/works/16818093088208501166/episodes/16818093088315653679'
    ]
    
    episodes = [Episodes('16818093088208501166','16818093088315544074') for url in urls]
    
    downloader = Downloader(episodes)
    
    downloader.download()
    
    for episode in episodes:
        print(episode.html_file)