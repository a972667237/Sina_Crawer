#coding=utf-8
import sqlite3
import settings
from models import HotData

class sqliteSave:
    def __init__(self, table_name):
        self.name = settings.DBNAME
        self.table = table_name
        self.table_item = settings.TABLE[table_name]
    def insert(self, datas):
        insert_code = "INSERT INTO " + self.table + " (" + ",".join(self.table_item.keys()) + ") VALUES ("
        conn = sqlite3.connect(self.name)
        for data in datas:
            code = insert_code + "'" + "','".join([value.replace("'", '"') for value in data.__dict__.values()]) + "')"
            print code
            conn.execute(code)
        conn.commit()
        conn.close()
    def get_from_hot(self):
        conn = sqlite3.connect(self.name)
        results = conn.execute("SELECT * FROM hot")
        result_list = []
        while True:
            try:
                res = results.next()
            except:
                break
            i, title, description, discuss, scheme = res
            result_list.append(HotData(title, description, discuss, scheme))
        conn.close()
        return result_list
