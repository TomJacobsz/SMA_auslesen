from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

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

def pretty_print(last_day : list)->list:
    pretty_return = []
    pretty_return.append("{:<30}{:<10}{:<10}{:<10}".format("Zeit","Leistung","Netzbezug","Ertrag"))
    for entry in last_day:
        datetime_obj, value1, value2, value3 = entry
        formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        formatted_entry = "{:<30}{:<10}{:<10}{:<10}".format(formatted_datetime, value1, value2, value3)
        pretty_return.append(formatted_entry)
    return pretty_return


@app.route('/PV/Leistung/last_2_minutes', methods=['GET'])
def get_leistung():
    last_2_minutes = read_database("SELECT * FROM Leistung where Zeit > DATE_SUB(NOW(), INTERVAL 2 MINUTE)")
    return jsonify(last_2_minutes)

@app.route('/PV/Leistung/last_day', methods=['GET'])
def get_last_day():
    last_day = read_database("SELECT * FROM Leistung where Zeit > DATE_SUB(NOW(), INTERVAL 1 DAY)")
    return jsonify(pretty_print(last_day))

if __name__ == '__main__':
    app.run(debug=True)