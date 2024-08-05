# SMA_auslesen(Sunnyboy 5.0)

## Grundidee:
Das folgende Python Skript liest die Leistungs und Verbrauchsdaten des Wechselrichters unserer PV-Anlage. Grundidee dieses Projektes war es, die Stromkosten unseres Elektroautos berechnen zu können. Hierfür muss man natürlich wissen wie hoch der Solarstromanteil bei der in das Auto eingespeisten Energie ist. Also wurde ein Strommesser (Shelly 3em) istalliert, um differenzieren zu können, wann genau das Auto lädt.

## Funktionsweise:
Das Skript besteht aus mehreren Funktionen und einer Hauptschleife, die die Aufgaben Datenerfassung,
Datenspeicherung, Fehlerbehandlung und Sitzungsmanagement behandeln. 

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








