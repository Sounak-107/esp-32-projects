import machine
import time

#set thr pins
led_pin= machine.Pin(19, machine.Pin.OUT)
ir_pin= machine.Pin(27, machine.Pin.IN)


try:
    while True:
        a= ir_pin.value()
        if a== 0:
            led_pin.on()
        else:
            led_pin.off()
except KeyboardInterrupt:
    print("disrrupted...")
    led_pin.off()
