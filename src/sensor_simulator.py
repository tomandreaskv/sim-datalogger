import random
import time
import math

class SensorSimulator:
    def __init__(self, error_rate=0.05, environment="outdoor"):
        """ 
        Simulerer sensorverdier, med støtte for innendørs/utendørs miljø. 
        environment: "outdoor" (ute) eller "indoor" (inne).
        """
        self.error_rate = error_rate
        self.environment = environment
        self.start_time = time.time()  # Brukes til naturlige svingninger

        self.sensor_values = {
            "temperature": random.uniform(-10.0, 25.0),
            "humidity": random.uniform(30.0, 50.0),
            "pressure": random.uniform(900, 1100),
            "ph": random.uniform(5.5, 7.5),
            "soil_moisture": random.uniform(20, 80),
            "light": random.uniform(10, 500),  # Justert startverdi
        }

        self.sensor_limits = {
            "temperature": {"unit": "C", "min": -10.0, "max": 40.0, "change": 0.5 if self.environment == "outdoor" else 0.2},
            "humidity": {"unit": "%", "min": 20.0, "max": 100.0, "change": 2.0 if self.environment == "outdoor" else 1.0},
            "pressure": {"unit": "hPa", "min": 900, "max": 1100, "change": 1.0 if self.environment == "outdoor" else 0.1},
            "ph": {"unit": "pH", "min": 5.0, "max": 8.0, "change": 0.05},
            "soil_moisture": {"unit": "%", "min": 10, "max": 90, "change": 3.0 if self.environment == "outdoor" else 1.5},
            "light": {"unit": "lux", "min": 0, "max": 5000 if self.environment == "outdoor" else 1000, "change": 50.0},
        }

    def is_daytime(self):
        """ Bestemmer om det er dag eller natt basert på klokkeslett (lokal tid). """
        current_hour = time.localtime().tm_hour
        return 6 <= current_hour <= 18  # Dag mellom 06:00 og 18:00

    def introduce_error(self, sensor, value):
        """ Introducerer tilfeldig sensorfeil basert på sannsynlighet. """
        if random.random() < self.error_rate:
            error_type = random.choice(["over_limit", "under_limit", "frozen", "spike"])
            if error_type == "over_limit":
                return value + random.uniform(100, 500)  # Større variasjon for lys
            elif error_type == "under_limit":
                return value - random.uniform(100, 500)
            elif error_type == "frozen":
                return self.sensor_values[sensor]
            elif error_type == "spike":
                return value * random.uniform(2, 5)
        
        return value

    def generate_sensor_data(self):
        """ Genererer og oppdaterer sensorverdier med mer naturlige variasjoner."""
        
        elapsed_time = time.time() - self.start_time
        is_day = self.is_daytime()

        for sensor, params in self.sensor_limits.items():
            change = random.uniform(-params["change"], params["change"])
            self.sensor_values[sensor] += change

            # 🌞 Simuler dag/natt-lysverdier med realistiske verdier
            if sensor == "light":
                if self.environment == "outdoor":
                    if is_day:
                        target_light = random.uniform(1000, 5000)  # Dagtid
                    else:
                        target_light = random.uniform(1, 50)  # Natt
                else:  # Innendørs
                    if is_day:
                        target_light = random.uniform(100, 500)  # Kunstig lys
                    else:
                        target_light = random.uniform(5, 50)  # Svakt nattlys
                self.sensor_values[sensor] += (target_light - self.sensor_values[sensor]) * 0.1

            # 🌡️ Temperatur: Utendørs svinger mer enn innendørs
            elif sensor == "temperature":
                base_temp = 22 if is_day else 15 if self.environment == "outdoor" else 21
                temp_variation = 8 if self.environment == "outdoor" else 2
                self.sensor_values[sensor] = base_temp + temp_variation * math.sin(elapsed_time / 3600)

            # 💦 Luftfuktighet: Varierer mer ute
            elif sensor == "humidity":
                base_humidity = 40 if is_day else 60 if self.environment == "outdoor" else 45
                humidity_variation = 20 if self.environment == "outdoor" else 5
                self.sensor_values[sensor] = base_humidity + humidity_variation * math.sin(elapsed_time / 4500)

            # 🌱 Jordfuktighet: Utendørs faller den raskere
            elif sensor == "soil_moisture":
                if random.random() < (0.02 if self.environment == "outdoor" else 0.005):
                    self.sensor_values[sensor] = random.uniform(70, 90)
                else:
                    self.sensor_values[sensor] -= 0.3 if self.environment == "outdoor" else 0.1
                if self.sensor_values[sensor] < params["min"]:
                    self.sensor_values[sensor] = params["min"]

            # 🧪 pH-verdi: Påvirkes mer utendørs (regn, jord)
            elif sensor == "ph":
                ph_variation = 0.05 if self.environment == "outdoor" else 0.02
                self.sensor_values[sensor] += random.uniform(-ph_variation, ph_variation)

            # 🌫️ Trykk: Endrer seg sakte ute, men er stabil inne
            elif sensor == "pressure":
                self.sensor_values[sensor] += random.uniform(-1.0, 1.0) if self.environment == "outdoor" else 0.0

            # Begrens verdiene innenfor min/max
            self.sensor_values[sensor] = max(params["min"], min(params["max"], self.sensor_values[sensor]))

            # Mulighet for å introdusere feil
            self.sensor_values[sensor] = self.introduce_error(sensor, self.sensor_values[sensor])

        return {
            sensor: {"value": round(value, 2), "unit": self.sensor_limits[sensor]["unit"]}
            for sensor, value in self.sensor_values.items()
        }
