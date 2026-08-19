from machine import Pin, ADC, I2C, time_pulse_us, PWM  # type: ignore[import-not-found]
import time
import ssd1306  # type: ignore[import-not-found]
import example_button_configure  # The configuration file (must be edited to match the hardware)


# HARDWARE INITIALIZATION

# I2C OLED Setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Boot Screen
oled.fill(0)
oled.text("   WELCOME!   ", 10, 25)
oled.show()

# Receiver Input
receiver = Pin(27, Pin.IN)

# Joystick Setup
joy_x = ADC(Pin(35))             
joy_x.atten(ADC.ATTN_11DB)       

joy_y = ADC(Pin(34))            
joy_y.atten(ADC.ATTN_11DB)       

# Button set to PULL_UP
joy_btn = Pin(32, Pin.IN, Pin.PULL_UP)  

# Buzzer Output
# Buzzer Output (Configured for a Passive Buzzer)
buzzer = PWM(Pin(26))
buzzer.duty(0)  # Set volume to 0 (silent)


# HELPER FUNCTIONS FOR DISPLAY

def draw_menu(selected_index):
    """Draws the main mode selection screen."""
    oled.fill(0)
    oled.text("SELECT MODE:", 15, 0)
    oled.hline(0, 12, 128, 1)  
    
    prefix1 = "> " if selected_index == 0 else "  "
    oled.text(prefix1 + "Rapid Fire", 5, 22)
    
    prefix2 = "> " if selected_index == 1 else "  "
    oled.text(prefix2 + "Tie Breaker", 5, 42)
    
    oled.show()

def draw_rapid_fire(teams, back_selected):
    """Draws the Rapid Fire screen listing up to 3 teams."""
    oled.fill(0)
    oled.text("RAPID FIRE", 25, 0)
    oled.hline(0, 10, 128, 1)
    
    # Print the top 3 teams
    y_pos = 15
    for i in range(len(teams)):
        oled.text(str(i+1) + ". " + teams[i], 0, y_pos)
        y_pos += 12
        
    # Draw BACK button at bottom right
    oled.hline(0, 52, 128, 1)
    back_text = "> BACK" if back_selected else "  BACK"
    oled.text(back_text, 75, 55) 
    oled.show()

def draw_tie_breaker(teams_data, back_selected):
    """Draws the Tie Breaker screen split in two halves."""
    oled.fill(0)
    oled.text("TIE BREAKER", 20, 0)
    oled.hline(0, 10, 128, 1)
    
    # Left Side: First Team
    if len(teams_data) > 0:
        oled.text(teams_data[0][0], 0, 20)
        oled.text(teams_data[0][1], 0, 35)
        
    # Draw vertical split line
    if len(teams_data) > 1:
        oled.vline(64, 12, 38, 1)
        
    # Right Side: Second Team
    if len(teams_data) > 1:
        oled.text(teams_data[1][0], 68, 20)
        oled.text(teams_data[1][1], 64, 35)
        
    # Draw BACK button at bottom right
    oled.hline(0, 52, 128, 1)
    back_text = "> BACK" if back_selected else "  BACK"
    oled.text(back_text, 75, 55)
    oled.show()

time.sleep(1.5)


# MAIN STATE MACHINE LOOP

state = "MENU"
menu_option = 0  
in_game_back_selected = False
joystick_ready = True

# Lists to store the winning teams for each round
rf_teams = []
tb_data = []

draw_menu(menu_option)

