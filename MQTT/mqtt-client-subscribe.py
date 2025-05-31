import ssl
import json
import paho.mqtt.client as mqtt_client

# Configurações
broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"  # US-EAST-1
port = 443
topic = "room1/led/status"  # Ou use "iot/room" se quiser ser mais específico
client_id = "yasubscribe"

# Caminhos para seus certificados
ca = "./certs/root-CA.crt"
cert = "./certs/edudardo_thing.cert.pem"
private = "./certs/edudardo_thing.private.key"
# Dicionário para armazenar o estado das lâmpadas
lamp_status = {}

def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        return ssl_context
    except Exception as e:
        print("Erro ao configurar SSL/ALPN")
        raise e

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao MQTT Broker!")
        client.subscribe(topic, qos=1)
    else:
        print(f"❌ Falha na conexão, código de retorno: {rc}")

def on_message(client, userdata, message):
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


def run():
    # client = mqtt_client.Client(client_id=client_id)
    # ssl_context = ssl_alpn()
    # client.tls_set_context(context=ssl_context)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_forever()

run()
