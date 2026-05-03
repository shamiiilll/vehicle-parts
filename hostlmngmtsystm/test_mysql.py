import pymysql
try:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='')
    print("SUCCESS")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_db")
    print("DB_CREATED")
except Exception as e:
    print(f"FAILED: {e}")
