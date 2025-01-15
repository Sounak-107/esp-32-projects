from machine import Pin, I2C, PWM
import time
import bh1750
import hcsr04

# Initialize I2C for BH1750
i2c = I2C(0, sda=Pin(21), scl=Pin(22))  # Change pin numbers as needed
light_sensor = bh1750.BH1750(i2c)

# Initialize HC-SR04
sensor1 = hcsr04.HCSR04(trigger_pin=5, echo_pin=18)  # Change pin numbers as needed
sensor2 = hcsr04.HCSR04(trigger_pin=19, echo_pin=23)  # Change pin numbers as needed

# Initialize PWM for analog SSR dimmer module
pwm_pin = Pin(13, Pin.OUT)  # Change pin number as needed
pwm = PWM(pwm_pin, freq=1000)  # PWM frequency (1kHz)

# Define brightness adjustment function
def set_brightness(value):
    # Map brightness from 0-100 to PWM duty cycle (0-1023)
    duty = int((value / 100) * 1023)
    pwm.duty(duty)

# Define thresholds and constants
LIGHT_THRESHOLD = 50  # Threshold for ambient light (lux)
DISTANCE_THRESHOLD = 20  # Distance threshold for brightness adjustment (cm)
BRIGHTNESS_INCREASE = 20  # Percentage to increase brightness
BRIGHTNESS_DECREASE = 20  # Percentage to decrease brightness

def read_light():
    # Read ambient light level from BH1750
    return light_sensor.luminance(BH1750.ONCE_HIRES_1)

def read_distance(sensor):
    # Read distance from HC-SR04
    return sensor.distance_cm()

def adjust_brightness(distance1, distance2):
    # Adjust brightness based on distance from two HC-SR04 sensors
    average_distance = (distance1 + distance2) / 2
    if average_distance < DISTANCE_THRESHOLD:
        # Increase brightness if object is close
        current_brightness = min(100, current_brightness + BRIGHTNESS_INCREASE)
    else:
        # Decrease brightness if object is far
        current_brightness = max(0, current_brightness - BRIGHTNESS_DECREASE)
    set_brightness(current_brightness)

# Main loop
current_brightness = 0  # Initial brightness (0% to 100%)

while True:
    # Read ambient light
    ambient_light = read_light()

    if ambient_light < LIGHT_THRESHOLD:
        # If light is low, turn on lamp and adjust brightness based on distance
        pwm.duty(0)  # Ensure lamp is on
        distance1 = read_distance(sensor1)
        distance2 = read_distance(sensor2)
        adjust_brightness(distance1, distance2)
    else:
        # If light is sufficient, turn off lamp
        pwm.duty(1023)  # Ensure lamp is off (or set to minimum brightness)

    # Delay before next reading
    time.sleep(1)
