from optparse import OptionParser
import json
import requests
import getpass
from  helpers import prefHelper
import config
import re
from  helpers import mqtt_server

def _parse_options():
    """
    Parse the command line arguments for script
    """
    try:
        parser = OptionParser(usage='%prog [Options]', version='1.0',)
        options, args = parser.parse_args()
        return options, args
    except Exception as e:
        print("Exception while parsing arguments: " + str(e))



options, args = _parse_options()
if len(args) == 0:
    print('please specify an action')
    exit()
    
if args[0] == 'login':
    print("Login to your alexasmarttv.tk account")
    email = input("Email: ")
    password = getpass.getpass(prompt='Password: ')
    payload ={"email": email, "password": password}
    headers = {'content-type': 'application/json'}
    response = requests.post('https://alexasmarttv.tk/api/v1/login', data=json.dumps(payload), headers=headers)
    json_data = json.loads(response.text)
    if 'error' in json_data:
        print(json_data['error']['message'])
    else:
        file = open('.auth/token','w')
        file.write(json_data['jwt'])
        file.close
        print("User successfully logged in.")
        
        
if args[0] == 'register':
    if not prefHelper.loggedIn():
        print('Error: please log in before registering device.')
    else:
        print("Registering device...")
        payload ={"name": config.device_name, "tvs": len(config.tvs)}
        reregister = False
        if prefHelper.deviceRegistered():
            payload['uuid'] = prefHelper.deviceUUID()
            reregister = True
            
        headers = {'content-type': 'application/json', 'jwt': prefHelper.deviceToken()}
        
        response = requests.post('https://alexasmarttv.tk/api/v1/register_device', data=json.dumps(payload), headers=headers)
        json_data = json.loads(response.text)
        if 'error' in json_data:
            print(json_data['error']['message'])
        else:
            file = open('.auth/uuid','w')
            file.write(json_data['uuid'])
            file.close
            
            file = open('.auth/private.pem.key','w')
            file.write(json_data['private_key'])
            file.close
            
            file = open('.auth/certificate.pem.crt','w')
            file.write(json_data['pubic_certificate'])
            file.close
            if reregister:
                print("device successfully reregistered.")
            else:
                print("device successfully registered.")
            
            
if args[0] == 'setup_cable':
    print("Setting up your cable.")
    zipcode = input("Enter Zipcode: ")
    response = requests.get('https://mobilelistings.tvguide.com/Listingsweb/ws/rest/serviceproviders/zipcode/' + zipcode + '?formattype=json')
    providerlist = []
    index = 0
    print("Providers found in your area: ")
    
    for provider in json.loads(response.text):
        for device in provider["Devices"]:
            print(str(index+1) + ') ' + provider["Name"] + ("" if device["DeviceName"] == "" else "   (" +  device["DeviceName"] + ")"))
            providerlist.append((str(provider["Id"]) + '.' + str(device["DeviceFlag"]), provider["Name"], device["DeviceName"], provider["Type"]))
            index +=1
    selection = input("Select provider: ")
    response = requests.get("http://mobilelistings.tvguide.com/Listingsweb/ws/rest/schedules/" + providerlist[int(selection)-1][0] + "/start/0/duration/1?ChannelFields=Name,FullName,Number&formattype=json&disableChannels=music,ppv,24hr&ScheduleFields=ProgramId")
    lineup = {}
    for channel in json.loads(response.text):
        full = channel["Channel"]["FullName"]
        regex = re.compile('\(.+?\)')
        full = regex.sub('', full).lower()
        full = full.replace('&','and')

        pattern = re.compile('([^\s\w]|_)+')
        full = pattern.sub('', full)

        name = channel["Channel"]["Name"].lower()
        name = pattern.sub('', name)

        num = channel["Channel"]["Number"] 

        if " hdtv" in full or " hd" in full:
            full = full.replace(' hdtv','')
            full = full.replace(' hd','')
            full = full.strip()
            if name.endswith("hd"):
                name = name[:-2]
            elif name.endswith("d"):
                name = name[:-1]
            name = name.strip()
            
            if full in lineup and lineup[full][3] == None:
                lineup[full] = (lineup[full][0],lineup[full][1],lineup[full][2],num)
            elif full not in lineup:
                lineup[full] = (name,full,None,num)
        else:
            full = full.strip()
            name = name.strip()
            if full in lineup and lineup[full][2] == None:
                lineup[full] = (lineup[full][0],lineup[full][1],num,lineup[full][3])
            elif full not in lineup:
                lineup[full] = (name,full,num,None)
                 
    sortedlist = sorted(lineup.values(), key=lambda x: (int(x[2]) if x[2] is not None else int(x[3])))
   
    file = open('helpers/lineup.txt','w')
   
    for value in sortedlist:
        file.write(str(value) + '\n')
    file.close
    print("Successfully downloaded channel listings")



if args[0] == 'start':
   mqtt_server.startServer()