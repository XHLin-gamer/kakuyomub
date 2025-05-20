from gevent import monkey
monkey.patch_all()

from .epub_maker import Epub_maker

from .works import Works, chapter

import argparse

parser = argparse.ArgumentParser(description='カクヨム => Epub')
parser.add_argument('work_id', help='the id of the work')

def main(id,path = None):
    """download work to epub with id, and move the file to the path

    Args:
        id (str|int): the work id
        path (str, optional): the target path. Defaults to None.
    """
    w = Works(id)

    title = w.title
    maker = Epub_maker('test_epub1',title,w.author)

    def build_pages(node: chapter, toc: list):
        for episode in  node.episodes:
            chap = maker.add_chapter('', episode.title, episode.html_file,id =episode.episode_id)
            toc.append(chap)
        for chapter in node.children:
            toc.append([maker.section(chapter.title) ,build_pages(chapter, list())])
        return toc

    toc = build_pages(w.content, list())

        
    maker.set_toc(toc)
    maker.set_spine()
    maker.add_navi()

    maker.write_epub('.')
    
    
        
if __name__ == "__main__":
    args = parser.parse_args()
    # print()
    main(args.work_id)