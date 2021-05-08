#
# DDNS Updater
# 
# Update Dynamic DNS for Google Domains
#
# https://github.com/tamusiunas/ddnshostupdater
# 
# by Fabricio Tamusiunas 
# 

import argparse
import logging
import time
import http.client
from base64 import b64encode
import json
import os
import urllib

class GoogleDDNS:
    
    __host_name = ""
    __username_host = ""
    __password_host = ""
    __logging = b""

    def __init__(self, host_name, username_host, password_host, logging):
        self.__host_name = host_name
        self.__username_host = username_host
        self.__password_host = password_host
        self.__logging = logging
    
    def getCurrentTimeInMillis(self):
        return round(time.time() * 1000)

    def updateIP(self, ipAddress):

        stringUrl = "domains.google.com" 
        stringGet = "/nic/update?hostname=" + self.__host_name + "&myip=" + ipAddress.decode("utf-8")

        userAndPassStr = self.__username_host + ":" + self.__password_host
        userAndPassB64 = b64encode(str.encode(userAndPassStr)).decode("ascii")

        conn = http.client.HTTPSConnection(stringUrl)
        headers = {
        "Accept": "text/html",
        "User-Agent": "DDNSUpdater / http://github.com/tamusiunas/ddnshostupdater",
        "Authorization" : "Basic %s" % userAndPassB64
        }
      
        conn.request("GET", stringGet,"",headers)
        googleResponse = conn.getresponse()
        googleResponseRead = googleResponse.read()
        if (googleResponseRead.decode("utf-8") == "badauth"):
            self.__logging.error("Authentication error. Check the username and password.");
            conn.close()
            os._exit(1)
        elif (googleResponseRead.decode("utf-8") == "nohost"):
            self.__logging.error("Host %s not configured as Dynamic DNS at Google.", self.__host_name);
            conn.close()
            os._exit(1)
        elif (googleResponseRead.decode("utf-8") == "notfqdn"):
            self.__logging.error("Host %s is not a FQDN (Full Qualified Domain Name).", self.__host_name);
            conn.close()
            os._exit(1)
        self.__logging.info("Host %s updated to %s. Response: %s", self.__host_name, ipAddress.decode("utf-8"), googleResponseRead.decode("utf-8"))
        conn.close()

class ParseConfig:
    __configFile = ""
    __host_name = ""
    __username_host = ""
    __password_host = ""
    __ipVersion = 4
    __logging = b""
    __envVars = b""

    def __init__(self, configFile, envVars, logging):
        self.__configFile = configFile
        self.__logging = logging
        self.__envVars = envVars
        self.readConfig()
    
    def readConfig(self):
        self.__host_name = self.__envVars.get("host_name")
        self.__username_host = self.__envVars.get("username_host")
        self.__password_host = self.__envVars.get("password_host")
        self.__ipVersion = self.__envVars.get("ip_version")
        if (self.__configFile != None):
            try:
                with open(self.__configFile, "r") as jsonfile:
                    try:
                        jsonData = json.load(jsonfile)
                    except ValueError as err:
                        self.__logging.error("Config file %s is not valid", self.__configFile)
                        os._exit(1)
                    print (jsonData)
                    if (self.__host_name == None): self.__host_name = jsonData.get("host_name")
                    if (self.__username_host == None): self.__username_host = jsonData.get("username_host")
                    if (self.__password_host == None): self.__password_host = jsonData.get("password_host")
                    if (self.__ipVersion == None): self.__ipVersion = jsonData.get("ip_version")
            except FileNotFoundError as err:
                self.__logging.error("Config file %s not found", self.__configFile)
                os._exit(1)
        if (self.__host_name == None):
            self.__logging.error("Key \"host_name\" not found in config file or environment var HOST_NAME")
            os._exit(1)
        if (self.__username_host == None):
            self.__logging.error("Key \"username_host\" not found in config file or environment var USERNAME_HOST")
            os._exit(1)
        if (self.__password_host == None):
            self.__logging.error("Key \"password_host\" not found in config file or environment var PASSWORD_HOST")
            os._exit(1)
        if (self.__host_name == ""):
            self.__logging.error("Key \"host_name\" is empty in config file or environment var HOST_NAME is empty")
            os._exit(1)
        if (self.__username_host == ""):
            self.__logging.error("Key \"username_host\" is empty in config file or environment var USERNAME_HOST is empty")
            os._exit(1)
        if (self.__password_host == ""):
            self.__logging.error("Key \"password_host\" is empty in config file or environment var PASSWORD_HOST is empty")
            os._exit(1)
        if ((self.__ipVersion == None) or (self.__ipVersion == "")):
            self.__logging.info("Key \"ip_version\" not found or is empty in config file or environment var IP_VERSION is empty. Assuming IPv4.")
        self.__host_name = urllib.parse.quote_plus(self.__host_name)
    
    def getHostName(self):
        return self.__host_name

    def getUsername(self):
        return self.__username_host

    def getPassword(self):
        return self.__password_host

    def getIpVersion(self):
        return self.__ipVersion

