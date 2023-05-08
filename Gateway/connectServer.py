from Adafruit_IO import MQTTClient
import uart
import log
import sys

clientInfo = open("./client_info.txt", "r")
AIO_FEED_IDs = ["nutnhan1", "nutnhan2", "cambien1", "cambien2", "mcu_info", "sending_freq", "error_detect"]
AIO_USERNAME = clientInfo.readline().strip()
AIO_KEY = clientInfo.readline().strip()

def connected(client):
    for feed in AIO_FEED_IDs:
        client.subscribe(feed)
    
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed...")

def disconnected(client):
    print("Disconnected...")
    sys.exit (1)

def message(client , feed_id , payload):
    if feed_id == "nutnhan1":
        if payload == "0":
            uart.writeData("@OFF1*")
        else:
            uart.writeData("@ON1*")
    if feed_id == "nutnhan2":
        if payload == "0":
            uart.writeData("@OFF2*")
        else:
            uart.writeData("@ON2*")
    if feed_id == "sending_freq":
        print("New Operating Cycle: " + payload)
        uart.setProcDelay(int(payload))
        uart.writeData("@F:" + str(payload) + ":" + "*")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
try: 
    client.connect()
except:
    print("Internet Connection Loss...")
    log.writelog("Internet Connection Loss...")
    sys.exit(1)
client.loop_background()