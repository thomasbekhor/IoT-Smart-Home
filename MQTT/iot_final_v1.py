import ssl
import time
import paho.mqtt.client as mqtt_client
import RPi.GPIO as GPIO
import json

# Configuração GPIO para PWM dos LEDs
GPIO.setmode(GPIO.BCM)

LED_PIN_1 = 18  # Primeira lâmpada (room 1)
LED_PIN_2 = 19  # Segunda lâmpada (room 2)

# Configuração dos pinos para PWM
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

# Criando os PWM para cada lâmpada
pwm_1 = GPIO.PWM(LED_PIN_1, 1000)  # 1 kHz PWM para LED 1
pwm_2 = GPIO.PWM(LED_PIN_2, 1000)  # 1 kHz PWM para LED 2

# Iniciando com 0% de duty cycle para ambos os LEDs
pwm_1.start(0)
pwm_2.start(0)

# Configuração do sensor
PIN_SENSOR = 17      # Entrada digital do sensor (D0)
PIN_LED_RELE = 23    # Saída para LED/relé

# Configurar o modo da GPIO
GPIO.setup(PIN_SENSOR, GPIO.IN)         # Sensor como entrada
GPIO.setup(PIN_LED_RELE, GPIO.OUT)      # LED/relé como saída

# Configurações de MQTT
broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"
port = 443

# Tópicos para controle das lâmpadas
topic_subscribe_1 = "room1/led"  # Tópico para controle de intensidade do LED 1 (room 1)
topic_subscribe_2 = "room2/led"  # Tópico para controle de intensidade do LED 2 (room 2)

# Tópicos para publicação de status de intensidade
topic_publish_intensity_1 = "room1/led/status"  # Status da intensidade do LED 1
topic_publish_intensity_2 = "room2/led/status"  # Status da intensidade do LED 2

topic_publish_sensor = "iot/room/sensor_status"  # Tópico para publicar o status do sensor

client_id = "combined_client"

ca = "./certs/root-CA.crt"
cert = "./certs/edudardo_thing.cert.pem"
private = "./certs/edudardo_thing.private.key"

# Variáveis para controlar a intensidade dos LEDs
current_intensity_1 = 0
current_intensity_2 = 0

# Função de SSL
def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        return ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

# Conexão com o MQTT
def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ Conectado ao MQTT Broker!")
            # Inscrever-se nos tópicos de controle de intensidade dos LEDs
            client.subscribe(topic_subscribe_1)
            client.subscribe(topic_subscribe_2)
        else:
            print(f"❌ Falha na conexão, código de retorno {rc}")

    client = mqtt_client.Client(client_id=client_id)
    ssl_context = ssl_alpn()
    client.tls_set_context(context=ssl_context)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

# Função para processar mensagens recebidas do MQTT
def on_message(client, userdata, msg):
    global current_intensity_1, current_intensity_2
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Mensagem recebida no tópico {msg.topic}: {payload}")
        
        # Converte a mensagem JSON recebida
        data = json.loads(payload)
        
        if msg.topic == topic_subscribe_1:
            # Controla a intensidade do LED 1 (room1)
            intensity_1 = data.get("intensity", -1)
            if 0 <= intensity_1 <= 100:
                current_intensity_1 = intensity_1
                pwm_1.ChangeDutyCycle(current_intensity_1)  # Ajusta a intensidade do PWM para LED 1
                # Publica a intensidade atual do LED 1
                publish_intensity_status(client, 1, current_intensity_1)
        
        if msg.topic == topic_subscribe_2:
            # Controla a intensidade do LED 2 (room2)
            intensity_2 = data.get("intensity", -1)
            if 0 <= intensity_2 <= 100:
                current_intensity_2 = intensity_2
                pwm_2.ChangeDutyCycle(current_intensity_2)  # Ajusta a intensidade do PWM para LED 2
                # Publica a intensidade atual do LED 2
                publish_intensity_status(client, 2, current_intensity_2)

    except Exception as e:
        print(f"⚠️ Erro ao processar mensagem: {e}")
        print(f"Mensagem recebida: {msg.payload}")

# Publica o status de intensidade dos LEDs
def publish_intensity_status(client, led_number, intensity):
    if led_number == 1:
        topic = topic_publish_intensity_1
    elif led_number == 2:
        topic = topic_publish_intensity_2
    msg = f'{{"intensity": {intensity}}}'
    result = client.publish(topic, msg, 0)
    if result.rc == mqtt_client.MQTT_ERR_SUCCESS:
        print(f"📤 Sent intensity `{intensity}` to topic `{topic}`")
    else:
        print(f"❌ Falha ao enviar a mensagem para o tópico `{topic}`")

# Função para monitorar o sensor e publicar seu status
def monitor_sensor():
    sensor_state = GPIO.input(PIN_SENSOR)

    if sensor_state == GPIO.HIGH:
        # Sensor NÃO detectou nada (sem gás/fumaça/presença)
        GPIO.output(PIN_LED_RELE, GPIO.HIGH)  # Liga LED/relé
        print("Presença detectado! LED ligado.")
        return "On"
    else:
        # Sensor detectou presença (gás/fumaça, etc.)
        GPIO.output(PIN_LED_RELE, GPIO.LOW)   # Desliga LED/relé
        print("Ambiente limpo! LED desligado.")
        return "Off"
        
# Publica o status do sensor
def publish_sensor_status(client):
    sensor_status = monitor_sensor()
    msg = json.dumps({"sensor_status": sensor_status})
    result = client.publish(topic_publish_sensor, msg, 0)
    if result.rc == mqtt_client.MQTT_ERR_SUCCESS:
        print(f"📤 Sent sensor status `{sensor_status}` to topic `{topic_publish_sensor}`")
    else:
        print("❌ Falha ao enviar a mensagem para o tópico de sensor status")

# Função principal para rodar o script
def run():
    client = connect()
    client.on_message = on_message  # Define o callback de recebimento de mensagens
    client.loop_start()  # Inicia o loop do cliente MQTT

    try:
        while True:
            # Monitorar o sensor e publicar seu status
            publish_sensor_status(client)

            # Loop principal do MQTT para controlar a intensidade dos LEDs
            time.sleep(1)

    except KeyboardInterrupt:
        print("❌ Interrompido pelo usuário.")
    finally:
        pwm_1.stop()
        pwm_2.stop()
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()

run()
