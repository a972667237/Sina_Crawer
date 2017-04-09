# encoding = utf-8
import requests
import cookies
import user_agent
import time
import random
from saveToSQL import sqliteSave
import urlparse
from models import WeiboData

class WeiboCrawer:
    def __init__(self):
        self.cookie = {}
        self.session = requests.session()
        self.indexPageUrl = 'https://m.weibo.cn/api/container/getIndex'
        self.agent = {
            'user_agent': random.choice(user_agent.agents)
        }
        self.updateCookies()
        self.hot = []
        self.weibo = []
        self._update_hot()
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
    def _parse_scheme(self, scheme):
        scheme_parse = urlparse.urlparse(scheme)
        return [i.split('=')[1] for i in scheme_parse.query.split('&')]
    def _index_params(self, scheme, since_id=0):
        containerid, extparam, luicode, lfid = self._parse_scheme(scheme)
        params = {}
        if not since_id:
            params = {
                'containerid': containerid,
                'extparam': extparam,
                'luicode': luicode,
                'lfid': lfid
            }
        else:
            params = {
                'containerid': containerid,
                'extparam': extparam,
                'luicode': luicode,
                'lfid': lfid,
                'since_id': since_id
            }
        return params
    def _update_hot(self):
        sql = sqliteSave('hot')
        self.hot = sql.get_from_hot()
    def _get_page_json(self, scheme, since_id):
        response = self._get(self.indexPageUrl, params = self._index_params(scheme, since_id))
        return response.json()
    def _save_info(self, hot, cards, since_id):
        group = []
        for i in cards:
            try:
                group = i['card_group']
            except:
                continue
            if len(group) > 5:
                break
        for i in group:
            try:
                attitude = str(i['mblog']['attitudes_count'])
                comment = str(i['mblog']['comments_count'])
                date = i['mblog']['created_at']
                repost = str(i['mblog']['reposts_count'])
                text = i['mblog']['text']
                scheme = str(i['scheme'])
                self.weibo.append(WeiboData(hot, attitude, comment, repost, date, text, scheme))
            except:
                print "save fail"
        print str(len(group)) + " infomation been save"
        if len(self.weibo) > 100:
            print "save infomation to sqlite3"
            sql = sqliteSave('weibo')
            sql.insert(self.weibo)
            self.weibo = []

    def start(self):
        for i in self.hot:
            since_id = 0
            page = 0
            while True:
                res_json = self._get_page_json(i.SCHEME, since_id)
                if res_json['ok'] is 0:
                    break
                self._save_info(i.TITLE, res_json['cards'], since_id)
                since_id = res_json['pageInfo']['since_id']
                page = page + 1
                print i.TITLE, page
                time.sleep(5)

a = WeiboCrawer()
a.start()
