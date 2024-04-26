# vyos-droplist
Script that fetches Spamhaus drop or dropv6 list and updates VyOS network block ruleset

Edit updateDroplist.sh according to your use-case: want to block IPv4, IPv6 (or both)

Save scripts to persistent storage within VyOS and make them executable:
  chmod 755 /config/scripts/updateDroplist.sh
  chmod 755 /config/scripts/updateDroplist.py

Configure task scheduler:
  configure
  set system task-scheduler task updateDroplist executable arguments 'sg vyattacfg -c'
  set system task-scheduler task updateDroplist executable path '/config/scripts/updateDroplist.sh'
  set system task-scheduler task updateDroplist interval '1d'
  commit
  save

Configure your IPv4/IPv6 firewall rules. I use a zone-based configuration:
  "IPV4"
  set firewall ipv4 name WAN-LOCAL rule 10 source group network-group 'ng-Blocklist'
  set firewall ipv4 name WAN-LOCAL rule 10 action 'drop'
  set firewall ipv4 name WAN-LOCAL rule 10 log
  set firewall ipv4 name WAN-LOCAL rule 10 description 'Drop traffic from DROP/eDROP networks'
  
  set firewall ipv4 name WAN-LAN rule 10 source group network-group 'ng-Blocklist'
  set firewall ipv4 name WAN-LAN rule 10 action 'drop'
  set firewall ipv4 name WAN-LAN rule 10 log
  set firewall ipv4 name WAN-LAN rule 10 description 'Drop traffic from DROP/eDROP networks'
  
  set firewall ipv4 name LAN-WAN rule 10 destination group network-group 'ng-Blocklist'
  set firewall ipv4 name LAN-WAN rule 10 action 'drop'
  set firewall ipv4 name LAN-WAN rule 10 log
  set firewall ipv4 name LAN-WAN rule 10 description 'Drop traffic to DROP/eDROP networks
  
  set firewall ipv4 name LOCAL-WAN rule 10 destination group network-group 'ng-Blocklist'
  set firewall ipv4 name LOCAL-WAN rule 10 action 'drop'
  set firewall ipv4 name LOCAL-WAN rule 10 log
  set firewall ipv4 name LOCAL-WAN rule 10 description 'Drop traffic to DROP/eDROP networks'

  "IPV6"
  set firewall ipv6 name WAN-LOCAL-6 rule 10 source group network-group 'ng-Blocklist-v6'
  set firewall ipv6 name WAN-LOCAL-6 rule 10 action 'drop'
  set firewall ipv6 name WAN-LOCAL-6 rule 10 log
  set firewall ipv6 name WAN-LOCAL-6 rule 10 description 'Drop traffic from DROP/eDROP networks'
  
  set firewall ipv6 name WAN-LAN-6 rule 10 source group network-group 'ng-Blocklist-v6'
  set firewall ipv6 name WAN-LAN-6 rule 10 action 'drop'
  set firewall ipv6 name WAN-LAN-6 rule 10 log
  set firewall ipv6 name WAN-LAN-6 rule 10 description 'Drop traffic from DROP/eDROP networks'
  
  set firewall ipv6 name LAN-WAN-6 rule 10 destination group network-group 'ng-Blocklist-v6'
  set firewall ipv6 name LAN-WAN-6 rule 10 action 'drop'
  set firewall ipv6 name LAN-WAN-6 rule 10 log
  set firewall ipv6 name LAN-WAN-6 rule 10 description 'Drop traffic to DROP/eDROP networks'
  
  set firewall ipv6 name LOCAL-WAN-6 rule 10 destination group network-group 'ng-Blocklist-v6'
  set firewall ipv6 name LOCAL-WAN-6 rule 10 action 'drop'
  set firewall ipv6 name LOCAL-WAN-6 rule 10 log
  set firewall ipv6 name LOCAL-WAN-6 rule 10 description 'Drop traffic to DROP/eDROP networks'
