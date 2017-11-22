from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from helpers.pywakeonlan import send_magic_packet
import samsungctl
import tvconfig
import json
import requests
from helpers import prefHelper
import math
from difflib import get_close_matches


remote_config = {
    "name": "samsungctl",
    "description": "PC",
    "id": "",
    "host": tvconfig.tvs[0]['host'],
    "port": tvconfig.tvs[0]['port'],
    "method": tvconfig.tvs[0]['method'],
    "timeout": 0,
}

tv_listings_dict = {}
tv_channels = []

def printmsg(message):
    print("\n\nReceived a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------")
    
    
def power(client, userdata, message):
    printmsg(message)
    payload = json.loads(message.payload.decode('utf-8'))

    try:
        if payload['operation'] == 'turnOn':
            send_magic_packet(tvconfig.tvs[0]['tv_mac_address'])
            time.sleep(3)
            with samsungctl.Remote(remote_config) as remote:
                remote.control("KEY_RETURN")  #get rid of the on menu when you turn the tv on
        elif payload['operation'] == 'turnOff':
            with samsungctl.Remote(remote_config) as remote:
                remote.control("KEY_POWER") 
    except:
        print("Failed to send message to TV")

   
   
   
def channel(client, userdata, message):
    printmsg(message)
    payload = json.loads(message.payload.decode('utf-8'))
    try:
        if payload['operation'] == 'ChangeChannel':
            if 'number' in payload['channel_data']['channel']:
                with samsungctl.Remote(remote_config) as remote:
                    for c in payload['channel_data']['channel']['number']:
                        remote.control("KEY_" + str(c))
                        time.sleep(0.25)
                    remote.control("KEY_ENTER")
                    
            else: 
                channel_name = ''
                if 'callSign' in payload['channel_data']['channel']:
                    channel_name = payload['channel_data']['channel']['callSign']
                elif 'affiliateCallSign' in payload['channel_data']['channel']:
                    channel_name = payload['channel_data']['channel']['affiliateCallSign']
                elif 'channelMetadata' in payload['channel_data'] and 'name' in payload['channel_data']['channelMetadata']:
                    channel_name = payload['channel_data']['channelMetadata']['name']

                with samsungctl.Remote(remote_config) as remote:
                    res = get_close_matches(channel_name.lower().replace('&','and').replace('the ','').replace(' channel',''), tv_channels)
                    if len(res) > 0:
                        chan = tv_listings_dict[res[0]]
                        num = ""
                        if chan[3] != None and tvconfig.prefer_HD:
                            num = str(chan[3])
                        else:
                            num = str(chan[2])
                        print(channel_name + ':   closest match - ' + res[0] + '     -  ' + str(num))
                        for c in payload['channel']['number']:
                            remote.control("KEY_" + str(c))
                            time.sleep(0.25)
                        remote.control("KEY_ENTER") 
                        
                    
        elif payload['operation'] == 'SkipChannels':
            steps = payload['channelCount']
            chandown = steps < 0
            steps = math.fabs(steps)
            
            for i in range(0,steps):
                with samsungctl.Remote(remote_config) as remote:
                    remote.control("KEY_CHDOWN" if chandown else "KEY_CHUP") 
                    time.sleep(0.25) #delay for volume 
    except:
        print("Failed to send message to TV")



def speaker(client, userdata, message):
    printmsg(message)
    payload = json.loads(message.payload.decode('utf-8'))

    try:
        if payload['operation'] == 'SetMute':
            with samsungctl.Remote(remote_config) as remote:
                remote.control("KEY_MUTE") 
        elif payload['operation'] == 'AdjustVolume':
            steps = payload['volumeSteps']
            voldown = steps < 0
            steps = math.fabs(steps)
            
            if steps == 1:
                steps = tvconfig.volume_step_size
            
            for i in range(0,steps):
                with samsungctl.Remote(remote_config) as remote:
                    remote.control("KEY_VOLDOWN" if voldown else "KEY_VOLUP") 
                    time.sleep(0.25) #delay for volume
    except:
        print("Failed to send message to TV")
        

def playback(client, userdata, message):
    printmsg(message)
    payload = json.loads(message.payload.decode('utf-8'))

    try:
        if payload['operation'] == 'Pause' or payload['operation'] == 'Stop':
            with samsungctl.Remote(remote_config) as remote:
                remote.control("KEY_PAUSE")
        elif payload['operation'] == 'Play':
            with samsungctl.Remote(remote_config) as remote:
                remote.control("KEY_PLAY") 
    except:
        print("Failed to send message to TV")





def startServer():
    
    global tv_listings_dict
    global tv_channels

    with open('helpers/lineup.json') as json_data:
        tv_json = json.load(json_data)
        for chan in tv_json:
            tv_channels.append(chan[0])
            tv_channels.append(chan[1])
            tv_listings_dict[chan[0]] = chan
            tv_listings_dict[chan[1]] = chan

    
    
    clientid = prefHelper.deviceUUID()
    myMQTTClient = AWSIoTMQTTClient(clientid)
    myMQTTClient.configureEndpoint("afkx1f9takwol.iot.us-east-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials(".auth/root.pem", ".auth/private.pem.key", ".auth/certificate.pem.crt")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    print('starting server...')
    myMQTTClient.connect()
    
    myMQTTClient.subscribe("power/" + clientid, 1, power)
    myMQTTClient.subscribe("channel/" + clientid, 1, channel)
    myMQTTClient.subscribe("speaker/" + clientid, 1, speaker)
    myMQTTClient.subscribe("playback/" + clientid, 1, playback)

    #myMQTTClient.unsubscribe("myTopic")
    #myMQTTClient.disconnect()
    print('server running. Pres CTRL + C to stop')

    counter = 0
    while True:
        time.sleep(1)
        if counter == 0:
            payload ={"uuid": prefHelper.deviceUUID()}
            headers = {'content-type': 'application/json', 'jwt': prefHelper.deviceToken()}
            response = requests.post('https://alexasmarttv.tk/api/v1/ping', data=json.dumps(payload), headers=headers)
            
        counter += 1
        counter = counter%900
