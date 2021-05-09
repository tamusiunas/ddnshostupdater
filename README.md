# DDNS Host Updater for Google Domains

Dynamic DNS (DDNS) is a method of automatically updating a name server in the Domain Name System (DNS), often in real time, with the active DDNS configuration of its configured hostnames, addresses or other information.

Users who have their domain registrations registered with [Google Domains](https://domains.google.com/registrar/) can create synthetic hosts to have their public IP address updated whenever they wish.

The DDNS Host Updater for Google Domains system is a system that allows automatic updating to the configured host whenever a change of public ip address is noticed.

There are three ways to use it:

Standalone
```bash
git clone https://github.com/tamusiunas/ddnshostupdater
cd ddnshostupdater

#
# Edit config.json and set you host credentials
#

python3 ./ddnshostupdater.py
```

Universal deb package

```bash
wget https://github.com/tamusiunas/ddnshostupdater/releases/download/1.0/ddnshostupdater_1.0.deb
sudo apt install ./ddnshostupdater.deb

#
# edit config.json and set you host credentials
#

systemctl restart ddnshostupdater

```

Docker container for multiple platforms

```bash
git clone https://github.com/tamusiunas/ddnshostupdater
cd ddnshostupdater

#
# Edit docker-compose.yml and set you host credentials
#

docker-compose create # (Create services)
docker-compose up # (Create and start containers - in foreground)
docker-compose down # (Stop and remove resources)
docker-compose start # (Start services - in background)
docker-compose stop # (Stop services)
```


## How to configure a Dynamic DNS Host at [Google Domains](https://support.google.com/domains/answer/6147083?hl=en)

### Dynamic DNS

Dynamic DNS allows you to direct your domain or a subdomain to a resource that is behind a gateway that has a dynamically assigned IP address.

To use dynamic DNS with Google Domains you set up a Dynamic DNS synthetic record. This synthetic record:

- Sets up an A or AAAA record for your domain or subdomain that lets the Google name servers know to expect a dynamic IP.

- Generates a username and password your host or server will use to communicate the new IP address to the Google name servers.

Once you set up the Dynamic DNS synthetic record, you must set up a client program on your host or server (the resource behind the gateway) or on the gateway itself that detects IP address changes and uses the generated username and password and communicate the new address to the Google name servers.

**Note**: Dynamic DNS works with both IPv4 and IPv6 addresses. 

### Setting up a Dynamic DNS synthetic record

1. Sign in to Google Domains.
2. Select the name of your domain.
3. Open the menu Menu.
4. Click DNS.
5. Scroll down to Synthetic Records.
6. Select Dynamic DNS from the list of synthetic record types.
7. Enter the name of the resource you plan to have assigned a Dynamic IP, either a subdomain or @ for your default domain (“root domain” or “naked domain”).
8. If you selected sub-domain, enter the name of the subdomain.
9. Click Add.
10. The Dynamic DNS record is created in your list of synthetic records. Click the expand triangle next to the record to view its values.
11. Click View Credentials to view the user name and password created for this record.
12. Note the username and password created for the synthetic record. You'll need these to configure your gateway or client software to contact the Google name servers.

You can edit or delete the record with the Edit and Delete buttons next to the record.
