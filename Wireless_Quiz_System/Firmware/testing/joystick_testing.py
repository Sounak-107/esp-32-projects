from machine import Pin, ADC
import time

# Set up the analog pins for X and Y axes
joystick_x = ADC(Pin(35))
joystick_y = ADC(Pin(34))

# Tell the ESP32 to read the full 3.3V voltage range
joystick_x.atten(ADC.ATTN_11DB)
joystick_y.atten(ADC.ATTN_11DB)

# Set up the push-button with an internal pull-up resistor
button = Pin(32, Pin.IN, Pin.PULL_UP)

print("Starting Joystick Test...")

# Create an infinite loop to constantly read the values
while True:
    x_val = joystick_x.read()
    y_val = joystick_y.read()
    btn_val = button.value()
    
    # Print the data
    print("X:", x_val, " | Y:", y_val, " | Button:", btn_val)
    
    # Pause for a fraction of a second so the shell doesn't crash
    time.sleep(0.2)

