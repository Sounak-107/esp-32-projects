from machine import Pin, I2C
import ssd1306

# 1. Set up the I2C communication on the pins we just wired
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# 2. Tell the ESP32 the size of our screen (128 pixels wide, 64 pixels high)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 3. Clear the screen (fill it with black so no random pixels are on)
oled.fill(0)

# 4. Write our test text! (The numbers are the X and Y coordinates)
oled.text("Hardware Test:", 0, 0)
oled.text("Screen is ALIVE!", 0, 20)

# 5. Push the text to the physical display
oled.show()

