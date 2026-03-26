import os
import ssl
import wifi
import board
import socketpool
import adafruit_requests
import adafruit_ahtx0
from analogio import AnalogIn

light_pin = AnalogIn(board.A0)

try:
    i2c = board.I2C()
    aht20 = adafruit_ahtx0.AHTx0(i2c)
    print("AHT20 Sensor: Found")
except Exception:
    print("AHT20 Sensor: Not found (Check SDA/SCL)")
    aht20 = None
    aht20 = None

print("--- CONNECTING TO WIFI ---")
try:
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print(f"Connected to: {os.getenv('CIRCUITPY_WIFI_SSID')}")
except Exception as e:
    print(f"WiFi Connection Failed: {e}")

# Setup Web Requests
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# Calculate Light in mV
light_mv = (light_pin.value * 3300) / 65535

# Calculate Temp/Humidity
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

# Using a single-line URL to prevent syntax errors
api_key = "RPNXYKFO02MLMNUK"
update_url = f"https://api.thingspeak.com/update?api_key={api_key}&field1={light_mv:.1f}&field2={temp_f:.1f}&field3={humidity:.1f}"

print("Updating ThingSpeak...")
try:
    response = requests.get(update_url)
    print(f"ThingSpeak Entry ID: {response.text}")
    response.close()
except Exception as e:
    print(f"Failed to update ThingSpeak: {e}")

print("Done!")
