import json
import requests
from requests.auth import HTTPBasicAuth
import mysql.connector
from mysql.connector import Error
import time
# Pfad der pass datei eins über skriptordner
passdateipfad = "../pass.json"

# Öffnen und Lesen der JSON-Datei
with open(passdateipfad, 'r') as f:
    passdata = json.load(f)

def read_database(query : str)->list:
    try:
        connection = mysql.connector.connect(host="dbtommi", user=passdata["Datenbank"]["user"], password=passdata["Datenbank"]["password"], database="PV")
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

def insert_data_into_Shelly(Watt,Wattstunden : float):
    try:
        connection = mysql.connector.connect(
            host='dbtommi',        # z.B. 'localhost'
            database='PV',
            user='tom',
            password=passdata["Datenbank"]["password"]) # hier Passwort der Datenbank eingeben

        cursor = connection.cursor()
        query = "INSERT INTO Shelly (Zeit, Watt,Wattstunden) VALUES (NOW(), %s ,%s)"
        record = (Watt,Wattstunden)
        cursor.execute(query, record)
        connection.commit()
        print("Data successfully inserted")

    except Error as e:
        print("Error while connecting to MariaDB", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection is closed")

Wattstunden = float(read_database("SELECT Wattstunden FROM Shelly ORDER BY Zeit DESC LIMIT 1")[0][0])
while True:
    start_time = time.time()

    # Shelly API abfragen:
    username = passdata["Shelly"]["user"]
    password = passdata["Shelly"]["password"]
    url = 'http://192.168.0.49/status'
    response = requests.get(url, auth=HTTPBasicAuth(username,password)).json()

    Watt = response["total_power"]
    print(Watt)
    Wattstunden = Wattstunden + Watt/360

    insert_data_into_Shelly(Watt,Wattstunden)
    print("Watt: " + str(Watt) + "W")
    print("Wattstunden: " + str(Wattstunden) + "Wh")

    end_time = time.time()
    time.sleep(max(10-(end_time-start_time),0))


