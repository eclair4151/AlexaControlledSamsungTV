from optparse import OptionParser
import json
import requests
import getpass
from  helpers import prefHelper
import tvconfig
import re
from  helpers import mqtt_server
import os
from helpers.ssdp import scan_network_ssdp

url = "https://alexasmarttv.dev"
def _parse_options():
    """
    Parse the command line arguments for script
    """
    try:
        parser = OptionParser(usage='%prog [Options]', version='1.0',)
        parser.add_option("-m", "--mute", action="store_true", dest="mute")

        options, args = parser.parse_args()
        return options, args
    except Exception as e:
        print("Exception while parsing arguments: " + str(e))



options, args = _parse_options()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if len(args) == 0:
    print('please specify an action')
    exit()
    
if args[0] == 'login':
    print("Login to your alexasmarttv.dev account")
    email = input("Email: ")
    password = getpass.getpass(prompt='Password: ')
    payload ={"email": email, "password": password}
    headers = {'content-type': 'application/json'}
    response = requests.post(url + '/api/v1/login', data=json.dumps(payload), headers=headers)
    json_data = json.loads(response.text)
    if 'error' in json_data:
        print(json_data['error']['message'])
    else:
        file = open('.auth/token','w')
        file.write(json_data['jwt'])
        file.close()
        print("User successfully logged in.")


if args[0] == 'scan':
    print('Scanning for TVs. make sure they are turned on and on the same network')
    tvs = scan_network_ssdp(True, wait=2)
    if len(tvs) == 0:
        print('No TVs found')

if args[0] == 'reset':
    os.remove('.auth/uuid')
    os.remove('.auth/token')
    os.remove('.auth/private.pem.key')
    os.remove('.auth/certificate.pem.crt')
    print("Reset device. you will now need to relogin and register this device")
    
        
if args[0] == 'register':
    if not prefHelper.loggedIn():
        print('Error: please log in before registering device.')
    else:
        print("Registering device...")
        tvs = []
        for tv in tvconfig.tvs:
            tvs.append({'name':tv['tv_name'], 'mac_address': tv['tv_mac_address']})
            
        payload ={"name": tvconfig.device_name, "tvs": tvs}
        reregister = False
        if prefHelper.deviceRegistered():
            payload['uuid'] = prefHelper.deviceUUID()
            reregister = True
            
        headers = {'content-type': 'application/json', 'jwt': prefHelper.deviceToken()}
        
        response = requests.post(url + '/api/v1/register_device', data=json.dumps(payload), headers=headers)
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
    zipcode = input("Enter Zipcode (Leave empty to skip this step if it does not work or you are outside the US): ")
    if zipcode != '':
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
            full = full.replace('the ', '')
            full = full.replace(' channel', '')
    
    
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
        sortedlist = sorted(lineup.values(), key=lambda x: (float(x[2]) if x[2] is not None else float(x[3])))
       
        with open('helpers/lineup.json', 'w') as outfile:
            json.dump(sortedlist, outfile)
        #for value in sortedlist:
        #file.write(json.dumps(sortedlist))
        #file.close
        print("Successfully downloaded channel listings")
    else:
         with open('helpers/lineup.json', 'w') as outfile:
             outfile.write('[]')
             


if args[0] == 'start':
    if not prefHelper.loggedIn():
        print('Error: please log in before starting server.')
    else:
        mqtt_server.startServer(options.mute)


