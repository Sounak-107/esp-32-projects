from umqtt.simple import MQTTClient
import machine
import time
import network

# Replace with your Wi-Fi network credentials
SSID = "DEVICE'S SSID"
PASSWORD = 'PASSWORD'

def connect_to_wifi(ssid, password):
    # Initialize the Wi-Fi station interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # Activate the interface

    # Check if already connected
    if wlan.isconnected():
        print('Already connected to Wi-Fi.')
        print('IP Address:', wlan.ifconfig()[0])
        return

    # Connect to the Wi-Fi network
    print('Connecting to Wi-Fi...')
    wlan.connect(ssid, password)

    # Wait for connection to establish
    timeout = 10  # Timeout period in seconds
    start_time = time.time()

    while not wlan.isconnected():
        if time.time() - start_time > timeout:
            print('Failed to connect to Wi-Fi. Check your credentials or network.')
            return
        time.sleep(1)
    
    # Connection established
    print('Connected to Wi-Fi!')
    print('IP Address:', wlan.ifconfig()[0])

# Call the function to connect
connect_to_wifi(SSID, PASSWORD)

# MQTT server details
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC ="esp32/test"

# Callback function to handle received messages
def message_callback(topic, msg):
    print("Received message:", msg.decode())

# Initialize the client
client = MQTTClient("esp32_subscriber", MQTT_BROKER, port=MQTT_PORT)

# Connect to the broker
client.connect()
if client.connect():
    print("Subscriber connected to the broker successfully...")

# Set the callback function
client.set_callback(message_callback)

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)
if client.subscribe(MQTT_TOPIC):
    print("Waiting for message....")

while True:
    # Check for new messages
    client.check_msg()
    time.sleep(1)
