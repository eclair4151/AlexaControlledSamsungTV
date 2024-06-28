device_name = "Home Raspberry PI" #What shows up under devices in alexasmarttv.tk. not that important unless you have multiple devices (not tvs) on your account
volume_step_size = 10  #how much your tv volume should go up by when you say 'Alexa, turn up the volume on my tv'


tvs = [
    {
        'host': "192.168.2.111", #ip address of tv
        'tv_model' : 'UN65MU630D',
        'tv_mac_address': "68:27:37:4c:6b:1e",
        'tv_name' : 'TV', #Leave as TV to refrence this by just 'TV'. ex: 'Alexa, turn on the TV'.  Change to eg:'Kitchen TV' if you want to say 'Alexa turn on the kitchen TV', You cannot have multiple tvs have the same name
        'prefer_HD': True, #if you say 'change the channel to ESPN',  always attempt to use the HD channel number'
    }
]