# libraries imports
import pymysql

# local files imports
import config


try:
    conn = pymysql.connect(
        host = config.host,
        port = config.port,
        user = config.user,
        password = config.password,
        database = config.database,
        cursorclass = pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchall()
    print(output)
    print("Connected successfully! ")
    conn.close()
except Exception:
    print("Connection failure ... ")