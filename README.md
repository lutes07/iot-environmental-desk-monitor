# iot-environmental-desk-monitor

## Project Overview
This project is an IoT-enbaled evnironmental sensing system that is made to monitor and log surrounding conditions in real time. The system measures temperature, humidity, light level, and distance away from the sensor, displaying the live data on an OLED screen while also pushing it to the cloud via ThingSpeak for long term data collection and anaylsis

The actual cicurity is housed in a custom designed, laser-cut box.

## Hardware Components
* **Microcontroller**: (To be filled in)
* **AHT20**: Temperature and humidty sensor.
* **Photoresistor**: Ambient light intesity sensor
* **US-100**: Ultrasonic distance sensor
* **Featherawing OLED 128x64 Screen**: Local display for real-time data readouts.
* **Box Enclosure**: Laser-cut wood housing designed for optimal sensor exposure and wire managment.

## Software & Cloud Integration
* **Languages**: MicroPython and Python
* **Data Logging**: Integrated with the **ThingSpeak API** to upload environmental data packets, allowing for remote monitoring and data visualization with graphs.
* **Local Display**: (To be filled in)

## System Architecture
1. **Data Acquisition**: The microcontoller polls the AHT20, Photoresistor, and US-100 at regular intervals.
2. **Local Poressing & UI**: The raw data from the sensor is formatted and moved to the FeatherWing OLED.
3. **Cloud Transmission**: An HTTP requrest is formatted with the current sensor payload and is sent over to the ThingSpeak cloud by Wi-Fi.

