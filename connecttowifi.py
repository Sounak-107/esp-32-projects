import network
import time

#wifi credentials
ssid= "DEVICES SSID"
password="DIVICES PASSWORD"

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
    
    
#deactivate the wifi
a = input("If you want to dissconnect the device from the wifi network \n please press the space bar once \n")  
while a==" ":
    if a == " ":
        wifi.disconnect()
        print("The divice is disconnected from the network")
        
        #Deactivate the station interface
        wifi.active(False)
        print("Wifi interface de-activated")
    else:
        print("please choose the correct alternative")
        a = input("If you want to dissconnect the device from the wifi network \n please press the space bar once")
        
