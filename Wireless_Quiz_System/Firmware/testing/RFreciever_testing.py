from machine import Pin, time_pulse_us
import time

receiver = Pin(27, Pin.IN)

print("Filtering out static...")
print("Listening for a real remote!")

while True:
    try:
        # Look for a LOW (0) pulse. 
        # Wait a maximum of 20,000 microseconds (20ms) before giving up
        pulse_length = time_pulse_us(receiver, 0, 20000)
        
        if pulse_length > 5000:
            print(">>> REMOTE BUTTON PRESSED! Sync Pulse:", pulse_length, "us")
            
            # Pause for half a second so we don't spam the screen on a single press
            time.sleep(0.5) 
            
    except OSError:
        # If no long pulse is found within 20ms, it "times out". 
        # We just ignore it and loop back to try again.
        pass

