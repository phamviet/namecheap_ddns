#!/usr/bin/env bash

DOMAIN=$1
PASSWORD=$2

PRIMARY_INTERFACE=eth0
SECONDARY_INTERFACE=wlan0
NAMECHEAP_DDNS=/usr/local/bin/namecheap_ddns.py
CACHE=/home/pi/.namecheap_ddns.cache

ipaddr=`ifconfig $PRIMARY_INTERFACE | awk '/inet addr:/{gsub(/.*:/,"",$2);print$2}'`
[ -z $ipaddr ] && ipaddr=`ifconfig $SECONDARY_INTERFACE | awk '/inet addr:/{gsub(/.*:/,"",$2);print$2}'`

if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
  echo "IPv4 is up"
else
  echo "IPv4 is down"
  exit 0
fi

EXTERNAL_IP=`curl --silent http://dynamicdns.park-your-domain.com/getip`

if [ ! -f "$NAMECHEAP_DDNS" ]; then
    curl -o $NAMECHEAP_DDNS https://raw.githubusercontent.com/phamviet/namecheap_ddns/master/namecheap_ddns.py
    chmod +x $NAMECHEAP_DDNS
fi

if [ ! -z "$ipaddr" ]; then
    $NAMECHEAP_DDNS --domain=$DOMAIN --password=$PASSWORD --host=* --ip=$EXTERNAL_IP --debug=1 --cachefile=$CACHE
    $NAMECHEAP_DDNS --domain=$DOMAIN --password=$PASSWORD --host=@ --ip=$EXTERNAL_IP --debug=1 --cachefile=$CACHE
    $NAMECHEAP_DDNS --domain=$DOMAIN --password=$PASSWORD --host=*.loc --ip=$ipaddr --debug=1 --cachefile=$CACHE
fi
