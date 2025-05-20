from setuptools import setup, find_packages            #这个包没有的可以pip一下
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')
setup(
    name = "kakuyomub",      #这里是pip项目发布的名称
    version = "0.2.0",  #版本号，数值大的会优先被pip
    keywords = ("kakuyomu", "epub"),
    description = "Convert kakuyomu articles to one epub file",
    long_description = long_description,
    long_description_content_type='text/markdown',
    license = "MIT Licence",

    url = "https://github.com/XHLin-gamer/kakuyomub",     #项目相关文件地址，一般是github
    author = "XHLin-gamer",
    author_email = "earllin@shu.edu.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
            'grequests',
            'loguru',
            'bs4',
            'jinja2',
            'requests',
            'ebooklib',
            'PrettyPrintTree'
        ]          #这个项目需要的第三方库
)