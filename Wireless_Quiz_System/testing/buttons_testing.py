from machine import Pin, time_pulse_us
import time
import buttonconfigure  # This pulls in your custom dictionaries!

receiver = Pin(27, Pin.IN)

print("Integration Test Started!")
print("Press any button on any remote...")

while True:
    try:
        # 1. Wait for the long Sync Pulse
        sync_pulse = time_pulse_us(receiver, 0, 20000)
        
        if sync_pulse > 5000:
            raw_id = 0
            
            # 2. Read the 24 data bits
            for i in range(24):
                high_pulse = time_pulse_us(receiver, 1, 5000)
                raw_id = raw_id << 1 
                if high_pulse > 600: 
                    raw_id = raw_id | 1
            
            # 3. The Hacker Math: Extract the Team ID and Button ID
            remote_id = raw_id >> 4
            button_val = raw_id & 15
            
            # 4. Look up the names in your buttonconfigure file safely
            # Using .get() prevents the code from crashing if an unknown remote is presse
            team_name = buttonconfigure.teams.get(remote_id, "Unknown Team")
            button_name = buttonconfigure.buttons.get(button_val, "Unknown Button")
            
            # 5. Print the final decoded result!
            print(">>> SUCCESS:", team_name, "|", button_name)
            
            # Pause to prevent a single press from triggering multiple times
            time.sleep(0.5)
            
    except OSError:
        pass
