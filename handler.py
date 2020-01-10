# -*- coding: utf-8 -*-
import requests
from xlsx import Xlsx


class Handler(object):
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
    URL_TEMP = "https://app.gushiwen.cn/api/search11.aspx?page={}&type=title&value={}&token=gswapi"

    def __init__(self):
        self._names = set()  # 诗名集合，用于排除重复诗词
        self._total_page = 0  # 总页数
        self._page_data = None  # 每一页的数据
        self._dynasty2data = {}  # 解析出的数据

    def process(self):
        for k in self.KEYWORDS:
            self.process_keyword(k)
        self._save_to_excel()

    def process_keyword(self, keyword):
        print("开始查找相关诗词: {}".format(keyword))
        self._handle_first_page(keyword)

        for i in range(self._total_page):
            page = i + 1
            if page == 1:
                continue

            self._handle_page(page, keyword)

        print("已查找完相关诗词: {}".format(keyword))

    def _handle_first_page(self, keyword):
        self._handle_page(1, keyword)
        self._total_page = self._page_data["sumPage"]

    def _handle_page(self, page, keyword):
        self._page_data = self._get_page_data(page, keyword)

        for record in self._page_data["gushiwens"]:
            name = record["nameStr"]
            if name in self._names:
                continue

            author2data = self._dynasty2data.setdefault(record["chaodai"], {})
            conts = author2data.setdefault(record["author"], [])
            conts.append({"name": name, "content": self._clear_content(record["cont"])})
            self._names.add(name)

    def _clear_content(self, content):
        replaces = [
            ("<br />", "\n"),
            ("<br/>", ""),
            ("<br>", "\n"),
            ("<p>", ""),
            ("</p>", ""),
            ("<div class='small'></div>", "\n"),
        ]
        for r in replaces:
            content = content.replace(*r)

        return content

    def _get_page_data(self, page, keyword):
        try:
            response = requests.get(self.URL_TEMP.format(page, keyword))
            response.raise_for_status()
        except Exception:
            raise Exception("Got exception when request url: {}".format(self.page_url))

        return response.json()

    def _save_to_excel(self):
        print("开始导出数据")
        sheet2headers = self._build_sheet2headers()
        sheet2lines = self._build_sheet2lines()

        Xlsx("build/古诗词.xlsx", sheet2headers, sheet2lines).make()
        print("成功导出数据")

    def _build_sheet2headers(self):
        return {s: ["作者", "诗名", "诗句"] for s in self._dynasty2data}

    def _build_sheet2lines(self):
        return {s: self._build_sheet_lines(s) for s in self._dynasty2data}

    def _build_sheet_lines(self, sheet):
        return [
            [author, cont["name"], cont["content"]]
            for author, conts in self._dynasty2data[sheet].items()
            for cont in conts
        ]
