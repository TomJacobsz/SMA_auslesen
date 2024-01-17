import time
import logging

# Erstellen Sie einen Logger und setzen Sie das Log-Level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Erstellen Sie einen FileHandler und setzen Sie das Log-Level
handler = logging.FileHandler('/home/tom/SMA_Projekt/SMA_auslesen/logfile.log')
handler.setLevel(logging.INFO)

# Erstellen Sie einen Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Fügen Sie den Formatter zum Handler hinzu
handler.setFormatter(formatter)

# Fügen Sie den Handler zum Logger hinzu
logger.addHandler(handler)

logger.info("Starte programm")


while True:
    time.sleep(3)
    logger.info('Dies ist eine Info-Nachricht')
    time.sleep(3)
    logger.error('Dies ist eine Fehlermeldung')