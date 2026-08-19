from machine import Pin, PWM
import time

buzzer = PWM(Pin(26))
buzzer.duty(512)

print("Beeping...")

buzzer.freq(2000)
time.sleep(0.5)

buzzer.freq(1000)
time.sleep(0.5)

buzzer.duty(0)

print("Test complete!")

