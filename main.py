import os
from dotenv import load_dotenv
from datalogger import DataLogger

# Last miljøvariabler fra .env-filen
load_dotenv()

if __name__ == "__main__":
    # Hent konfigurasjon fra miljøvariabler
    mqtt_broker = os.getenv("MQTT_BROKER", "mqtt-broker")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    device_id = os.getenv("DEVICE_ID", "datalogger-1")
    send_interval = int(os.getenv("SEND_INTERVAL", "5"))

    # Start dataloggeren
    datalogger = DataLogger(device_id, mqtt_broker, mqtt_port, send_interval)
    datalogger.start()