from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from pywakeonlan import send_magic_packet
import samsungctl
from alexasmarttv import config
import json
import requests
import prefHelper

remote_config = {
    "name": "samsungctl",
    "description": "PC",
    "id": "",
    "host": config.tvs[0]['host'],
    "port": config.tvs[0]['port'],
    "method": config.tvs[0]['method'],
    "timeout": 0,
}


def printmsg(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    
def turnOn(client, userdata, message):
    printmsg(message)
    send_magic_packet(config.tvs[0]['tv_mac_address'])
    time.sleep(3)
    with samsungctl.Remote(remote_config) as remote:
        remote.control("KEY_RETURN")  #get rid of the on menu when you turn the tv on


def turnOff(client, userdata, message):
    printmsg(message)
    with samsungctl.Remote(remote_config) as remote:
        remote.control("KEY_POWER")  #get rid of the on menu when you turn the tv on


def mute(client, userdata, message):
    printmsg(message)
    with samsungctl.Remote(remote_config) as remote:
        remote.control("KEY_MUTE")  #get rid of the on menu when you turn the tv on





def startServer():
    clientid = prefHelper.deviceUUID()

    myMQTTClient = AWSIoTMQTTClient(clientid)
    myMQTTClient.configureEndpoint("afkx1f9takwol.iot.us-east-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials(".auth/root.pem", ".auth/private.pem.key", ".auth/certificate.pem.crt")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    
    myMQTTClient.connect()
    myMQTTClient.subscribe("turnon/" + clientid, 1, turnOn)
    myMQTTClient.subscribe("turnoff/" + clientid, 1, turnOff)
    myMQTTClient.subscribe("mute/" + clientid, 1, mute)

    #myMQTTClient.publish("myTopic", "myPayload", 0)
    #myMQTTClient.unsubscribe("myTopic")
    #myMQTTClient.disconnect()
    
    counter = 0
    while True:
        time.sleep(1)
        if counter == 0:
            payload ={"uuid": prefHelper.deviceUUID()}
            headers = {'content-type': 'application/json', 'jwt': prefHelper.deviceToken()}
            response = requests.post('https://alexasmarttv.tk/api/v1/ping', data=json.dumps(payload), headers=headers, verify=False)
            
        counter += 1
        counter = counter%900
