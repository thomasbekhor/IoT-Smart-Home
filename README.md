# 💡 Smart House IoT System

This project simulates a **smart home lighting automation system** using a **Raspberry Pi** connected to **AWS IoT Core**. The system allows users to control LEDs either manually through a web interface or automatically via a motion sensor.

---

## 📌 Problem

Most home lighting systems still rely on manual switches, lacking features such as intensity control and presence-based automation. As a result, smart home technology remains expensive and inaccessible to many.

---

## 🧠 Solution

Development of a complete system that simulates lamp control through:

* Interactive Web Interface (Streamlit)
* Backend logic in Python
* MQTT Broker hosted on AWS IoT Core
* IoT Device (Raspberry Pi with LEDs and motion sensor)

---

## 🧱 System Architecture

```
[User] → [Web Interface - Streamlit] 
        ↕ MQTT
[Backend - Python] 
        ↕ MQTT
[AWS IoT Core - MQTT Broker] 
        ↕ MQTT
[IoT Device - Raspberry Pi + Motion Sensor]
```

---

## 🔧 Technologies Used

* **Python**
* **Streamlit** – Web interface
* **MQTT** – Communication protocol
* **AWS IoT Core** – MQTT broker
* **Raspberry Pi** – IoT device
* **Motion Sensor** – Automatic activation

---

## ⚙️ Components & Development

### 1. **MQTT Broker on AWS**

* Created a *Thing* (representing the ESP32/RPi) in the AWS IoT console.
* Generated and stored authentication files (.pem certificate, .private.key, Amazon Root CA).
* Defined a permission policy for MQTT publish/subscribe.
* Secure connection configured via TLS (port 8883).

### 2. **Backend and Web Interface**

* Developed in **Python** using **Streamlit**.
* MQTT-based communication for real-time control.
* Users can manually toggle 2 LEDs from the interface.

### 3. **IoT Device**

* **2 LED circuits** with 220-ohm resistors connected to PWM outputs.
* **1 motion-triggered LED** circuit connected to a digital GPIO.
* Integrated with MQTT logic for seamless control.

---

## ✅ Results

* Full control of LEDs via a simple, intuitive web interface.
* Motion sensor triggers automatic lighting without user input.
* Secure and stable communication between all system components.

---

## 🚀 Future Improvements

* Scheduled lamp activation (e.g., based on time of day).
* Data logging and analysis for energy consumption.
* Usage pattern detection and optimization.


