#!/bin/vbash
source /opt/vyatta/etc/functions/script-template

_script_name="updateDroplist"
logger(){
    /usr/bin/logger -t ${_script_name} -p local1.notice "$@" 
}

START=$(date +"%s")

logger "INFO: Starting ${_script_name} script..."

configure
source <(/config/scripts/updateDroplist.py --url https://www.spamhaus.org/drop/drop.txt --network_group ng-Blocklist)
commit

configure
source <(/config/scripts/updateDroplist.py --ipv6 --url https://www.spamhaus.org/drop/dropv6.txt --network_group ng-Blocklist-v6)
commit

END=$(date +"%s")
DIFF=$(($END-$START))

logger "INFO: Network group(s) updated in $(($DIFF / 60)) minutes and $(($DIFF % 60)) seconds!"
