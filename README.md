# Sim-Datalogger: IoT Sensor Simulering med MQTT og Docker

Dette prosjektet simulerer flere IoT-enheter som publiserer sensordata til en MQTT-broker. Ved hjelp av Docker Compose kan vi kjøre en MQTT-broker (Eclipse Mosquitto) og flere datalogger-instanser samtidig for å skape et realistisk testmiljø.

## 📁 Prosjektstruktur

```
/sim-datalogger
│── src/
│   ├── main.py
│   ├── datalogger.py
│   ├── sensor_simulator.py
│── .env
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── mosquitto.conf  <-- MQTT konfigurasjonsfil
```


## 🚀 Kom i gang

### 1️⃣ Installer Docker og Docker Compose

- Last ned og installer Docker Desktop.

- Kontroller installasjonen:

    ```
    docker --version
    docker-compose --version
    ```

### 2️⃣ Sett opp MQTT Broker-konfigurasjonen

- Sørg for at mosquitto.conf ligger i rotmappen og inneholder:
    ```
    listener 1883
    allow_anonymous true
    ```

## 🏗️ Bygg og start tjenestene

Start hele systemet:
```
docker-compose up --build
```

Start i bakgrunnen:
```
docker-compose up --build -d
```

Stopp tjenestene:
```
docker-compose down
```

## 🔍 Testing og debugging

### 1️⃣ Sjekk om MQTT Broker kjører
```
docker ps
```
Du bør se mqtt-broker i listen over kjørende containere.

### 2️⃣ Abonner på MQTT-meldinger

Kjør følgende kommando for å se sanntidsmeldinger fra IoT-enhetene:
```
mosquitto_sub -h localhost -t "sensors/#" -v
```

Dette vil vise all data publisert av simulerte dataloggere.

### 3️⃣ Skaler opp antall IoT-enheter

Hvis du vil simulere flere IoT-enheter:
```
docker-compose up --scale datalogger=10
```

Dette starter 10 datalogger-instanser som sender sensordata samtidig.

## 🔧 Feilsøking

Feil: "ConnectionRefusedError: [WinError 10061]"

🔹 Løsning: MQTT-broker kjører sannsynligvis ikke. Sjekk status med:
```
docker logs mqtt-broker
```
Hvis den ikke kjører, prøv å starte den manuelt:
```
docker-compose restart mqtt-broker
```
Feil: Ingen data mottas på MQTT

🔹 Løsning: Kontroller at dataloggerne er tilkoblet riktig broker:
```
docker logs datalogger1
```
Sjekk at MQTT_BROKER er riktig satt (f.eks. mqtt-broker).

## 📌 Oppsummering

✅ MQTT-broker og flere IoT-enheter kjøres i containere.✅ Sensordata publiseres via MQTT og kan observeres i sanntid.✅ Lett å skalere opp for mer realistisk testing.

💡 Utvidelse: Kan kobles til en database eller et dashbord for å visualisere data!

🔗 Bidrag: Pull requests og forslag er velkomne! 🚀