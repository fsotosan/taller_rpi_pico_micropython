# Taller Raspberry Pi Pico con MicroPython
# Termómetro y LCD
# Fuente: https://raphaelkabo.com/blog/pi-pico-hd44780/

from machine import Pin, Timer
from machine import ADC
import utime

# Almost entirely copied from micropython-lcd by wjdp
# https://github.com/wjdp/micropython-lcd
class LCD(object):
    # Pinout, change within or outside class for your use case
    PINS = [16, 17, 18, 19, 20, 21]
    # Pin names, don't change
    PIN_NAMES = ['RS','E','D4','D5','D6','D7']

    # Dict of pins
    pins = {}

    # Pin mode, push-pull control
    PIN_MODE = Pin.OUT

    # Define some device constants
    LCD_WIDTH = 16    # Maximum characters per line
    # Designation of T/F for character and command modes
    LCD_CHR = True
    LCD_CMD = False

    LINES = {
        0: 0x80, # LCD RAM address for the 1st line
        1: 0xC0, # LCD RAM address for the 2nd line
        # Add more if desired
    }

    # Timing constants
    E_PULSE = 1
    E_DELAY = 1

    def init(self):
        # Initialise pins
        for pin, pin_name in zip(self.PINS, self.PIN_NAMES):
            self.pins['LCD_'+pin_name] = Pin(pin, self.PIN_MODE)
        # Initialise display
        self.lcd_byte(0x33,self.LCD_CMD)
        self.lcd_byte(0x32,self.LCD_CMD)
        self.lcd_byte(0x28,self.LCD_CMD)
        self.lcd_byte(0x0C,self.LCD_CMD)
        self.lcd_byte(0x06,self.LCD_CMD)
        self.lcd_byte(0x01,self.LCD_CMD)

    def clear(self):
        # Clear the display
        self.lcd_byte(0x01,self.LCD_CMD)

    def set_line(self, line):
        # Set the line that we're going to print to
        self.lcd_byte(self.LINES[line], self.LCD_CMD)

    def set_string(self, message):
        # Pad string out to LCD_WIDTH
        m_length = len(message)
        if m_length < self.LCD_WIDTH:
            short = self.LCD_WIDTH - m_length
            blanks=str()
            for i in range(short):
                blanks+=' '
            message+=blanks
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        self.pin_action('LCD_RS', mode) # RS

        # High bits
        self.pin_action('LCD_D4', False)
        self.pin_action('LCD_D5', False)
        self.pin_action('LCD_D6', False)
        self.pin_action('LCD_D7', False)
        if bits&0x10==0x10:
            self.pin_action('LCD_D4', True)
        if bits&0x20==0x20:
            self.pin_action('LCD_D5', True)
        if bits&0x40==0x40:
            self.pin_action('LCD_D6', True)
        if bits&0x80==0x80:
            self.pin_action('LCD_D7', True)

        # Toggle 'Enable' pin
        self.udelay(self.E_DELAY)
        self.pin_action('LCD_E', True)
        self.udelay(self.E_PULSE)
        self.pin_action('LCD_E', False)
        self.udelay(self.E_DELAY)

        # Low bits
        self.pin_action('LCD_D4', False)
        self.pin_action('LCD_D5', False)
        self.pin_action('LCD_D6', False)
        self.pin_action('LCD_D7', False)
        if bits&0x01==0x01:
            self.pin_action('LCD_D4', True)
        if bits&0x02==0x02:
            self.pin_action('LCD_D5', True)
        if bits&0x04==0x04:
            self.pin_action('LCD_D6', True)
        if bits&0x08==0x08:
            self.pin_action('LCD_D7', True)

        # Toggle 'Enable' pin
        self.udelay(self.E_DELAY)
        self.pin_action('LCD_E', True)
        self.udelay(self.E_PULSE)
        self.pin_action('LCD_E', False)
        self.udelay(self.E_DELAY)

    def udelay(self, us):
        # Delay by us microseconds, set as function for portability
        utime.sleep_ms(us)

    def pin_action(self, pin, high):
        # Pin high/low functions, set as function for portability
        if high:
            self.pins[pin].value(1)
        else:
            self.pins[pin].value(0)

display = LCD()
display.init()

sensor_temp = ADC(4)
conv_factor = 3.3 / 65535
old_temp = 0.0 
while True:
    reading = sensor_temp.read_u16() * conv_factor 
    deg_celsius = round(27 - (reading - 0.706)/0.001721,1)
    if deg_celsius != old_temp:
        old_temp = deg_celsius
        display.set_line(0)
        display.set_string("Temperatura: {}".format(deg_celsius))
    utime.sleep(5)



