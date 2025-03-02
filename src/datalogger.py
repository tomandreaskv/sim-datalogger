import paho.mqtt.client as mqtt
import json
import time
from sensor_simulator import SensorSimulator

class DataLogger:
    def __init__(self, device_id, mqtt_broker, mqtt_port=1883, send_interval=5, error_rate=0.05):
        self.device_id = device_id
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.send_interval = send_interval
        self.sensor_simulator = SensorSimulator(error_rate=error_rate)

        self.mqtt_topic = f"sensors/{self.device_id}"
        self.mqtt_config_topic = f"config/{self.device_id}"

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """ Kobler til MQTT og lytter etter konfigurasjonsmeldinger. """
        print(f"[{self.device_id}] Connected to MQTT Broker: {rc}")
        client.subscribe(self.mqtt_config_topic)

    def on_message(self, client, userdata, msg):
        """ Håndterer innkommende MQTT-meldinger (f.eks. oppdatering av config). """
        payload = json.loads(msg.payload)
        print(f"[{self.device_id}] Received config update: {payload}")

    def start(self):
        """ Starter MQTT-kommunikasjonen og publiserer sensordata i en løkke. """
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()

        try:
            while True:
                data = {
                    "device_id": self.device_id,
                    "timestamp": int(time.time()),
                    "sensors": self.sensor_simulator.generate_sensor_data()
                }
                payload = json.dumps(data)
                self.client.publish(self.mqtt_topic, payload)
                print(f"[{self.device_id}] Published: {payload}\n")
                time.sleep(self.send_interval)
        except KeyboardInterrupt:
            print(f"[{self.device_id}] Stopping simulation...")
        finally:
            self.client.loop_stop()
            self.client.disconnect()