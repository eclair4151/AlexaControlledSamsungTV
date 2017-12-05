#   Copyright 2014 Dan Krause, Python 3 hack 2016 Adam Baxter
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import http.client
import io
import socket
import re
import urllib.request
import xml.etree.ElementTree as ET
import requests


class SSDPResponse(object):
    class _FakeSocket(io.BytesIO):
        def makefile(self, *args, **kw):
            return self

    def __init__(self, response):
        r = http.client.HTTPResponse(self._FakeSocket(response))
        r.begin()
        self.location = r.getheader("location")
        self.usn = r.getheader("usn")
        self.st = r.getheader("st")
        self.cache = r.getheader("cache-control").split("=")[1]

    def __repr__(self):
        return "<SSDPResponse({location}, {st}, {usn})>".format(
            **self.__dict__)


def discover(service, timeout=5, retries=1, mx=3):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}',
        'MAN: "ssdp:discover"',
        'ST: {st}', 'MX: {mx}', '', ''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        message_bytes = message.format(
            *group, st=service, mx=mx).encode('utf-8')
        sock.sendto(message_bytes, group)

        while True:
            try:
                response = SSDPResponse(sock.recv(1024))
                responses[response.location] = response
            except socket.timeout:
                break
    return list(responses.values())



def scan_network_ssdp(verbose, wait=0.3):
    try:
        tv_list = []
        tvs_found = discover(
            "urn:samsung.com:device:RemoteControlReceiver:1",
            timeout=wait)
        for tv in tvs_found:
            info = getTVinfo(tv.location)
            tv_list.append(info)


            print(
                '\n\nName: ' + info['fn'] +
                "\nModel: " +
                info['model'] +
                '\nSeries: ' + info['model'][4] +
                "\nIp: " +
                info['ip'] +
                '\nMacAddress: ' + info['mac_address'])
        return tv_list

    except KeyboardInterrupt:
       print('Search interrupted by user')


def namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def getTVinfo(url):
    ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    xmlinfo = urllib.request.urlopen(url)
    xmlstr = xmlinfo.read().decode('utf-8')
    root = ET.fromstring(xmlstr)
    ns = namespace(root)
    fn = root.find('.//{}friendlyName'.format(ns)).text
    model = root.find('.//{}modelName'.format(ns)).text
    udn = root.find('.//{}UDN'.format(ns)).text.split(':')[1].replace('-','')
    mac_address = ''
    if model[4] < 'K':
        if model[4] == 'J' or model[4] == 'H':
            print('This TV is not currently supported')
        else:
            mac_address = ':'.join(format(s, '02x') for s in bytes.fromhex(udn[0:12]))
    else:
        resp = requests.get('http://' + ip.group(0) + ':8001/api/v2/').json()
        mac_address = resp['device']['wifiMac']
    return {'fn': fn, 'ip': ip.group(0), 'model': model, 'mac_address': mac_address}