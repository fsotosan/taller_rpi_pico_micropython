# Taller Raspberry Pi Pico con MicroPython
# Conexión WIFI y servidor web
# Fuente: https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from pico_i2c_lcd import I2cLcd
import machine

ssid = 'Banana'
password = '_m3l0c0t0n_'

i2c_sda = machine.Pin(26)
i2c_scl = machine.Pin(27)

i2c = machine.I2C(1,sda=i2c_sda, scl=i2c_scl, freq=400000)
i2c_addr = i2c.scan()[0]
print("LCD addr:", i2c_addr)
lcd = I2cLcd(i2c, i2c_addr, 2, 16)
lcd.blink_cursor_on()
lcd.putstr("Hola")

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        action = ''
        print(request)
        try:
            action = request.split()[1]
        except IndexError:
            pass
        if action == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif action =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        elif action.startswith('/lcd?'):
            msg = action[5:].replace('%20',' ')
            lcd.clear()
            lcd.putstr(msg)
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()