while True:
    x_val = joy_x.read()
    y_val = joy_y.read()
    
    # Deadzone check for both X and Y axes
    if 1500 < x_val < 2500 and 1500 < y_val < 2500:
        joystick_ready = True

    # --------------------------------------
    # STATE 1: MENU NAVIGATION
    # --------------------------------------
    if state == "MENU":
        if joystick_ready:
            # Scroll Down or Right
            if (y_val > 3000 or x_val > 3000) and menu_option < 1:
                menu_option += 1
                draw_menu(menu_option)
                joystick_ready = False  
            # Scroll Up or Left
            elif (y_val < 1000 or x_val < 1000) and menu_option > 0:
                menu_option -= 1
                draw_menu(menu_option)
                joystick_ready = False  

        # Select Mode
        if joy_btn.value() == 0:
            time.sleep(0.1)  
            in_game_back_selected = False # Always default to Reset Mode, not Back
            if menu_option == 0:
                state = "RAPID_FIRE"
                rf_teams = [] # Clear previous memory
                draw_rapid_fire(rf_teams, in_game_back_selected)
            elif menu_option == 1:
                state = "TIE_BREAKER"
                tb_data = [] # Clear previous memory
                draw_tie_breaker(tb_data, in_game_back_selected)
            
            while joy_btn.value() == 0:
                pass
            time.sleep(0.1)  

    # --------------------------------------
    # STATE 2: ACTIVE GAME MODES
    # --------------------------------------
    elif state in ["RAPID_FIRE", "TIE_BREAKER"]:
        
        # 1. IN-GAME NAVIGATION (Cursor for the BACK button)
        if joystick_ready:
            # Pushing Right or Down selects the "> BACK" button
            if (x_val > 3000 or y_val > 3000) and not in_game_back_selected:
                in_game_back_selected = True
                joystick_ready = False
                if state == "RAPID_FIRE": draw_rapid_fire(rf_teams, True)
                else: draw_tie_breaker(tb_data, True)
                
            # Pushing Left or Up deselects BACK (Meaning a click will RESET the round)
            elif (x_val < 1000 or y_val < 1000) and in_game_back_selected:
                in_game_back_selected = False
                joystick_ready = False
                if state == "RAPID_FIRE": draw_rapid_fire(rf_teams, False)
                else: draw_tie_breaker(tb_data, False)

        # 2. IN-GAME BUTTON ACTION (Reset vs Exit)
        if joy_btn.value() == 0:
            time.sleep(0.1)
            
            if in_game_back_selected:
                # EXIT to Menu
                state = "MENU"
                draw_menu(menu_option)
            else:
                # RESET the current game for the next question
                if state == "RAPID_FIRE":
                    rf_teams = []
                    draw_rapid_fire(rf_teams, in_game_back_selected)
                elif state == "TIE_BREAKER":
                    tb_data = []
                    draw_tie_breaker(tb_data, in_game_back_selected)
            
            while joy_btn.value() == 0:
                pass
            time.sleep(0.1)
            continue # Skip reading the receiver right after a reset

        # 3. WIRELESS SIGNAL CAPTURE
        try:
            sync_pulse = time_pulse_us(receiver, 0, 20000)
            
            if sync_pulse > 5000:
                raw_id = 0
                for i in range(24):
                    high_pulse = time_pulse_us(receiver, 1, 5000)
                    raw_id = raw_id << 1
                    if high_pulse > 600:
                        raw_id = raw_id | 1
                
                remote_id = raw_id >> 4
                button_val = raw_id & 15
                
                #print("DEBUG - The Remote ID is:", remote_id, " | The Button is:", button_val)
                
                team_name = example_button_configure.teams.get(remote_id, "Unknown Team")
                button_name = example_button_configure.buttons.get(button_val, "Unknown")
                
                # RAPID FIRE LOGIC (First 3 unique teams) 
                if state == "RAPID_FIRE":
                    if len(rf_teams) < 3 and team_name not in rf_teams:
                        rf_teams.append(team_name)
                        draw_rapid_fire(rf_teams, in_game_back_selected)
                        
                        buzzer.freq(2000)  # Set the pitch (1000 Hz is a standard beep)
                        buzzer.duty(512)   # Set volume to 50%
                        time.sleep(0.5)    # Wait half a second
                        buzzer.duty(0)     # Turn the volume back to 0 (silent)
                        
                        
                # TIE BREAKER LOGIC (First 2 unique teams + Switch) 
                elif state == "TIE_BREAKER":
                    already_buzzed = any(t[0] == team_name for t in tb_data)
                    
                    if len(tb_data) < 2 and not already_buzzed:
                        tb_data.append((team_name, button_name))
                        draw_tie_breaker(tb_data, in_game_back_selected)
                        
                        buzzer.freq(2000)  # Set the pitch (2000 Hz is a standard beep)
                        buzzer.duty(512)   # Set volume to 50%
                        time.sleep(0.5)    # Wait half a second
                        buzzer.duty(0)     # Turn the volume back to 0 (silent)
                        
                
        except OSError:
            pass

    time.sleep_ms(10)
