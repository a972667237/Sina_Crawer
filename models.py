class HotData:
    def __init__(self, title, description, discuss, scheme):
        self.TITLE = title
        self.DESCRIPTION = description
        self.DISCUSS = discuss
        self.SCHEME = scheme
    def __str__(self):
        return self.title

class WeiboData:
    def __init__(self, hot, attitude, comment, repost, date, text, scheme):
        self.HOT = hot
        self.ATTITUDE = attitude
        self.COMMENT = comment
        self.REPOST = repost
        self.DATE = date
        self.TEXT = text
        self.SCHEME = scheme
