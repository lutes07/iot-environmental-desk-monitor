import os
import time
import ssl
import terminalio
import displayio
import adafruit_hcsr04
import wifi
import board
import socketpool
import adafruit_requests
import adafruit_ahtx0
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from adafruit_display_text import label
from adafruit_st7789 import ST7789

light_pin = AnalogIn(board.A0)

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D10, echo_pin=board.D11)

try:
    i2c = board.I2C()
    aht20 = adafruit_ahtx0.AHTx0(i2c)
    print("AHT20 Sensor: Found")
except Exception:
    print("AHT20 Sensor: Not found (Check SDA/SCL)")
    aht20 = None

button = DigitalInOut(board.D12)
button.direction = Direction.INPUT
button.pull = Pull.UP

print("--- CONNECTING TO WIFI ---")
try:
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print(f"Connected to: {os.getenv('CIRCUITPY_WIFI_SSID')}")
except Exception as e:
    print(f"WiFi Connection Failed: {e}")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
api_key = "RPNXYKFO02MLMNUK"

is_collecting = False
last_upload_time = 0
upload_interval = 300
previous_button_state = button.value

print("System Ready. Waiting for button press...")

while True:
    current_button_state = button.value
    if current_button_state == False and previous_button_state == True:
        if is_collecting == False:
            is_collecting = True
            print("Collection Started")
            last_upload_time = time.monotonic()
        elif is_collecting == True:
            is_collecting = False
            print("Collection Paused")
        time.sleep(0.2)
    previous_button_state = current_button_state

    if is_collecting == True:
        current_time = time.monotonic()

        if(current_time - last_upload_time) >= upload_interval:
            print("5 minutes have passed! Sending data...")
            light_mv = (light_pin.value * 3300) / 65535
            
            try:
                distance = sonar.distance
                print(f"Distance:    {distance:.1f} cm")
            except RuntimeError:
                distance = 0
                print("Distance:    Out of range")

            if aht20:
                temp_f = (aht20.temperature * 9 / 5) + 32
                humidity = aht20.relative_humidity
            else:
                temp_f = 0
                humidity = 0

            mac_addr = ':'.join(['{:02X}'.format(i) for i in wifi.radio.mac_address])
            print("-" * 30)
            print(f"MAC Address: {mac_addr}")
            print(f"IP Address:  {wifi.radio.ipv4_address}")
            print(f"Light:       {light_mv:.1f} mV")
            print(f"Temperature: {temp_f:.1f} F")
            print(f"Humidity:    {humidity:.1f} %")
            print("-" * 30)

            update_url = f"https://api.thingspeak.com/update?api_key={api_key}&field1={light_mv:.1f}&field2={temp_f:.1f}&field3={humidity:.1f}&field4={distance:.1f}"

            print("Updating ThingSpeak...")
            try:
                response = requests.get(update_url)
                print(f"ThingSpeak Entry ID: {response.text}")
                response.close()
            except Exception as e:
                print(f"Failed to update ThingSpeak: {e}")

            print("Done!")
            last_upload_time = current_time
    
    time.sleep(0.05)
