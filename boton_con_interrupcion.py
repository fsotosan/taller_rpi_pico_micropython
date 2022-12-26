# Taller Raspberry Pi Pico con MicroPython
# Botón con interrupción

import machine
import utime

# Handler de interrupción
# Parpadeo rápidp del LED de la placa
def boton_pulsado_handler(pin):
    global led_placa
    for i in range(10):
        led_placa.toggle()
        utime.sleep_ms(50)

led_placa = machine.Pin(25,machine.Pin.OUT)                     # LED integrado en placa
boton = machine.Pin(19,machine.Pin.IN,machine.Pin.PULL_UP)      # Botón conectado a GP19 y GND, con resistencia interna de PULL-UP
boton.irq(trigger=machine.Pin.IRQ_FALLING, handler=boton_pulsado_handler)

while True:
    led_placa.toggle()
    utime.sleep(1)
