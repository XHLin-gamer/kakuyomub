from loguru import logger
from requests import Session
from bs4 import BeautifulSoup
from PrettyPrint import PrettyPrintTree
from .episode import Episodes
from .downloader import Downloader

import json
import re



class chapter():
    def __init__(self,title, id, json = None, level = 0, work_id = None) -> None:
        self.title = title
        self.id = id
        self.level = level
        self.children: list = list()
        self.episodes: list[Episodes] = list()
        self.downloader = Downloader(self.episodes)
        self.work_id = work_id
        
        if json:
            self.json = json
            self.match_episode(self.json)

    def match_episode(self, json):
        if self.level != 0:
            key = f"TableOfContentsChapter:{self.id}"
            episode_data = json[key]['episodeUnions']
        else:
            episode_data = json['TableOfContentsChapter:']['episodeUnions']
            
        for item in episode_data:
            episode_id = item['__ref'].split(':')[-1]
            episode_data = json[f"Episode:{episode_id}"]
            episode_title = episode_data['title']
            self.episodes.append(Episodes(self.work_id, episode_id, episode_title))
            
        self.downloader.download()
        print(len(self.episodes))

    def add_child(self, child):
        self.children.append(child)
    
    def get_episodes(self):
        return self.episodes
    
    def get_child_info(self):
        res = []
        
        for child in self.children:
            res += [child.title]
            if child.children:
                res += [child.get_child_info()]
        return res
    
    def __str__(self) -> str:
        return f"{self.title} + {self.get_child_info()}"
    
def parse_meta_json(_json: json) -> dict:
    res = {}
    # allocate the data attribute of the json file
    # see bench.json to see more details on this json file
    data = _json['props']['pageProps']['__APOLLO_STATE__']
    
    # extract work id with regex 
    text = ''.join(data['ROOT_QUERY'].keys())
    x = re.findall(r'(?<=\()(.+?)(?=\))', text)
    meta_data = {}
    for x_text in x:
        k = dict(json.loads(x_text))
        meta_data.update(k)
    
    work_id = meta_data["id"]
    word_data = data[f'Work:{meta_data["id"]}']
    res['title'] = word_data['title']
    res['catchphrase'] = word_data['catchphrase']
    res['introduction'] = word_data['introduction']
    res['tagLabels'] = word_data['tagLabels']

    # generate the chapter tree structure
    chap_list = []
    for table_dict in word_data['tableOfContents']: 
        chap_list += [*table_dict.values()]
    
    # if there is no chapter tree structure, hint the flat structure
    if chap_list == ['TableOfContentsChapter:']: 
        logger.info('flat structure')
        root = chapter(res['title'],work_id,  data, 0, work_id)
        return res, root
    else:
        root = chapter(res['title'],res['title'])
        stack = [root]
        
        # Build the content tree
        for idx, chap_id in enumerate(chap_list):
            chap_j = data[chap_id[15:]]
            level, title =  chap_j['level'], chap_j['title']
            _id = chap_j['id']
            new = chapter(title, _id,data, level,work_id)
            if stack[-1].level < level:  
                stack[-1].add_child(new)
                stack.append(new)
            elif stack[-1].level == level:
                stack.pop(-1)
                stack[-1].add_child(new)
                stack.append(new)
            elif stack[-1].level > level:
                stack[level-1].add_child(new)
                stack.append(new)

        # use PrettyPrintTree to visualize the content tree
        pt = PrettyPrintTree(lambda x: x.children, lambda x: x.title,orientation=PrettyPrintTree.Horizontal)
        pt(root)
    
        
        
        return res, root
    


class Works():
    def __init__(self, work_id) -> None:
        self.work_id = work_id
        self._work_url = f'https://kakuyomu.jp/works/{self.work_id}'

        self.session = Session()
        
        self.json_raw : str = self.get_raw_json()
        parse_result = parse_meta_json(json.loads(self.json_raw))
        self.res : dict = parse_result[0]
        self.content : chapter = parse_result[1]
        # self.author = res['']
        self.title = self.res['title']
        self.catchphrase = self.res['catchphrase']
        self.introduction = self.res['introduction']
        self.tagLabels = self.res['tagLabels']

        
    def get_raw_json(self) -> str:
        
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        
        try:
            response = self.session.get(self._work_url)
            response.raise_for_status()
            f = open('./test.html','w', encoding='utf8')
            f.write(response.text)
            f.close()
        except Exception as e:
            logger.error(f"{e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        json_data = soup.find('script', id="__NEXT_DATA__")
        author_text = soup.find('title').text
        x = re.findall(r'(?<=（)(.+?)(?=\）)', author_text)
        # print(x, author_text)
        self.author = x[0]

        return json_data.text

    def get_content(self) -> chapter:
        return self.content
    
    def __str__(self) -> str:
        if not self.is_check():
            return f"[Unfinished] {self._work_url}"
        
if __name__ == "__main__":
    work = Works(16818093076629589128)
    print(*work.get_content().get_episodes())
    
    
    