import pymysql

def get_connection():
    try:
        connection = pymysql.connect(
            host='',
            user='',
            password='',
            database=''
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return None
