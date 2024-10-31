#!/bin/bash

# Avvia il server Flask
flask run --host=0.0.0.0 --port=5001 --debug &

# Avvia il server contenente algoritmo di ML
python3 ./main/ServerMQTT.py

