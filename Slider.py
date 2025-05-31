
import json
import streamlit as st
from datetime import datetime

from MQTT.mqtt_publish import MQTT_Publish


class SliderWidget(MQTT_Publish):
    def __init__(self, name, min_value, max_value, default_value, session_key):
        self.name = name
        self.label = "Select a Value"

        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value

        self.data = self.readDatabase()  # Load the database

        self.session_key = session_key  # Unique key for the slider
        self.debug = st.session_state["debug_mode"]


    def readDatabase(self):
        with open("./db/dbV3.json", "r") as file:
            data = json.load(file)

        return data


    def update_brightness(self, quarto, device, brightness):
        def find_index(data, target):
            index = next((i for i, room in enumerate(data) if room["name"] == target), None)
            return index

        # Indexes to access the Database
        index_room = find_index(self.data["MyHome"], quarto)
        index_device = find_index(self.data["MyHome"][index_room]["devices"], device["name"])

        # Updating value from Database
        self.data["MyHome"][index_room]["devices"][index_device]["brightness"] = brightness

        with open('./db/dbV3.json', 'w') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)


    def render(self, title, device):
        # Create and render the slider widget; value is automatically stored by the unique key
        st.markdown(f"### {self.name}")
        slider_value = st.slider(
            self.label, 
            min_value=self.min_value, 
            max_value=self.max_value,
            step=10, 
            value=self.default_value, 
            key=self.session_key,
            format="%d%%"
        )

        # st.write("Slider Value:", slider_value)  
        
        # Print the debug information if debug mode is enabled
        if self.debug:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[DEBUG] ({current_time}) Slider ({self.session_key}) value: {slider_value}")
        
        broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"  # US-EAST-1
        port = 443
        client_id_publish = "yapublish"

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

        topic = device["topic"]
        room = device["topic"].split("/")[0]  # Assuming the topic is structured like "home/room/lamp"
        lamp = device["id"]
        intensity = slider_value
        mqtt_publish.pipeline_publish(topic, room, lamp, intensity)

        self.update_brightness(title, device, slider_value)

        return slider_value



if __name__ == '__main__':
    debug_mode = True
    slider = SliderWidget(
        name="Hall Lamp",
        min_value=0, max_value=100, default_value=75, 
        session_key=f"slider_1", 
        debug=debug_mode
    )

    def main():
        st.title("Slider Button Previw")

        
        # Create instances of the ToggleButton and SliderComponent with the debug flag
        
        # Render the component
        sliderValue = slider.render()  

    main()
