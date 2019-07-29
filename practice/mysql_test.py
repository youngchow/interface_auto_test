import pymysql


class Tmysql:
    def __init__(self):
        self.conn = pymysql.connect(
            host = 'test.lemonban.com',
            port = 3306,
            user = 'test',
            db = 'future',
            password = 'test',
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def run_sql(self,sql,args = None,is_more = False):
        self.cursor.execute(sql,args)
        self.conn.commit()

        if is_more:
            result1 = self.cursor.fetchone()
            return  result1
        else:
            result2 = self.cursor.fetchall()
            return result2
    def close(self):
        self.cursor.close()
        self.conn.close()


