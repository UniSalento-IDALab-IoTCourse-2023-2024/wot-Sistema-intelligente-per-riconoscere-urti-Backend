import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    print(f"Received message: {data}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.subscribe("iot/sensordata")
client.loop_forever()
