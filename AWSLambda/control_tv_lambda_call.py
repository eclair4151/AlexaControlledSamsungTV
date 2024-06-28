
from __future__ import print_function

import json
from uuid import uuid4
import urllib.request
import urllib.parse
import jwt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import random, string
import requests


ALEXA_REQUEST_DISCOVER = "Alexa.Discovery"
ALEXA_REQUEST_POWER = "Alexa.PowerController"
ALEXA_REQUEST_CHANNEL = "Alexa.ChannelController"
ALEXA_REQUEST_STEP_SPEAKER = "Alexa.StepSpeaker"
ALEXA_REQUEST_PLAYBACK = "Alexa.PlaybackController"
JWT_PASSWORD = "ENTER_YOUR_JWT_PASSWORD"

CONTROL_TURN_ON = "TurnOn"
CONTROL_TURN_OFF = "TurnOff"
CONTROL_CHANGE_CHANNEL = "ChangeChannel"
CONTROL_SKIP_CHANNEL = "SkipChannels"
CONTROL_PLAY = "Play"
CONTROL_PAUSE = "Pause"
CONTROL_STOP = "Stop"
CONTROL_ADJUST_VOLUME = "AdjustVolume"
CONTROL_MUTE = "SetMute"


def randomId():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(15))
   
def sendMessage(topic, event, json_data):
    jwt_token = event['directive']['endpoint']['scope']['token']
    endpointid =  event['directive']['endpoint']['endpointId']
    data = jwt.decode(jwt_token, JWT_PASSWORD, algorithms=['HS256'])
    json_data["operation"] = event['directive']['header']['name']
    json_data["endpointid"] = endpointid
    print(data)
    
    myMQTTClient = AWSIoTMQTTClient(randomId(), useWebsocket=True)
    myMQTTClient.configureEndpoint("afkx1f9takwol.iot.us-east-1.amazonaws.com", 443)
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(4)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(4)
    myMQTTClient.configureCredentials("root.pem")
    myMQTTClient.configureIAMCredentials("YOUR_IAM_ACCESS_KEY", "YOUR_IAM_SECRET_KEY")
    myMQTTClient.connect()
    response = myMQTTClient.publish(topic + '/' + data['device_uuid'] , json.dumps(json_data), 0)
    myMQTTClient.disconnect()
    print(topic)

def lambda_handler(event, context):

    if event['directive']['header']['namespace'] == ALEXA_REQUEST_DISCOVER:
        return discover_device(event)

    if event['directive']['header']['namespace'] == ALEXA_REQUEST_POWER:
        return power_device(event)

    if event['directive']['header']['namespace'] == ALEXA_REQUEST_CHANNEL:
        return change_channel_device(event)

    if event['directive']['header']['namespace'] == ALEXA_REQUEST_STEP_SPEAKER:
        return step_speaker_device(event)
        
    if event['directive']['header']['namespace'] == ALEXA_REQUEST_PLAYBACK:
        return playback_device(event)
    print('un supported control request')
    return None
    
    
def discover_device(event):
    print('discover_device')
    discovered_appliances = {
        "endpoints": get_appliances(event)
    }
    return build_discover_response(event['directive']['header'], discovered_appliances)


