from machine import Pin, I2C
import ssd1306

# Set up the I2C communication on the pins we just wired
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Tell the ESP32 the size of the screen (128 pixels wide, 64 pixels high)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear the screen 
oled.fill(0)

# Write the test text (The numbers are the X and Y coordinates)
oled.text("Hardware Test:", 0, 0)
oled.text("Screen is ALIVE!", 0, 20)

# Push the text to the physical display
oled.show()

