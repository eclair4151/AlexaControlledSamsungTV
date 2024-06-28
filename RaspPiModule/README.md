# Amazon has stopped providing AWS credits to offset the cost of running Alexa Services. As such, this project has been deprecated/archived and servers shut down.
## The backend code and lambda calls have also been published to allow anyone to host this on thier own, but most of the code is outdated by now, and you can achieve the same result with Home Assistant.
https://www.zdnet.com/article/amazon-plans-to-stop-giving-free-aws-credits-and-paying-developers-to-make-alexa-apps/
<br /><br /><br /><br /><br /><br />
     
# Original documentation for this service is listed below
# The instructions below will no longer work, as most of the code in the project is not set up to use a self hosted domain or lambda function. As such a fair amount of work would be needed to correctly link every thing back together if you actually wanted to self host this such as setting up AWS IoT cert permissions, redirecting all lambda calls and api references in the code to point to your own, etc. 
## Connecting your Samsung Smart TV to Alexa
This tool allows you to connect your Samsung Smart TV to alexa, by using a rasberry pi. To see a full writeup of how this works see: https://drive.google.com/open?id=1uSn3TrIsmUn8I4OfTDpgXExMafl71EGzi0hFydTTWWo

## To run you will need Python3 with the following pip packages installed
 
websocket-client<br>     
AWSIoTPythonSDK<br>     
requests

## Setup

First you will need an online account. Create one at https://alexasmarttv.dev
Then clone this project onto your raspberryPi

Then turn on your TV and run the following commands to get up and running

```
python3 alexasmartcli.py scan
```

It should output the ip, mac address, and model.    
put those into the tvconfig.py file. The tvconfig should be in this format: 
```
device_name = "Home Raspberry PI" #What shows up under devices in alexasmarttv.dev. not that important unless you have multiple devices (not tvs) on your account
volume_step_size = 10  #how much your tv volume should go up by when you say 'Alexa, turn up the volume on my tv'


tvs = [
    {
        'host': ".....", #ip address of tv
        'tv_model' : '....',
        'tv_mac_address': "....",
        'tv_name' : 'TV', #Leave as TV to refrence this by just 'TV'. ex: 'Alexa, turn on the TV'.  Change to eg:'Kitchen TV' if you want to say 'Alexa turn on the kitchen TV', You cannot have multiple tvs have the same name
        'prefer_HD': True, #if you say 'change the channel to ESPN',  always attempt to use the HD channel number'
    },
    {
      #TV2....
    },
    {
       #TV3.... 
    }
    
]
```


Then run:

```
python3 alexasmartcli.py login
python3 alexasmartcli.py register (you will need to run this command anytime you change/add/remove a tv from tvconfig)
python3 alexasmartcli.py setup_cable (optional and only currently works in the US)
python3 alexasmartcli.py start (run with -m to mute the output)
```

to run this server in the backround automatically when your pi boots up place this line in your /etc/rc.local file (before the exit line):
```
python3 /PATH/TO/FOLDER/alexasmartcli.py start -m &&
```

Then just install the Alexa smart skill (Unofficial Samsung SmartTV Controller), discover devices and you will be on your way.
<br>
<br>
Link to alexa skill: https://www.amazon.com/dp/B07886XNK8
<br>
<br>
Tutorial:<br>
[![Alexa Setup Tutorial](https://img.youtube.com/vi/-uhd33FiEUM/0.jpg)](https://www.youtube.com/watch?v=-uhd33FiEUM)

### Currently supported commands:
* Alexa turn on the TV    (Only supported on K,M, and QLED TVS (2016 and newer))
* Alexa turn off the TV

* Alexa (un)mute the TV
* Alexa turn up/down the volume on TV

* Alexa change the channel to 25 on the TV
* Alexa change the channel to ESPN on the TV

* Alexa Play/Pause/Stop the TV
<br>
<br>

## Setting up your own channel mappings for unsupported countries/zipcodes:<br>
I currently pull all channel mappings from http://www.tvguide.com/Listings/
but if your tv provider/zipcode isnt on there you can still set it up manually:
<br>
* Create a file inside the helpers folder called lineup.json.
* inside you should put the channels in the following format:
```
[
  ["espn", "espn", "2", "502"], 
   ["dsc", "discovery", "120", "620"], 
   ... 
   ["fs1", "fox sports one", "83", "583"]
]
```
The first item the channel id like dsc or hgtv. 
The 2nd is the full channel name,
The 3rd is the nonhd channel num 
The 4th is the hd channel num. 

You can leave any the items that don’t apply empty/set to 0<br>
In many cases like ESPN the channel id and full name will be the same<br>
It is also important to note that that the channel id and name are completely arbitrary and can be named anything you want 
to, to tell alexa to change the channel, Eg: alexa change the channel to unicorn on my tv.<br><br>
Just note that in the full channel name to use spelled out numbers if it applies, Eg: Fox Sports One NOT Fox Sports 1


## Troubleshooting:    
if nothing seems to happen these are some steps you can take to debug:

* start the server without the -m option and ask alexa to mute the tv. If nothing appears in the output there was an error linking the alexa skill. This can happen if you reregister a pi but dont relogin to you account in the device linking. go the the alexa app, disable this skill and reenable to correctly link them  

* if the command appears in the output but doesnt control the tv your tvconfig file is incorrect. make sure you have put the correct IP address and model number. You can also try running the [Samsungctl](https://github.com/Ape/samsungctl) library directly to make sure you have the correct settings

* if discovering TVs through the Alexa app does not discover the tvs correctly try running python3 alexasmartcli.py register and restarting the server. Then try to rediscover your tvs.

* if when starting the server you get the following error
```
File "/usr/lib/python3.5/socket.py", line 733, in getaddrinfo
for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -2] Name or service not known
```
This is a known issue of the Mqtt library i use<br>
https://github.com/aws/aws-iot-device-sdk-python/issues/192<br>
The fix is to set the DNS provider of your raspi to 8.8.8.8, 8.8.4.4<br>
https://pimylifeup.com/raspberry-pi-dns-settings/


## Disclaimer:
1) H and J series TVs are currently unsupported but are being worked on to support it. There is an experimental fork to add support if you would like to give it a try: https://github.com/bencarlisle15/AlexaControlledSamsungTV

2) If you have a cable box, in order to change the channel the alexa sends a command to the smart remote which sends it back to the cable box over RF. Because of this for the command 'alexa change the channel' to work the remote needs to have line of sight with the cable box

