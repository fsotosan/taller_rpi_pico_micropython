import machine
import utime

servo = machine.PWM(machine.Pin(0))   # Señal de control del servo conectada a para GPIO0 (pin 1)
servo.freq(50)                        # Período de PWM de 20 ms (50 Hz)

sensor_ir = machine.Pin(1,machine.Pin.IN, machine.Pin.PULL_UP)

grados_servo = 0

# Conversión de grados a duty cycle en 
def duty_u16(deg):
    duty_0_deg = 2000                 # Rango [0,180] -> [1000,9000] 
    duty_180_deg = 8000
    return int(duty_0_deg + (duty_180_deg-duty_0_deg)*(deg/180))

def movimiento_progresivo(grados):
    global grados_servo
    diferencia = grados - grados_servo
    sign = 1
    if diferencia < 0:
        sign = -1
    while diferencia != 0:
        grados_servo = grados_servo + sign
        servo.duty_u16(duty_u16(grados_servo))
        diferencia = grados - grados_servo
        utime.sleep(0.02)

def barrera_abre():
    movimiento_progresivo(90)
    print("abierto")
    
def barrera_cierra():
    movimiento_progresivo(4)
    print("cerrado")

def sensor_ir_handler(pin):
    barrera_abre()

servo.duty_u16(duty_u16(grados_servo))
barrera_cierra()
sensor_ir.irq(trigger=machine.Pin.IRQ_FALLING, handler=sensor_ir_handler)

while True: 
    if sensor_ir.value() == 1:
        barrera_cierra()
    utime.sleep(2)
