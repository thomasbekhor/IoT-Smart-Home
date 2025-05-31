
import ssl
import time
import json
import streamlit as st

import paho.mqtt.client as mqtt_client
from paho.mqtt.client import CallbackAPIVersion

class MQTT_Publish:
    def __init__(self, broker, port, client_id, auth):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.ca = auth["ca"]
        self.cert = auth["cert"]
        self.private = auth["private"]


    def ssl_alpn(self):
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
            ssl_context.load_verify_locations(cafile=self.ca)
            ssl_context.load_cert_chain(certfile=self.cert, keyfile=self.private)
            return  ssl_context
        
        except Exception as e:
            print("exception ssl_alpn()")
            raise e


    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(
            client_id=self.client_id,
            protocol=mqtt_client.MQTTv311,
            callback_api_version=CallbackAPIVersion.VERSION2
        )
        client.tls_set_context(context=self.ssl_alpn())
        client.on_connect = on_connect
        client.connect(self.broker, self.port)

        return client


    def publish(self, client, topic, room, lamp, intensity):
        msg = json.dumps(
            { "room": room, "lamp": lamp, "intensity": intensity}
        )

        result = client.publish(topic, msg, 0)
        
        if result[0] == 0:
            print(f"[MQTT] Sent {msg} to topic {topic}")
        else:
            print(f"[MQTT] Failed to send message to topic {topic}")

        
        time.sleep(1)


    def pipeline_publish(self, topic, room, lamp, intensity):
        client = self.connect()
        self.publish(client, topic, room, lamp, intensity)
        client.disconnect()



if __name__ == "__main__":
    # Configurações
    broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"  # US-EAST-1
    port = 443
    client_id_publish = "yapublish"

    # Caminhos para seus certificados
    cert = st.secrets["mqtt_certs"]["cert"]
    private_key = st.secrets["mqtt_certs"]["private_key"]
    public_key = st.secrets["mqtt_certs"]["public_key"]

    # Salvar temporariamente (se o cliente MQTT exigir caminho de arquivo)
    with open("cert.pem", "w") as f:
        f.write(cert)

    with open("private.key", "w") as f:
        f.write(private_key)

    with open("public.key", "w") as f:
        f.write(public_key)

    aws_auth = {
        "ca": "cert.pem",
        "cert": "private.key",
        "private": "public.key"
    }

    mqtt_publish = MQTT_Publish(broker, port, client_id_publish, aws_auth)

    topic = "room2/led"
    room = "comodo1"
    lamp = "lampada1"
    intensity = 100
    mqtt_publish.pipeline_publish(topic, room, lamp, intensity)