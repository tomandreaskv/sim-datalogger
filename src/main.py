import os
from dotenv import load_dotenv
from datalogger import DataLogger
from pathlib import Path

# Finn den absolutte stien til root-mappen
BASE_DIR = Path(__file__).resolve().parent.parent  # Går opp fra 'src/' til root

# Last .env-filen eksplisitt fra root-mappen
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

if __name__ == "__main__":
    # Hent konfigurasjon fra miljøvariabler
    mqtt_broker = os.getenv("MQTT_BROKER", "mqtt-broker")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    device_id = os.getenv("DEVICE_ID", "datalogger-1")
    send_interval = int(os.getenv("SEND_INTERVAL", "5"))

    # Start dataloggeren
    datalogger = DataLogger(device_id, mqtt_broker, mqtt_port, send_interval)
    datalogger.start()