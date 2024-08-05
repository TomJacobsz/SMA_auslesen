# Wechselrichter_auslesen (SMA Sunnyboy 5.0)

## Grundidee:
Das folgende Python Skript liest die Leistungs und Verbrauchsdaten des Wechselrichters unserer PV-Anlage. Grundidee dieses Projektes war es, die Stromkosten unseres Elektroautos berechnen zu können. Hierfür muss man natürlich wissen wie hoch der Solarstromanteil bei der in das Auto eingespeisten Energie ist. Also wurde ein Strommesser (Shelly 3em) istalliert, um differenzieren zu können, wann genau das Auto lädt.

## Funktionsweise:
Das Skript besteht aus mehreren Funktionen und einer Hauptschleife, die die Aufgaben Datenerfassung,
Datenspeicherung, Fehlerbehandlung und Sitzungsmanagement behandeln. Das Skript läuft auf einem Server, der sich im Heimnetzwerk befindet. 

### Funktionen:
- **insert_data_into_Leistung_database(time, data):** Fügt Leistungsdaten in die Datenbank ein.
- **insert_data_into_Arbeit_database(time, data):** Fügt Arbeitsdaten in die Datenbank ein.
- **insert_data_into_Shelly_database(time, Watt, Wattstunden):** Fügt Shelly-Daten in die Datenbank ein.
- **read_database(query):** Liest Daten aus der Datenbank.
- **get_new_session_id():** Holt eine neue Sitzungs-ID vom Wechselrichter.
- **get_data(sid):** Holt Daten vom Wechselrichter unter Verwendung der Sitzungs-ID.

### Hauptschleife:
1. Erfasst die aktuelle Zeit.
2. Fragt Daten vom Wechselrichter ab und behandelt mögliche Fehler (Timeout, Verbindungsfehler, ungültige Sitzungs-ID).
3. Fragt Daten von der Shelly-API ab.
4. Berechnet die Wattstunden und speichert die Daten in der Datenbank.
5. Speichert Leistungsdaten alle 10 Sekunden und Arbeitsdaten einmal pro Stunde.
6. Berechnet die Ausführungszeit und wartet entsprechend, um den nächsten Datenerfassungszyklus zu starten.

### Fehlerbehandlung:
Das Skript verwendet ein Logging-System, um die Fehlersuche erheblich zu vereinfachen. Die Logs werden in der Datei (logfile.log) gespeichert und enthalten Informationen über aufgetretene Fehler.

## Ergebnis:
![image](https://github.com/user-attachments/assets/0c843615-8c3d-430a-ac9c-f1a37124a82e)
### Graphen Beschreibung:
(Auflistung von oben nach unten betrachtet)
1. Der Orangene Plot zeigt den kompletten Netzbezug des Hauses, also inklusive Ladezüglen der Autos. Der Blaue zeigt den reinen Hausverbrauch, da hier die Datenpunkte des Shelly Messgerätes abgezogen werden. Zu beachten ist hierbei, dass der Haushalt zusätzlich über ein Hybridfahrzeug verfügt, dessen Ladezüglen noch nicht erfasst werden. Dies ist um den Zeitpunkt 2024-05-04 gut zu erkennen, da der blaue und orangene Graph komplett übereinstimmen.
2. Dieser Plot beschreibt den absoluten Ertrag (grün) und das, was nach Abzug des Hausverbrauches(inklusive Hybridfahrzeug) zur Verfügung steht (braun). Also der Überschuss, der im Normalfall in das Netz eingespeist wird.
3. Hier werden die Ladezüglen des Elektroautos dargestellt. Genauer, das, was vom Netz bezogen werden muss um das Auto zu laden. Also Ladelast - ((Absoluter Ertrag) - Hausverbrauch). Gut zu erkennen ist, dass sich der zu Verfügung stehende Ertrag der Solaranlage aus (2.) und dieser Plot ergänzen, da natürlich bei mehr zur Verfügung stehendem Ertrag weniger aus dem Netz bezogen werden muss.

Der Solarstromanteil des Verbrauchs des Elektroautos in diesem Zeitraum beläuft sich auf ~36%. Die Berechnung erfolgt druch:
- **Netzbezug_Wh** = Datenpunkte(Netzbezug durch Auto).sum() / 360
- **Gesamtlast_Wh** = Datenpunkte(Gesamtlast durch das Auto).sum() / 360
- **Anteil Solarstrom** = (Gesamtlast_Wh - Netzbezug_Wh) / Gesamtlast_Wh * 100
  

 durch 360, da alle 10 sek ein Datenpunkt in Watt erzeugt wird also erhalten wir durch diese Rechnung die     Wh dieses Zeitraumes








