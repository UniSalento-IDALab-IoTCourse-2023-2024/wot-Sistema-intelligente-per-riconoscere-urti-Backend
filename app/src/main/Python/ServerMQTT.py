import paho.mqtt.client as mqtt

# MQTT settings
BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883
TOPICS = [("iot/accelerometer", 0), ("iot/gyroscope", 0)]

# Callback when the client receives a message
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Received message '{payload}' on topic '{message.topic}'")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to topics
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        print(f"Connect failed with code {rc}")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(BROKER_URL, BROKER_PORT, 60)

# Start the MQTT client loop
client.loop_forever()
