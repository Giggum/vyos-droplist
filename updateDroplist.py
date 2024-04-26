#!/usr/bin/env python3
# FILE: /config/scripts/updateDroplist.py
# WHO: Giggum @ https://github.com/Giggum
# WHAT: Script that fetches Spamhaus drop or dropv6 list
#       and updates VyOS network block ruleset
# WHEN: 2024-01-01
#
# Usage
# =============
# $ python3 updateDroplist.py --url [URL]
#
# [URL] options:
#    https://www.spamhaus.org/drop/drop.txt
#    https://www.spamhaus.org/drop/dropv6.txt
#    if using dropv6.txt include --ipv6 in command above
#
import argparse
import logging
#import subprocess
#import socket
import sys
import urllib.request
from datetime import datetime

# Setting up logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(description='Retrieve Spamhaus Drop or Dropv6 list and update firewall ruleset accordingly', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--ipv6', action="store_true", help='Switch to enable processing of IPv6 addresses')
parser.add_argument('--url', help='URL where blocklist will be retrieved from')
parser.add_argument('--network_group', help='Name of network-group to save blocklist addresses to')

def get_blocklist(url: str):
    response = urllib.request.urlopen(url)
    data = response.readlines()
    return data

def generate_blocklist():
    f = get_blocklist(args.url)
    blocklist = []

    for row in f:
        row = str(row, 'utf-8')
        addr_extract = row.partition(";")[0].strip()

        # skip any lines without IPs
        if len(addr_extract) < 1:
            pass

        # skip any lines that contain local addresses
        elif addr_extract in ['127.0.0.0/8', '::1/128', '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '169.254.0.0/16', 'fc00::/7', 'fe80::/10']:
            pass

        else:
            address = addr_extract
            blocklist.append(address)

    log.info(f"INFO: {len(blocklist)} blacklisted networks retrived!")
    return blocklist

def apply_blocklist(list):
    DATE = datetime.now()
    NETWORKGROUP = args.network_group

    if(args.ipv6):
        print(f"delete firewall group ipv6-network-group {NETWORKGROUP}")
        print(f"set firewall group ipv6-network-group {NETWORKGROUP} description 'Spamhaus DROP/eDROP IPv6 list as of {DATE.strftime('%Y-%m-%d')}'")

        for ADDRESS in list:
            print(f"set firewall group ipv6-network-group {NETWORKGROUP} network {ADDRESS}")

    else:
        print(f"delete firewall group network-group {NETWORKGROUP}")
        print(f"set firewall group network-group {NETWORKGROUP} description 'Spamhaus DROP/eDROP IPv4 list as of {DATE.strftime('%Y-%m-%d')}'")

        for ADDRESS in list:
            print(f"set firewall group network-group {NETWORKGROUP} network {ADDRESS}")

if __name__ == '__main__':
    args = parser.parse_args()

    try:
        list = generate_blocklist()
        apply_blocklist(list)

    except ConfigError as e:
        print(e)
        sys.exit(1)
