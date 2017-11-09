device_name = "Home Raspberry PI"



tvs = [
    {
    'host': "Samsung.fios-router.home", #ip address of tv
    'port': 8001,
    'method': "websocket",
    'tv_mac_address': "68:27:37:4c:6b:1e",
    'tv_name' : '', #Leave blank if you like to refrence this tv on the alexa by just 'TV'. ex: 'Alexa, turn on the TV'. You cannot have multiple tvs be blank
    'prefer_HD': True, #if you say 'change the channel to ESPN',  always attempt to use the HD channel number'
    'legacy_power_off': False #turn this to true if your tv is 2015 or below
    }
]