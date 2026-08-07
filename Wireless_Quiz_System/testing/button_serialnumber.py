from machine import Pin, time_pulse_us
import time

receiver = Pin(27, Pin.IN)

print("Ready to decode! Press a button...")

while True:
    try:
        # 1. Wait for the long Sync Pulse (LOW)
        sync_pulse = time_pulse_us(receiver, 0, 20000)
        
        if sync_pulse > 5000:
            # We found a sync pulse! Now create an empty variable to hold our data.
            button_id = 0
            
            # 2. Quickly read the next 24 data pulses
            for i in range(24):
                # Measure how long the signal stays HIGH0
                high_pulse = time_pulse_us(receiver, 1, 5000)
                
                # Shift our data over to make room for the new 1 or 0
                button_id = button_id << 1 
                
                # If the pulse is longer than 600 microseconds, it's a binary '1'
                if high_pulse > 600: 
                    button_id = button_id | 1
            
            # 3. Print the final unique decimal number!
            print(">>> Button ID Decoded:", button_id)
            
            # Pause so it doesn't read the same button press 10 times in a row
            time.sleep(0.5)
            
    except OSError:
        # If a pulse takes too long or fails, just quietly ignore it and keep listening
        pass

