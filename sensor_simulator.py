import random
import time

class SensorSimulator:
    def __init__(self, error_rate=0.05):
        """ 
        Definerer sensorene og startverdier for simulering. 
        error_rate: Sannsynlighet (0-1) for at en sensorfeil skal oppstå. 
        """
        self.error_rate = error_rate  # 5% sjanse for feil
        self.sensor_values = {
            "temperature": random.uniform(20.0, 25.0),
            "humidity": random.uniform(30.0, 50.0),
            "pressure": random.uniform(900, 1100),
            "ph": random.uniform(5.5, 7.5),
            "soil_moisture": random.uniform(20, 80),
            "light": random.uniform(100, 1000),
        }

        self.sensor_limits = {
            "temperature": {"unit": "C", "min": 20.0, "max": 30.0, "change": 0.2},
            "humidity": {"unit": "%", "min": 30.0, "max": 70.0, "change": 1.0},
            "pressure": {"unit": "hPa", "min": 900, "max": 1100, "change": 2.0},
            "ph": {"unit": "pH", "min": 5.5, "max": 7.5, "change": 0.05},
            "soil_moisture": {"unit": "%", "min": 20, "max": 80, "change": 2.0},
            "light": {"unit": "lux", "min": 0, "max": 1000, "change": 10.0},
        }

    def is_daytime(self):
        """ Bestemmer om det er dag eller natt basert på klokkeslett (lokal tid). """
        current_hour = time.localtime().tm_hour
        return 6 <= current_hour <= 18  # Dag mellom 06:00 og 18:00

    def introduce_error(self, sensor, value):
        """ Introducerer tilfeldig sensorfeil basert på sannsynlighet. """
        if random.random() < self.error_rate:  # F.eks. 5% sjanse for feil
            error_type = random.choice(["over_limit", "under_limit", "frozen", "spike"])
            if error_type == "over_limit":
                return value + random.uniform(10, 50)  # Skyver verdien over maksgrensen
            elif error_type == "under_limit":
                return value - random.uniform(10, 50)  # Skyver verdien under mingrensen
            elif error_type == "frozen":
                return self.sensor_values[sensor]  # Fryser verdien (ingen endring)
            elif error_type == "spike":
                return value * random.uniform(2, 5)  # Plutselig hopp (dobling/flere ganger høyere)
        
        return value  # Ingen feil

    def generate_sensor_data(self):
        """ Genererer og oppdaterer sensorverdier med en liten tilfeldig variasjon. """
        
        is_day = self.is_daytime()

        for sensor, params in self.sensor_limits.items():
            change = random.uniform(-params["change"], params["change"])
            self.sensor_values[sensor] += change

            # Simuler dag/natt-lysverdier
            if sensor == "light":
                target_light = random.uniform(500, 1000) if is_day else random.uniform(10, 50)
                self.sensor_values[sensor] += (target_light - self.sensor_values[sensor]) * 0.1  # Smooth overgang


            # Begrens verdiene innenfor min/max
            self.sensor_values[sensor] = max(params["min"], min(params["max"], self.sensor_values[sensor]))

            # Mulighet for å introdusere feil
            self.sensor_values[sensor] = self.introduce_error(sensor, self.sensor_values[sensor])

        return {
            sensor: {"value": round(value, 2), "unit": self.sensor_limits[sensor]["unit"]}
            for sensor, value in self.sensor_values.items()
        }