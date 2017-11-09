from optparse import OptionParser
import json
import requests
import getpass
import prefHelper
import config

def _parse_options():
    """
    Parse the command line arguments for script
    """
    try:
        parser = OptionParser(usage='%prog [Options]', version='1.0',)
        parser.add_option(
            '-l', '--location',
            dest='location',
            help='Location of the new server folder'
            )

        parser.add_option(
            '-s', '--snapshot',
            action="store_true",
            default=False,
            dest='snapshot',
            help='Whether the server should download a snapshot'
        )

        parser.add_option(
            '', '--start',
            dest='start',
            action="store_true",
            default=False,
            help='Start the server once its created'
        )

        options, args = parser.parse_args()
        return options, args
    except Exception as e:
        print("Exception while parsing arguments: " + str(e))



options, args = _parse_options()
if args[0] == 'login':
    print("Login to your alexasmarttv.tk account")
    email = input("Email: ")
    password = getpass.getpass(prompt='Password: ')
    payload ={"email": email, "password": password}
    headers = {'content-type': 'application/json'}
    response = requests.post('https://alexasmarttv.tk/api/v1/login', data=json.dumps(payload), headers=headers, verify=False) #verify is not working WTF
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
        payload ={"name": config.device_name, "tvs": 1}
        if prefHelper.deviceRegistered():
            payload['uuid'] = prefHelper.deviceUUID()
            
        headers = {'content-type': 'application/json', 'jwt': prefHelper.deviceToken()}
        
        response = requests.post('https://alexasmarttv.tk/api/v1/register_device', data=json.dumps(payload), headers=headers, verify=False) #verify is not working WTF
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
            
            print("device successfully registered.")