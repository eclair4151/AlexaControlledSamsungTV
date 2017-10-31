from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")



myMQTTClient = AWSIoTMQTTClient("1234")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint("afkx1f9takwol.iot.us-east-1.amazonaws.com", 8883)
# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
myMQTTClient.configureCredentials("certs/root.pem", "certs/private.pem.key", "certs/certificate.pem.crt")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec




myMQTTClient.connect()
#myMQTTClient.publish("myTopic", "myPayload", 0)
myMQTTClient.subscribe("turnon/1", 1, customCallback)
#myMQTTClient.unsubscribe("myTopic")
#myMQTTClient.disconnect()


while True:
    time.sleep(1)