#!/bin/sh

# Broker MQTT (remplacez l'adresse IP et le port par ceux de votre broker)
BROKER="127.0.0.1"
PORT="1883"

# Sujet MQTT auquel le client doit souscrire pour recevoir les messages
TOPIC="application/#"

# Chemin du fichier de sortie pour stocker la payload des messages
OUTPUT_FILE="/mnt/mmcblk0p1/ifremer/last_data.txt"

# Souscription aux messages MQTT et stockage de la payload dans le fichier
mosquitto_sub -h "$BROKER" -p "$PORT" -t "$TOPIC" | while IFS= read -r payload; do
    echo "$payload" >> "$OUTPUT_FILE"
done