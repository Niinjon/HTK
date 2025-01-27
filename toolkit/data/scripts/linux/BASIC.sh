#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

echo "interfaces fájl módosítása"
cat <<EOL > /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address $IP_ADDRESS
    netmask $NETMASK
    gateway $GATEWAY
EOL

echo "interfaces fájl sikeresen frissíve"

if [[ ! -f /etc/resolv.conf ]]; then
    echo "A fájl nem létezik"
    touch /etc/resolv.conf
fi

echo "nameserver $DNS_SERVER" > /etc/resolv.conf

sed -i '1d' /etc/apt/sources.list
sed -i '1i deb http://ftp.debian.org/debian stable main contrib non-free\n\ndeb-src http://ftp.debian.org/debian stable main contrib non-free' /etc/apt/sources.list

echo "Sikeres konfiguráció"
echo "IP-cím: $IP_ADDRESS"
echo "Netmask: $NETMASK"
echo "Átjáró: $GATEWAY"
echo "DNS-szerver: $DNS_SERVER"
