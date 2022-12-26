# Taller Raspberry Pi Pico con MicroPython
# Control de un servo con un potenciómetro

import machine
import utime

servo = machine.PWM(machine.Pin(0))   # Señal de control del servo conectada a para GPIO0 (pin 1)
servo.freq(50)                        # Período de PWM de 20 ms (50 Hz)
pot = machine.ADC(26)                 # Pin central del potenciómetro conectada a ADC0 en GPIO26 (pin 31)

# Conversión de grados a duty cycle en 
def duty(deg):
    duty_0_deg = 1500                 # Rango [0,180] -> [1000,9000] 
    duty_180_deg = 8500
    return int(duty_0_deg + (duty_180_deg-duty_0_deg)*(deg/180))

def adc2deg(adc):
    max_adc = 65535                   # Aunque el ADC es de 12 bits la lectura mediante read_u16() davuelve un rango de 16 bits 
    return int(adc*180/max_adc)       # Rango [0,65535] -> [0,180]

while True:
    lectura_pot = pot.read_u16()      # Leemos el valor del ADC (rango de 16 bits)
    grados = adc2deg(lectura_pot)     # Convertimos el valor a grados
    servo.duty_u16(duty(grados))      # Convertimos los grados a duty cycle y actualizamos el PWM
    utime.sleep(0.1)                  # Esperamos al menos un período (5 en este caso)
    
