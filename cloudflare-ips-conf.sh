#!/bin/bash
IPFILE=./ips-cloudflare.txt
PROXYFILE=./proxy.conf
ALLOWCF=./allow-cf.conf
wget 'https://www.cloudflare.com/ips-v4/' -O $IPFILE
printf "\n" >> $IPFILE
wget 'https://www.cloudflare.com/ips-v6/' -O ->> $IPFILE



for IP in $(cat $IPFILE); do
#    printf "set_real_ip_from $IP;\n" >> $PROXYFILE
    printf "allow $IP;\n" >> $ALLOWCF
done

#printf "\nreal_ip_header CF-Connecting-IP;" >> $PROXYFILE
printf "\ndeny all;" >> $ALLOWCF
