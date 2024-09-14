#!/bin/bash
IPFILE=./ips-cloudflare.txt
CONFFILE=./proxy.conf
wget 'https://www.cloudflare.com/ips-v4/' -O $IPFILE
printf "\n" >> $IPFILE
wget 'https://www.cloudflare.com/ips-v6/' -O ->> $IPFILE

rm $CONFFILE

for IP in $(cat $IPFILE); do
    printf "set_real_ip_from $IP;\n" >> $CONFFILE
done

printf "\nreal_ip_header CF-Connecting-IP;" >> $CONFFILE
