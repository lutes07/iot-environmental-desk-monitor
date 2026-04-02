# IoT Environmental Desk Monitor

## Project Overview
This project is an IoT-enabled environmental sensing system designed to monitor and log surrounding conditions in real time. The system measures temperature, humidity, light level, and distance away from the sensor, displaying the live data on a 1.9" Color TFT screen while also pushing it to the cloud via ThingSpeak for long-term data collection and analysis.

The actual circuitry is housed in a custom-designed, laser-cut box.

## Hardware Components
* **Microcontroller**: Adafruit ESP32-S3 Feather
* **AHT20**: Temperature and humidity sensor.
* **Photoresistor**: Ambient light intensity sensor.
* **HC-SR04**: Ultrasonic distance sensor.
* **Adafruit 1.9" 320x170 Color IPS TFT**: Local display for real-time data readouts.
* **Box Enclosure**: Laser-cut wood housing designed for optimal sensor exposure and wire management.

## Current Progress
*The main system set up with the AHT20, Microcontroller, Photoresistor, and button control*
![PXL_20260402_010648230](https://github.com/user-attachments/assets/06de61c6-0b7e-471f-b860-77f77a367897)
*The current build featuring the 1.9" TFT display and HC-SR04 sensor integration. This is a seperate testing build I made to test the OLED display and distance sensor.*
![PXL_20260402_190510851](https://github.com/user-attachments/assets/d740372d-375f-4679-8fba-79e34f7bd712)

## Software & Cloud Integration
* **Languages**: CircuitPython and Python
* **Data Logging**: Integrated with the **ThingSpeak API** to upload environmental data packets, allowing for remote monitoring and data visualization with graphs.
* **Local Display**: 1.9" Color TFT using the ST7789 driver.

## System Architecture
1. **Data Acquisition**: The microcontroller polls the AHT20, Photoresistor, and HC-SR04 at regular intervals.
2. **Local Processing & UI**: The raw data from the sensors is formatted and sent to the 1.9" Color TFT.
3. **Cloud Transmission**: An HTTP request is formatted with the current sensor payload and is sent to the ThingSpeak cloud via Wi-Fi.