def get_appliances(event):
    tvs = []
    
    jwt_token = event['directive']['payload']['scope']['token']
    data = jwt.decode(jwt_token, JWT_PASSWORD, algorithms=['HS256'])
    headers = {'content-type': 'application/json', 'jwt':jwt_token} 
    payload ={"uuid": data['device_uuid']}
    response = requests.post('https://alexasmarttv.dev/api/v1/get_devices', data=json.dumps(payload), headers=headers)
    json_data = json.loads(response.text)
    
    for tv in json_data['tvs']:
        tvs.append(
            {
                "endpointId": tv['mac_address'],
                "manufacturerName": "Samsung",
                "displayCategories":[ "TV"],
                "friendlyName": tv['name'],
                "description":"Samsung Smart TV",
                "capabilities": [
                    {
                         "type":"AlexaInterface",
                         "interface":ALEXA_REQUEST_STEP_SPEAKER,
                         "version":"1.0",
                         "properties":{
                            "supported":[
                               {
                                  "name":CONTROL_ADJUST_VOLUME,
                               },
                               {
                                  "name":CONTROL_MUTE
                               }
                            ]
                         }
                      },
                      {
                         "type":"AlexaInterface",
                         "interface":ALEXA_REQUEST_CHANNEL,
                         "version":"1.0",
                         "properties":{
                            "supported":[
                               {
                                  "name":CONTROL_CHANGE_CHANNEL
                               },
                               {
                                   "name":CONTROL_SKIP_CHANNEL
                               }
                            ]
                         }
                      },
                      {
                         "type":"AlexaInterface",
                         "interface":ALEXA_REQUEST_POWER,
                         "version":"1.0",
                         "properties":{
                            "supported":[
                               {
                                  "name":CONTROL_TURN_OFF
                               },
                               {
                                   "name": CONTROL_TURN_ON
                               }
                            ]
                         }
                      },
                      {
                         "type":"AlexaInterface",
                         "interface":ALEXA_REQUEST_PLAYBACK,
                         "version":"1.0",
                         "properties":{
                            "supported":[
                               {
                                    "name":CONTROL_PLAY
                               },
                               {
                                   "name": CONTROL_PAUSE
                               },
                               {
                                   "name": CONTROL_STOP
                               }
                            ]
                         }
                      }
                ],
                "additionalApplianceDetails": {}
            }
        )
    return tvs
    
    
def build_discover_response(event_header, discovered_appliances):
    header = {
        "payloadVersion": event_header['payloadVersion'],
        "namespace": event_header['namespace'],
        "name": "Discover.Response",
        "messageId": str(uuid4())
    }
    response = {
        "event": {
        "header": header,
        "payload": discovered_appliances
        }
    }

    return response
    
    
def power_device(event):
    print('power_device')
    value = ""
    
    if event['directive']['header']['name'] == CONTROL_TURN_ON:
        sendMessage('power',event,{})
        value = "ON"
        
    if event['directive']['header']['name'] == CONTROL_TURN_OFF:
        sendMessage('power',event,{})
        value = "OFF"
    
    properties = [{
      "namespace": ALEXA_REQUEST_POWER,
      "name": "powerState",
      "value": value,
      "uncertaintyInMilliseconds": 500
    }]

    return build_control_response(event, properties)
    
def change_channel_device(event):
    print('channel')
    value = ""
    
    if event['directive']['header']['name'] == CONTROL_CHANGE_CHANNEL:
        sendMessage('channel',event,{"channel_data": event['directive']['payload']})
        value = event['directive']['payload']['channel']
        
    if event['directive']['header']['name'] == CONTROL_SKIP_CHANNEL:
        sendMessage('channel',event,{"channelCount": event['directive']['payload']['channelCount']})
        value = {"channel":{"number":"1","callSign":"unknown","affiliateCallSign":"unknown"}}  #who knows what channel we are on
    
    properties = [{
      "namespace": ALEXA_REQUEST_CHANNEL,
      "name": "channel",
      "value": value,
      "uncertaintyInMilliseconds": 500
    }]

    return build_control_response(event, properties)

def step_speaker_device(event):
    print('speaker')

    if event['directive']['header']['name'] == CONTROL_MUTE:
        sendMessage('speaker',event,{})

    if event['directive']['header']['name'] == CONTROL_ADJUST_VOLUME:
        sendMessage('speaker',event,{"volumeSteps": event['directive']['payload']['volumeSteps']})

    properties = []

    return build_control_response(event, properties)
    
def playback_device(event):
    print('playback')

    if event['directive']['header']['name'] == CONTROL_PLAY or event['directive']['header']['name'] == CONTROL_PAUSE or event['directive']['header']['name'] == CONTROL_STOP:
        sendMessage('playback',event,{})

    properties = []

    return build_control_response(event, properties)
    
def build_control_response(event, properties):
    response = {"event" :{
                    "header": {
                        "namespace":"Alexa",
                        "messageId": str(uuid4()),
                        "name": "Response",
                        "payloadVersion": event['directive']['header']['payloadVersion'],
                        "correlationToken": event['directive']['header']['correlationToken']
                    },
                    "endpoint":event["directive"]["endpoint"],
                    "payload": {}
                },
                "context":{"properties": properties}
    }


    return response