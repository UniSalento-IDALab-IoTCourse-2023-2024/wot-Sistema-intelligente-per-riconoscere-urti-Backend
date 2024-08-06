import joblib
import paho.mqtt.client as mqtt
import numpy as np
import re

# Impostazioni MQTT
BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883
TOPICS = [("iot/accelerometer", 0), ("iot/gyroscope", 0)]

# Carica il modello pre-addestrato
with open('model.joblib', 'rb') as model_file:
    model = joblib.load('model.joblib')

# Variabili globali per memorizzare i dati dei sensori
accel_data = None
gyro_data = None


# Preprocessa il payload del messaggio in arrivo
def preprocess_payload(payload):
    try:
        # Estrae i numeri dal payload utilizzando una regex
        data = re.findall(r"[-+]?\d*\.\d+|\d+", payload)
        data = np.array([float(x) for x in data])
        return data
    except Exception as e:
        print(f"Errore durante l'elaborazione del payload: {e}")
        return None


# Funzione per tentare la previsione se sono disponibili entrambi i dataset
def try_predict():
    global accel_data, gyro_data

    if accel_data is not None and gyro_data is not None:
        # Combina i dati dei due sensori
        combined_data = np.concatenate((accel_data, gyro_data)).reshape(1, -1)

        # Predice l'evento
        prediction = model.predict(combined_data)
        print(f"Evento previsto: {prediction[0]}")

        # Resetta i dati
        accel_data = None
        gyro_data = None


# Callback quando il client riceve un messaggio
def on_message(client, userdata, message):
    global accel_data, gyro_data

    payload = message.payload.decode('utf-8')
    print(f"Messaggio ricevuto '{payload}' sul topic '{message.topic}'")

    # Preprocessa i dati
    data = preprocess_payload(payload)
    if data is not None:
        if message.topic == "iot/accelerometer":
            accel_data = data
        elif message.topic == "iot/gyroscope":
            gyro_data = data

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
