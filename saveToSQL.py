import sqlite3
import settings

class sqliteSave:
    def __init__(self, table_name):
        self.name = settings.DBNAME
        self.table = table_name
        self.table_item = settings.TABLE[table_name]
    def insert(self, datas):
        insert_code = "INSERT INTO " + self.table + " (" + ",".join(self.table_item.keys()) + ") VALUES ("
        conn = sqlite3.connect(self.name)
        for data in datas:
            conn.execute(insert_code + "'" + "','".join(data.__dict__.values()) + "')")
        conn.commit()
        conn.close()
