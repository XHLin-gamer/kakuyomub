from ebooklib import epub
import os

class Epub_maker():
    def __init__(self, identifier = '', title = '', author = '') -> None:
        self.book = epub.EpubBook()
        self.identifier = identifier
        self.title = title
        self.author = author
        
        self.book.set_identifier(self.identifier)
        self.book.set_title(self.title)
        self.book.set_language('ja')
        self.book.add_author(self.author)
        
        style = 'body { font-size: 10px; font-family: Roboto, Arial, sans-serif;}'

        nav_css = epub.EpubItem(uid="style_nav",
                                file_name="style/nav.css",
                                media_type="text/css",
                                content=style)
        
        self.book.add_item(nav_css)

        
        self.spine = ['nav']
        
    def add_chapter(self, path, title, content, id) -> epub.EpubHtml:
        chapter = epub.EpubHtml(title = title,file_name=f'{id}.xhtml', lang='ja')
        chapter.set_content(content)
        self.book.add_item(chapter)
        self.spine.append(chapter)
        return chapter
    
    def section(self, section_title):
        return epub.Section(section_title)
    
    def set_toc(self, toc):
        self.book.toc = toc
    
    def set_spine(self):
        self.book.spine = self.spine
        
    def add_navi(self):
        ## ナビファイルの追加
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        
    def write_epub(self, path):
        epub.write_epub(f'{path}/{self.title}.epub', self.book)
        
if __name__ == '__main__':
    title = '生意気な後輩に人生を全否定されたので、腹いせに屋上から飛び降りたらどうなるか検証してみた。'
    maker = Epub_maker('test_epub1',title,'式崎識也')
    for idx, file in enumerate(os.listdir('./cache')):
        file_path = f"./cache/{file}"
        with open(file_path, 'r', encoding='utf-8') as f: 
            # print(f.read())
            maker.add_chapter('', f'chap{idx}', f.read())
    
    maker.set_toc()
    maker.set_spine()
    maker.add_navi()
    
    maker.write_epub('.')
    

