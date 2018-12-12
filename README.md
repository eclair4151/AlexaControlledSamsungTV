## WARNING. As of 10/25/18 Samsung has pushed a firmware upgrade to many TVs that disables the websocket api that this program uses. 
## The fix has been issued. You will need to go into the directory you cloned this repo in and run git pull. Then restart the server

## To run you will need Python3 with the following pip packages installed
 
websocket-client<br>     
AWSIoTPythonSDK<br>     
requests

## Setup

First you will need an online account. Create one at alexasmarttv.tk
Then clone this project onto your raspberryPi

Then turn on your TV and run the following commands to get up and running

```
python3 alexasmartcli.py scan
```

It should output the ip, mac address, and model.    
put those into the tvconfig.py file. The tvconfig should be in this format: 
```
device_name = "Home Raspberry PI" #What shows up under devices in alexasmarttv.tk. not that important unless you have multiple devices (not tvs) on your account
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

## Disclaimer:
1) H and J series TVs are currently unsupported but are being worked on to support it

2) If you have a cable box, in order to change the channel the alexa sends a command to the smart remote which sends it back to the cable box over RF. Because of this for the command 'alexa change the channel' to work the remote needs to have line of sight with the cable box

