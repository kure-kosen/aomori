import os
import sys
from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup


from time import time, sleep
from urllib.request import urlopen, Request
from mimetypes import guess_extension
import traceback

class Fetcher:
    def __init__(self, ua=''):
        self.ua = ua

    def fetch(self, url):
        req = Request(url, headers={'User_Agent': self.ua})
        try:
            with urlopen(req, timeout=3) as p:
                b_content = p.read()
                mime = p.getheader('Content-Type')
        except:
            sys.stderr.write('Error in fetching {}\n'.format(url))
            sys.stderr.write(traceback.format_exc())
            return None, None
        return b_content, mime


fetcher = Fetcher('Mozilla/5.0')#ユーザーエージェント
page_num = 20
dirname =  'datasets/cards'

#画像保存用ファイル作成
if not os.path.exists(dirname):
    os.makedirs(dirname)

#PhantomJSをSelenium経由で利用します。
# url = "https://search.yahoo.co.jp/image/search?p=%E8%A1%9B%E8%97%A4%E7%BE%8E%E5%BD%A9&oq=&ei=UTF-8&save=0"
url = "https://search.yahoo.co.jp/image/search?p=%E3%83%88%E3%83%A9%E3%83%B3%E3%83%97+%E3%82%AB%E3%83%BC%E3%83%89&ei=UTF-8&rkf=1&oq=&save=0"
driver = webdriver.PhantomJS()

#PhantomJSで該当ページを取得&レンダリングします
driver.get(url)


for i in range(page_num):
    #レンダリング結果をPhantomJSから取得します。
    html = driver.page_source


    #画像のurlを取得する
    bs = BeautifulSoup(html, "html.parser")
    img_urls = [img.get("href") for img in bs.find_all("a", target="imagewin")]
    img_urls.remove("javascript:void(0);")
    img_urls = list(set(img_urls))
    #画像を保存する
    for j, img_url in enumerate(img_urls):
        sleep(0.1)
        img, mime = fetcher.fetch(img_url)
        if not mime or not img:
            continue
        ext = guess_extension(mime.split(';')[0])
        if ext in ('.jpe', '.jpeg'):
            ext = '.jpg'
        if not ext:
            continue
        result_file = os.path.join(dirname, str(i) + '_' + str(j) + ext)
        with open(result_file, mode='wb') as f:
            f.write(img)
        print('fetched', img_url)

    #次のページに移動する
    driver.find_element_by_link_text('次へ>').click()

driver.quit
