import mysql.connector
from mysql.connector import Error

params = {
    'host': 'dbtommi',
    'database': 'PV',
    'user': 'tom',
    'password': 'dexterfee123'
}

def read_database(query : str)->list:
    try:
        connection = mysql.connector.connect(host = params['host'],user = params['user'],password =  params['password'],database =  params['database'])
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Error as e:
        print("Error while connecting to MariaDB", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection is closed")

def pretty_print(last_day):
    print("{:<30}{:<10}{:<10}{:<10}".format("Zeit","Leistung","Netzbezug","Ertrag"))
    for entry in last_day:
        datetime_obj, value1, value2, value3 = entry
        formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        formatted_entry = "{:<30}{:<10}{:<10}{:<10}".format(formatted_datetime, value1, value2, value3)
        print(formatted_entry)

#last_day = read_database("SELECT * FROM Leistung where Zeit > DATE_SUB(NOW(), INTERVAL 10 MINUTE)")
last_20_seconds = read_database("SELECT * FROM Leistung where Zeit > DATE_SUB(NOW(), INTERVAL 5 MINUTE)")
pretty_print(last_20_seconds)