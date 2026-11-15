import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		client.subscribe("/tsensor/#")
	else:
		print(f"Connection failed: {rc}", flush=True)


def on_message(client, userdata, message):
	print(f"{message.topic}: {message.payload.decode('utf-8', errors='replace')}", flush=True)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt-broker", 1883)
client.loop_forever()
