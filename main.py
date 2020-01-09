import requests
# from bs4 import BeautifulSoup
from pprint import pprint

KEYWORDS = [
    "筝",
    # "瑶筝",
    # "宝筝",
    # "玉柱",
    # "雁柱",
    # "银甲",
    # "秦筝",
    # "银筝",
    # "哀筝",
    # "玉筝",
    # "锦筝",
    # "桓筝",
    # "钿筝",
    # "筝柱",
]

HOST = "https://so.gushiwen.org/"

class Handler(object):
    def __init__(keyword):
        self.page_url = "{}/search.aspx?value={}".format(HOST, keyword)
        self.page_dom_tree = None
        self.items = []

    def process():
        print("开始处理诗词关键字: {}".format(self.keyword))
        while self.page_url:
            self.handle_page()

        print("已处理完处理诗词关键字: {}".format(keyword))


    def handle_page():
        self.page_dom_tree = self.get_page_dom_tree()
    
        self.page_url = self.get_next_page_url()
        self.items.extends(self.list_items())

    def get_page_dom_tree():
        try:
            response = requests.get(self.page_url)
            response.raise_for_status()
        except Exception:
            raise Exception('Got exception when request url: {}'.format(self.page_url))

        dom = BeautifulSoup(response.text)
        pprint(dom)
        return dom
    
    def list_items():
        pass
    
    def build_item():
        pass

    def save_to_excel():
        pass

if __name__ == "__main__":
    for k in KEYWORDS:
        Handler(k).process()
