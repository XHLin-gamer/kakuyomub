from loguru import logger
from bs4 import BeautifulSoup
import requests
import jinja2
import os

class Episodes():
    def __init__(self, work_id, episode_id, title = '') -> None:
        self.work_id = work_id
        self.episode_id = episode_id
        self.title = title
        
        self.episode_url = f"https://kakuyomu.jp/works/{self.work_id}/episodes/{self.episode_id}"
        
        self._is_check = False
        
        # self.fetch_content()
    def set_content(self, raw_html_file):
        
        soup = BeautifulSoup(raw_html_file, features="lxml")
        contentMain = soup.find('div', id = 'contentMain-inner')

        self.content = [str(p) for p in contentMain.find_all('p')[1:]]
        
        env = jinja2.Environment()
        with open('./src/template.html') as f:
            template = env.from_string(f.read())
        file = template.render(title = self.title, content = '\n'.join(self.content))
        self.html_file = file
        
        if not os.path.exists('./cache/'): os.makedirs('./cache/')
        
        with open(f'./cache/{self.episode_id}.html','w', encoding='utf8') as f:
            f.write(file)
        
        logger.info(f"Successfully fetched {self.title} => ./cache/{self.episode_id}.html")
        
    def is_check(self):
        return self._is_check
        
    def get_url(self):
        return self.episode_url    
        
    def fetch_content(self):
        cache = os.listdir('./cache/')
        if f'{self.episode_id}.html' in cache:
            logger.info(f'load from cache {self.title} <= ./cache/{self.episode_id}.html')
            self.html_file = open(f'./cache/{self.episode_id}.html', encoding='utf8').read()
            return
        
        try:
            res = requests.get(self.get_url())
        except:
            logger.error(f"Failed to fetch {self.title}, {self.get_url()}")

        soup = BeautifulSoup(res.text, features="lxml")
        contentMain = soup.find('div', id = 'contentMain-inner')
        # print(contentMain.find('header').text)
        # print(contentMain.find_all('p')[1:])
        self.content = [str(p) for p in contentMain.find_all('p')[1:]]
        
        env = jinja2.Environment()
        with open('./src/template.html') as f:
            template = env.from_string(f.read())
        file = template.render(title = self.title, content = '\n'.join(self.content))
        self.html_file = file
        with open(f'./cache/{self.episode_id}.html','w', encoding='utf8') as f:
            f.write(file)
        
        logger.info(f"Successfully fetched {self.title} => ./cache/{self.episode_id}.html")
            
        
        
        
    def __str__(self) -> str:
        if not self.is_check():
            return f"[Unfinished] {self.title}"
    
        
if __name__ == "__main__":
    test_episode = Episodes(16817330668128729529, 16817330668128757674)
    logger.info(test_episode)
    test_episode.fetch_content()