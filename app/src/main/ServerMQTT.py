import joblib
import paho.mqtt.client as mqtt
import numpy as np
import re
import pandas as pd
import requests as requests


BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883
TOPICS = [("iot/accelerometer", 0), ("iot/gyroscope", 0)]

# Carica il modello pre-addestrato
with open('model.joblib', 'rb') as model_file:
    model = joblib.load(model_file)

# Variabili globali per memorizzare i dati dei sensori di accellerometro e giroscopio
accel_data = None
gyro_data = None

# Variabile globale che tiene conto del numero di eventi che sono stati rilevati fino a quel preciso momento
event_count = 0

# Variabile globale per memorizzare l'user_id
user_id = None

# Preprocessa il payload del messaggio in arrivo
def preprocess_payload(payload):
    try:
        payload = payload.replace(',', '.')

        user_id_match = re.search(r"user_id:\s*(\w+)", payload)
        if user_id_match:
            global user_id
            user_id = user_id_match.group(1)

        data = re.findall(r"[-+]?\d*\.\d+(?:[eE][-+]?\d+)?", payload)
        data = np.array([float(x) for x in data])
        return data
    except Exception as e:
        print(f"Errore durante l'elaborazione del payload: {e}")
        return None


# Funzione per pubblicare un messaggio via MQTT
def publish_mqtt_message(client, topic, message):
    try:
        client.publish(topic, message)
        print(f"Messaggio MQTT inviato al topic {topic}: {message}")
    except Exception as e:
        print(f"Errore durante l'invio del messaggio MQTT: {e}")


# Funzione per tentare la previsione mediante il modello di ML
def try_predict():
    global accel_data, gyro_data, event_count, user_id

    if accel_data is not None and gyro_data is not None:
        if len(accel_data) == 3 and len(gyro_data) == 3:
            combined_data = np.concatenate((accel_data, gyro_data)).reshape(1, -1)
            formatted_data = ["{:.4f}".format(x) for x in combined_data[0]]

            try:
                feature_names = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]
                combined_data_df = pd.DataFrame(combined_data, columns=feature_names)
                prediction = model.predict(combined_data_df)
                event_count += 1

                if prediction[0] == "incidenti":
                    url = "http://127.0.0.1:5001/api/incidenti/add_incidenti"
                    headers = {"Content-Type": "application/json"}
                    data = {"cliente_incidentato": user_id}

                    response = requests.post(url=url, headers=headers, json=data)

                    print(f"Valori Accelerometro: {accel_data}")
                    print(f"Valori Giroscopio: {gyro_data}")

                    if response.status_code == 200:
                        response_data = response.json()  # Decodifica la risposta JSON
                        incident_id = response_data.get("id")  # Ottieni l'ID dell'incidente

                        print("Incidente salvato con successo")
                        print(f"ID incidente: {incident_id}")

                        # Invia il messaggio tramite MQTT con l'ID dell'incidente al topic "iot/notifications"
                        publish_mqtt_message(client, "iot/notifications",
                                             f"Rilevato INCIDENTE con i seguenti valori.\n"
                                             f"Acccelerometro: {accel_data}\n"
                                             f"Giroscopio: {gyro_data}\n"
                                             f"ID Incidente: {incident_id}"
                                             )

                    else:
                        print("Incidente non salvato")

                # if prediction[0] == "frenate":
                #     url = "http://127.0.0.1:5001/api/frenate/add_frenate"
                #     headers = {"Content-Type": "application/json"}
                #     data = {"cliente": user_id}
                #     response = requests.post(url=url, headers=headers, json=data)
                #     print(f"Valori Accelerometro: {accel_data}")
                #     print(f"Valori Giroscopio: {gyro_data}")
                #     if response.status_code == 200:
                #         print("Frenata salvata con successo")
                #         publish_mqtt_message(client, "iot/notifications", f"Rilevata FRENATA con i seguenti valori.\nAcccelerometro: {accel_data}\nGiroscopio: {gyro_data}")
                #
                #     else:
                #         print("Frenata non salvata")

                if prediction[0] == "altro":
                    print(f"Valori Accelerometro: {accel_data}")
                    print(f"Valori Giroscopio: {gyro_data}")
                    publish_mqtt_message(client, "iot/notifications", "Evento rilevato: ALTRO")


            except ValueError as e:
                print(f"Errore di previsione: {e}")

        else:
            print(f"Dati dei sensori non validi: Accelerometro - {len(accel_data)}, Giroscopio - {len(gyro_data)}")

        accel_data = None
        gyro_data = None

# Callback quando il client riceve un messaggio
def on_message(client, userdata,message):
    global accel_data, gyro_data

    payload = message.payload.decode('utf-8')
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

        try_predict()
    else:
        print("Impossibile preprocessare i dati per la previsione.")

# Callback quando il client si connette al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connessione avvenuta con successo")
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        print(f"Connessione fallita con codice {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_URL, BROKER_PORT, 60)
client.loop_forever()
