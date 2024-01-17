sleep 20  # Warten Sie 20 Sekunden, um sicherzustellen, dass MariaDB bereit ist

source /pfad/zum/env/bin/activate #pip env activieren

python3 /pfad/zur/pythondatei/Wechselrichter_auslesen.py >> /pfad/zur/pythondatei/Wechselrichter_auslesen.log 2>&1 #Logdatei für Autostart schreiben.


# -> alternativ würde der Befehl /pfad/zum/env/python3 pfad/zur/pythondatei/Wechselrichter_auslesen.py auch funktionieren (denk ich)
