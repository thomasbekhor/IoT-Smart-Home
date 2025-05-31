
import random

import ssl
import time
import paho.mqtt.client as mqtt_client

# Configurações de conexão MQTT e certificados
broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"
port = 443
topic = "room1/led"
client_id = "yapublish"

ca = "./certs/root-CA.crt"
cert = "./certs/edudardo_thing.cert.pem"
private = "./certs/edudardo_thing.private.key"

def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id)
    ssl_context = ssl_alpn()
    client.tls_set_context(context=ssl_context)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    room = "comodo1"
    lamp = "lampada1"
    intensity = random.randint(1,100)  # ou pode mudar ao longo do tempo se quiser

    msg = f'''{{"room": "{room}", "lamp": "{lamp}", "intensity": {intensity}}}'''

    result = client.publish(topic, msg, 0)
    
    if result[0] == 0:
        print(f"[function] Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    
    time.sleep(1)


def run():
    client = connect()
    publish(client)
    client.disconnect()



if __name__ == "__main__":
    run()