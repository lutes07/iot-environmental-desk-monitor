import time
import board
import terminalio
import displayio
import adafruit_hcsr04
from adafruit_display_text import label
from adafruit_st7789 import ST7789

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D6

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)
display = ST7789(display_bus, width=340, height=240, rotation=270)

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D10, echo_pin=board.D11)

splash = displayio.Group()
display.root_group = splash

text_area = label.Label(terminalio.FONT, text="Distance: 0 cm", color=0xFFFFFF, x=20, y=120, scale=3)
splash.append(text_area)

while True:
    try:
        dist = sonar.distance
        text_area.text = f"Distance: {dist:.1f} cm"
    except RuntimeError:
        text_area.text = "Error/Out of range"
    time.sleep(0.1)
