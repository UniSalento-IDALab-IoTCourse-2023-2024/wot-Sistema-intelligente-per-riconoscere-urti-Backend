import joblib
import paho.mqtt.client as mqtt
import numpy as np
import re
import pandas as pd
import requests as requests

# Impostazioni MQTT
BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883
TOPICS = [("iot/accelerometer", 0), ("iot/gyroscope", 0)]

# Carica il modello pre-addestrato
with open('model.joblib', 'rb') as model_file:
    model = joblib.load(model_file)

# Variabili globali per memorizzare i dati dei sensori
accel_data = None
gyro_data = None

# Variabile globale per contare gli eventi
event_count = 0

# Variabile globale per memorizzare l'user_id
user_id = None

# Preprocessa il payload del messaggio in arrivo
def preprocess_payload(payload):
    try:
        # Sostituisci le virgole con i punti decimali
        payload = payload.replace(',', '.')

        # Estrai l'user_id dal payload
        user_id_match = re.search(r"user_id:\s*(\w+)", payload)
        if user_id_match:
            global user_id
            user_id = user_id_match.group(1)

        # Estrae i numeri dal payload utilizzando una regex
        data = re.findall(r"[-+]?\d*\.\d+(?:[eE][-+]?\d+)?", payload)
        # Converte i valori in float, gestendo la notazione scientifica
        data = np.array([float(x) for x in data])
        return data
    except Exception as e:
        print(f"Errore durante l'elaborazione del payload: {e}")
        return None


# Funzione per tentare la previsione se sono disponibili entrambi i dataset
def try_predict():
    global accel_data, gyro_data, event_count, user_id

    if accel_data is not None and gyro_data is not None:
        # Controlla che i dati abbiano la dimensione corretta
        if len(accel_data) == 3 and len(gyro_data) == 3:
            # Combina i dati dei due sensori
            combined_data = np.concatenate((accel_data, gyro_data)).reshape(1, -1)

            # Stampa i dati combinati con formattazione decimale
            formatted_data = ["{:.4f}".format(x) for x in combined_data[0]]
            # print(f"Dati combinati: {formatted_data}")

            # Predice l'evento
            try:
                # Supponendo che questi siano i nomi delle caratteristiche usati durante il training
                feature_names = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]

                # Converti l'array numpy in un DataFrame
                combined_data_df = pd.DataFrame(combined_data, columns=feature_names)

                # Fai la previsione usando il DataFrame
                prediction = model.predict(combined_data_df)

                # Incrementa il contatore degli eventi
                event_count += 1

                if prediction[0] != "altro":
                    print(f"Evento {event_count}: {prediction[0]} | User ID: {user_id}")

                if prediction[0] == "incidenti":
                    url = "http://127.0.0.1:5001/add_incidenti"
                    headers = {"Content-Type": "application/json"}
                    data = {"cliente_incidentato": user_id}
                    response = requests.post(url=url, headers=headers, json=data)
                    print(f"Valori Accelerometro: {accel_data}")
                    print(f"Valori Giroscopio: {gyro_data}")
                    if response.status_code == 200:
                        print("Incidente salvato con successo")
                    else:
                        print("Incidente non salvato")

                if prediction[0] == "frenate":
                    url = "http://127.0.0.1:5001/add_frenate"
                    headers = {"Content-Type": "application/json"}
                    data = {"cliente": user_id}
                    response = requests.post(url=url, headers=headers, json=data)
                    print(f"Valori Accelerometro: {accel_data}")
                    print(f"Valori Giroscopio: {gyro_data}")
                    if response.status_code == 200:
                        print("Frenata salvata con successo")
                    else:
                        print("Frenata non salvata")

            except ValueError as e:
                print(f"Errore di previsione: {e}")

        else:
            print(f"Dati dei sensori non validi: Accelerometro - {len(accel_data)}, Giroscopio - {len(gyro_data)}")

        # Resetta i dati
        accel_data = None
        gyro_data = None


# Callback quando il client riceve un messaggio
def on_message(client, userdata, message):
    global accel_data, gyro_data

    payload = message.payload.decode('utf-8')
    # print(f"Messaggio ricevuto '{payload}' sul topic '{message.topic}'")

    # Preprocessa i dati
    data = preprocess_payload(payload)
    if data is not None:
        if message.topic == "iot/accelerometer":
            if len(data) == 3:
                accel_data = data
            else:
                print(f"Dati accelerometro non validi: {data}")
        elif message.topic == "iot/gyroscope":
            if len(data) == 3:
                gyro_data = data
            else:
                print(f"Dati giroscopio non validi: {data}")

        # Tenta di prevedere se abbiamo entrambi i dati di accelerometro e giroscopio
        try_predict()
    else:
        print("Impossibile preprocessare i dati per la previsione.")


# Callback quando il client si connette al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connessione avvenuta con successo")
        # Iscriviti ai topic
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        print(f"Connessione fallita con codice {rc}")


# Inizializza il client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connetti al broker MQTT
client.connect(BROKER_URL, BROKER_PORT, 60)

# Avvia il loop del client MQTT
client.loop_forever()
