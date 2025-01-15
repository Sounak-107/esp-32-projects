import umqtt.simple 
import machine
import time
import network


#wifi credentials
ssid= "DEVICE'S identifier"
password="PASSWORD"

#creat station interface object
wifi = network.WLAN(network.STA_IF)

#activate the station interface
wifi.active(True)

#connect to the wifi network
wifi.connect(ssid,password)

#wait until the connection is establish
max_attempts= 10
attempts=0
while not wifi.isconnected() and attempts < max_attempts:
    print("Connecting to wifi network.....")
    time.sleep(1)
    attempts+=1
    
if wifi.isconnected():
    print("Connected to the wifi network ")
    print(f"Network configuration: {wifi.ifconfig()}")
else:
    print("Failed to connect, check the connection again")
    


# MQTT broker details
BROKER = 'broker.hivemq.com'  # Replace with your broker's address
PORT = 1883
TOPIC = 'home/led/s1975b'   # Topic to subscribe to

# Initialize the onboard LED
led = machine.Pin(2, machine.Pin.OUT)  # GPIO 2 is typically used for the onboard LED on ESP32

# MQTT callback function for messages
def message_callback(topic, msg):
    print("Received message:", msg.decode())
    a= float(msg.decode())
    running = True
    if a == 'ON':
        led.on()         # Turn the LED on
    elif a == 'OFF':
        led.off()        # Turn the LED off
    elif a=='BLINK' and running == True:
        b=1              # To Blink the Inbuild LED 10 Times
        while b<=10 and running == True:
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
            
            b+=1
    else :
        print("DHANUPISI KOTHAKAR, BESI MOJA PEYE GECHO NA! JANOWAAR LOKJON SOB!!")
# Create an MQTT client instance
client =umqtt.simple.MQTTClient("esp32_led_controller",BROKER, PORT)

# Assign the callback functions
client.set_callback(message_callback)

# Connect to the MQTT broker
client.connect()

# Subscribe to the topic
client.subscribe(TOPIC)

print(f"Subscribed to topic: {TOPIC}")

# Loop to process incoming messages
try:
    while True:
        client.check_msg()
        time.sleep(0.2)
except KeyboardInterrupt :
    print("interrupted...")
finally :
    client.disconnect()
    
    
    
    

