#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

echo "interfaces fájl módosítása"
INTERFACES_FILE="/etc/network/interfaces"
if [[ ! -f "$INTERFACES_FILE" || ! $(grep -q "iface eth0 inet static" "$INTERFACES_FILE") ]]; then
    cat <<EOL > /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address $IP_ADDRESS
    netmask $NETMASK
    gateway $GATEWAY
    dns-nameservers $DNS_SERVER
EOL
echo "Fájl sikeresen módosítva"
else
    echo "A fájl már létezik és nem üres"
fi

RESOLV_FILE="/etc/resolv.conf"
if [[ ! -f $RESOLV_FILE ]]; then
    touch "$RESOLV_FILE"
fi

if ! grep -qE "nameserver $DNS_SERVER | nameserver 8.8.8.8" "$RESOLV_FILE"; then
    echo "nameserver $DNS_SERVER" >> "$RESOLV_FILE"
    echo "Resolv.conf sikeresen konfigurálva"
else
    echo "Resolv.conf már létezik és tartalmazza a beállításokat"
fi

SOURCES_LIST="/etc/apt/sources.list"
if [[ ! -f "$SOURCES_LIST" ]]; then
    echo -e "deb http://ftp.debian.org/debian stable main contrib non-free\n\ndeb-src http://ftp.debian.org/debian stable main contrib non-free" > "$SOURCES_LIST"
fi

FILES=("$INTERFACES_FILE","$RESOLV_FILE","$SOURCES_LIST")

for file in "${FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "!!!!!!!!!Figyelmezetetés!!!!!!!!!: A(z) $file nem létezik!"
    fi
done

echo "Sikeres konfiguráció"
echo "IP-cím: $IP_ADDRESS"
echo "Netmask: $NETMASK"
echo "Átjáró: $GATEWAY"
echo "DNS-szerver: $DNS_SERVER"
