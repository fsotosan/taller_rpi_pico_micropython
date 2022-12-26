# Taller Raspberry Pi Pico con MicroPython
# Blink con dos LEDs

import machine
import utime

led_placa = machine.Pin(25,machine.Pin.OUT)     # LED integrado en placa
led_ext = machine.Pin(16,machine.Pin.OUT)       # LED externo conectado a GP16 (pin 21)

led_placa.value(0)
led_ext.value(1)

while True:
    utime.sleep(0.5)
    led_placa.toggle()
    led_ext.toggle()