class GetIP:
  __ipv4Url = "api.ipify.org"
  __ipv6Url = "api6.ipify.org"
  IPV4 = 4
  IPV6 = 6

  def getIP(self, ipVersion):
    if (ipVersion == self.IPV4):
        conn = http.client.HTTPSConnection(self.__ipv4Url)
    elif (ipVersion == self.IPV6):
        conn = http.client.HTTPSConnection(self.__ipv6Url)
    else:
        conn = http.client.HTTPSConnection(self.__ipv4Url)
    conn.request("GET", "/")
    ipResponse = conn.getresponse()
    ip = ipResponse.read()
    conn.close()
    return (ip)

# Configure arguments
ap = argparse.ArgumentParser(description='Dynamic DNS Updater for Google Domains')
ap.add_argument("-c", "--config", required=False,
   help="configuration file")
ap.add_argument("-l", "--log-file", required=False,
   help="log file")
args = vars(ap.parse_args())

# Environment variables
envIpVersion = None
if (os.getenv('IP_VERSION') != None):
    if (os.getenv('IP_VERSION').isnumeric()):
        envIpVersion = int(os.getenv('IP_VERSION'))    
envVars = {
    "host_name": os.getenv('HOST_NAME'),
    "username_host": os.getenv('USERNAME_HOST'),
    "password_host": os.getenv('PASSWORD_HOST'),
    "ip_version": envIpVersion
}

# Configure logging
if (args["log_file"] == None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
else:
    try:
        logging.basicConfig(filename=args["log_file"], level=logging.INFO, format='%(asctime)s %(message)s')
    except:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s') 
        logging.error("Error opening log file %s" % args["log_file"])
        os._exit(1)

# Read config
parseConfig = ParseConfig(args["config"], envVars, logging)
logging.info('Starting DDNS Host Updater for Google Domains - for more information: https://github.com/tamusiunas/ddnshostupdater')
logging.info('Domain: %s', parseConfig.getHostName())

# Prepare to get IP Address
getIP = GetIP()

# Google DDNS controller
googleDDNS = GoogleDDNS(parseConfig.getHostName(), parseConfig.getUsername(), parseConfig.getPassword(), logging)

# set vars
ipAddressPrevious = b""
timeLastUpdate = 0

while (True):
    ipAddress = getIP.getIP(parseConfig.getIpVersion())
    if ((ipAddress != 0) and ((googleDDNS.getCurrentTimeInMillis() - timeLastUpdate) > 3600000) or (ipAddress != ipAddressPrevious)):
            ipAddressPrevious = ipAddress
            logging.info('Update for %s - IP %s', parseConfig.getHostName(), ipAddress.decode("utf-8"))
            googleDDNS.updateIP(ipAddress)
            timeLastUpdate = googleDDNS.getCurrentTimeInMillis()
    time.sleep(60)
