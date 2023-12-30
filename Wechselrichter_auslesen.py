import requests
import json 
import urllib3
import time
import mysql.connector
from mysql.connector import Error
from requests.auth import HTTPBasicAuth


# Warnungen für unsichere HTTPS-Anfragen deaktivieren
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def insert_data_into_Leistung(data):
    if data[2] == None: 
        data[2] = 0
    try:
        connection = mysql.connector.connect(
            host='localhost',        # z.B. 'localhost'
            database='PV',
            user='tom',
            password='Passwort_geheim') #hier Passwort für die Datenbank eingaben

        cursor = connection.cursor()
        query = "INSERT INTO Leistung (Zeit, aktuelle_Einspeisung,aktueller_Netzbezug,aktueller_Ertrag) VALUES (NOW(), %s ,%s ,%s)"
        record = (data[0],data[1],data[2])
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


def insert_data_into_Arbeit(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',        # z.B. 'localhost'
            database='PV',
            user='tom',
            password='Passwort_geheim') # hier Passwort der Datenbank eingeben

        cursor = connection.cursor()
        query = "INSERT INTO Arbeit (Zeit, Gesamtertrag,Tagesertrag,total_Netzbezug,total_Einspeisezaehler) VALUES (NOW(), %s ,%s ,%s,%s)"
        record = (data[0],data[1],data[2],data[3])
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


def insert_data_into_Shelly(Watt,Wattstunden):
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


def get_new_session_id():
    login_url = "https://192.168.0.46/dyn/login.json"
    login_headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    login_payload = {
        "right": "istl",
        "pass": "Passwort_geheim" # hier Passwort für die WebAPI des Wechselrichters eingeben 
    }
    login_response = requests.post(login_url, headers=login_headers, json=login_payload, verify=False)
    #print("Login Response JSON:", login_response.text)
    if login_response.status_code == 200:
        return login_response.json().get('result', {}).get('sid', None)
    else:
        print("Fehler beim Login")
    return None


def get_data(sid):
    url = f"https://192.168.0.46/dyn/getAllOnlValues.json?sid={sid}"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    cookies = {
        "tmhDynamicLocale.locale": "\"en-us\"",
        "deviceMode443": "\"PSK\"",
        "deviceUsr443": "\"istl\"",
        "user443": r"%7B%22role%22%3A%7B%22bitMask%22%3A4%2C%22title%22%3A%22istl%22%2C%22loginLevel%22%3A2%7D%2C%22username%22%3A862%2C%22sid%22%3A%22" + str(sid) + r"%22%7D",
        "deviceSid443": f"\"{sid}\""
    }
    data = '{"destDev":[]}'
    response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    return response


# Passwörter und Benutzernamen auslesen
passdateipfad = "../pass.json"

# Öffnen und Lesen der JSON-Datei
with open(passdateipfad, 'r') as f:
    passdata = json.load(f)

# Initialer random SID-Wert 
sid = "hJ5UYSgefNxexRwP"
counter = 0

# laden des letzten Wattstundenwertes aus der Datenbank
Wattstunden = float(read_database("SELECT Wattstunden FROM Shelly ORDER BY Zeit DESC LIMIT 1")[0][0])

while True:
    start_time = time.time() # startzeit messen
    for _ in range(2):  # Maximal 2 Versuche
        response = get_data(sid)
        json_out = response.text
        try:
            data = json.loads(json_out)
            if "err" in data:
                error_code = data["err"]
                if error_code == 401: # session id falsch unauthorized
                    print("Unauthorized access. Please check your credentials.")
                    sid = get_new_session_id()
                elif error_code == 503: # maximale session ids
                    print("No more sessions available")
                    break
            else:
                print("Auth true")
                break

        except json.JSONDecodeError:
            print("Fehler beim Parsen der JSON-Antwort")
            break
    
    aktuelle_Einspeisung = data["result"]["0199-xxxxxA83"]["6100_40463600"]["1"][0]["val"]
    aktueller_Netzbezug = data["result"]["0199-xxxxxA83"]["6100_40463700"]["1"][0]["val"]
    aktueller_Ertrag = data["result"]["0199-xxxxxA83"]["6100_40263F00"]["1"][0]["val"]
    Gesamtertrag = data["result"]["0199-xxxxxA83"]["6400_00260100"]["1"][0]["val"]
    Tagesertrag = data["result"]["0199-xxxxxA83"]["6400_00262200"]["1"][0]["val"]
    total_Netzbezug = data["result"]["0199-xxxxxA83"]["6400_00469200"]["1"][0]["val"]
    total_Einspeisezaehler = data["result"]["0199-xxxxxA83"]["6400_00469100"]["1"][0]["val"]

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



    # Leistungsdaten alle 5 sek in Leistungstable speichern
    insert_data_into_Leistung([aktuelle_Einspeisung,aktueller_Netzbezug,aktueller_Ertrag])

    counter += 1 # Arbeitsdaten einmal pro stunde in ArbeitsTable speichern
    if counter == 720: # 720 = 60 min * 60 sek / 5 sek
        insert_data_into_Arbeit([Gesamtertrag, Tagesertrag, total_Netzbezug, total_Einspeisezaehler])
        counter = 0

    end_time = time.time() #Endzeit speichern
    execution_time = end_time - start_time  # Ausführungszeit berechnen
    time_to_sleep = max(5 - execution_time, 0)  # Berechnen, wie lange noch gewartet werden muss
    time.sleep(time_to_sleep) # Wartezeit time.sleep(5) war nicht genau genug 




