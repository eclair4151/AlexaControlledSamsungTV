# AlexaControlledSamsungTV
This is a python server to enable you to control your samsung tv via the amazon alexa (or any other thing that can make rest requests).        

it should support  both pre-2016 TVs as well most of the modern Tizen-OS TVs with Ethernet or Wi-Fi connectivity.    


to run you will need python3 with the following installed
samsungctl
websocket-client-py3
flask


then in your config.py set the ip (i would recommend setting a static ip for it in your router)and mac address of your tv

for everything else go to
https://github.com/Ape/samsungctl
to figure out what to put

then run the flash app and your good to go