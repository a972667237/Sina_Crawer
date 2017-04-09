# encoding=utf-8
import requests
import cookies
import user_agent
import time
import json
import random
from saveToSQL import sqliteSave
from models import HotData


class HotCrawer:
    def __init__(self):
        self.cookie = {}
        self.session = requests.session()
        self.hotDomainUrl = "https://m.weibo.cn/p/100803"
        self.indexPageUrl = "https://m.weibo.cn/api/container/getIndex"
        self.agent = {
            'user_agent': random.choice(user_agent.agents)
        }
        self.updateCookies()
        self.hot = []
    def updateCookies(self):
        try:
            self.cookie = cookies.get()[0]
        except:
            print "GET COOKIES FAILED"
            self.cookie = {}
            time.sleep(100)
            updateCookies()
    def _get(self, url, params = {}):
        if not params:
            response = self.session.get(url, cookies = self.cookie, headers = self.agent)
        else:
            response = self.session.get(url, cookies = self.cookie, params = params, headers = self.agent)
        return response
    def _index_params(self, page = 1):
        if page is 1:
            params = {
                'containerid': 100803
            }
        else:
            params = {
                'containerid': 100803,
                'page': page
            }
        return params
    def _get_page_json(self, page):
        response = self._get(self.indexPageUrl, params = self._index_params(page))
        return response.json()
    def _save_info(self, res, page):
        print "now save page" + str(page)
        group = []
        if page is 1:
            hot_group = res['cards'][1]['card_group']
            normal_group = res['cards'][10]['card_group']
            group = hot_group + normal_group
        else:
            group = res['cards'][0]['card_group']
        # finish get group
        for item in group:
            self.hot.append(HotData(item['card_type_name'], item['desc1'], item['desc2'], item['scheme']))
    def start(self):
        page = 1
        while True:
            res_json = self._get_page_json(page)
            if res_json['ok'] is 0:
                break
            self._save_info(res_json, page)
            page = page + 1
            time.sleep(10)
        sql = sqliteSave('hot')
        sql.insert(self.hot)

if __name__ == "__main__":
    a = HotCrawer()
    a.start()
