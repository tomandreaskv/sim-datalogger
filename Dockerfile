# Bruk en lettvektig Python-bilde
FROM python:3.13

# Sett arbeidskatalogen i containeren
WORKDIR /app

# Kopier alle nødvendige filer til containeren
COPY src /app/src
COPY .env /app/
COPY requirements.txt /app/

# Installer avhengigheter
RUN pip install --no-cache-dir -r requirements.txt

# Kjør applikasjonen
CMD ["python", "/app/src/main.py"]
