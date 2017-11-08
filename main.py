from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time


def turnOn(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")




#clientid = '61b3d4a3-efec-468c-b175-d3f0a872678c'
clientid = 'test123'

myMQTTClient = AWSIoTMQTTClient(clientid)
myMQTTClient.configureEndpoint("afkx1f9takwol.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("certs/root.pem", "certs/private.pem.key", "certs/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec




myMQTTClient.connect()
myMQTTClient.subscribe("turnon/" + clientid, 1, turnOn)

#myMQTTClient.publish("myTopic", "myPayload", 0)
#myMQTTClient.unsubscribe("myTopic")
#myMQTTClient.disconnect()


while True:
    time.sleep(1)