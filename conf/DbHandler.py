import traceback

# import pyodbc
from conf.sql.DbQueryString import getTables,getColunmsByTable, getTableIndexes

class Dbhandler():

    DB = None
    dbCursor = None
    dbUser = None
    dbPwd = None
    dbUrl = None
    dbDsn = None

    def __init__(self, dbInfo):
        self.dbUser = dbInfo.get('DB_USER')
        self.dbPwd = dbInfo.get('DB_PWD')
        self.dbUrl = dbInfo.get('DB_URL')
        self.dbDsn = dbInfo.get('DB_DSN')
        connection_string = f"DSN={self.dbDsn};UID={self.dbUser};PWD={self.dbPwd};DATABASE={self.dbUrl}"
        # self.DB = pyodbc.connect(connection_string)
        self.dbCursor = self.DB.cursor()


    def getTables(self):
        print('getTables')
        tables = []
        try:
            query = getTables(self.dbUser)
            tables = self.selectQuery(query)
            for i, item in enumerate(tables):
                item['COL_INFO'] = self.selectQuery(getColunmsByTable(item['TABLE_NAME'], self.dbUser))
                item['TABLE_INDEX'] = self.selectQuery(getTableIndexes(item['TABLE_NAME'], self.dbUser))
        except:
            traceback.print_exc()
        return tables



    def selectQuery(self, queryString):
        self.dbCursor.execute(queryString)
        rows = self.dbCursor.fetchall()
        # 열 이름 가져오기
        column_names = [description[0] for description in self.dbCursor.description]
        # 데이터를 JSON 형식으로 변환
        json_data = []
        for row in rows:
            json_data.append(dict(zip(column_names, row)))
        return json_data