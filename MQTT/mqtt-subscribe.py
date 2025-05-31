
import ssl
import time
import json

import paho.mqtt.client as mqtt_client
from paho.mqtt.client import CallbackAPIVersion

class MQTT_Client:
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


    def connect(self, topic):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                client.subscribe(topic, qos=1)
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(
            client_id=self.client_id,
            protocol=mqtt_client.MQTTv311,
            callback_api_version=CallbackAPIVersion.VERSION2
        )
        client.tls_set_context(context=self.ssl_alpn())
        client.on_connect = on_connect
        client.on_message = self.on_message
        # client.connect(self.broker, self.port)

        return client
    

    def on_message(self, client, userdata, message):
        lamp_status = {}
        try:
            payload = message.payload.decode("utf-8")
            data = json.loads(payload)

            intensity = data.get("intensity", -1)
            lamp_status["default"] = intensity  # usamos uma chave padrão

            # Exibe status atual
            print("\n📋 Estado Atual das Lâmpadas:")
            for key, val in lamp_status.items():
                print(f"  - {key} -> Intensidade: {val}")

        except Exception as e:
            print(f"⚠️ Erro ao processar mensagem: {e}")
            print(f"Mensagem recebida: {message.payload}")


    def pipeline_subscribe(self, topic):
        client = self.connect(topic)
        client.loop_forever()



if __name__ == "__main__":
    # Configurações
    broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"  # US-EAST-1
    port = 443
    client_id_publish = "yapublish"
    client_id_subscribe = "yasubscribe"

    # Caminhos para seus certificados
    aws_auth = {
        "ca": "./certs/root-CA.crt",
        "cert": "./certs/edudardo_thing.cert.pem",
        "private": "./certs/edudardo_thing.private.key"
    }

    mqtt_subscribe = MQTT_Client(broker, port, client_id_publish, aws_auth)

    topic = "room1/led"
    # room = "comodo1"
    # lamp = "lampada1"
    # intensity = 100
    mqtt_subscribe.pipeline_subscribe(topic)