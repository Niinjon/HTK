#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

echo "Elérhető hálózati adapterek: "
ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | nl
echo ""

read -p "Add meg a domain nevet: " DOMAIN_NAME

if [[ -z "$DOMAIN_NAME" ]]; then
    echo "Domain megadása kötelező"
    exit 1
fi

read -p "Add meg a szerver ip-t: " SERVER_IP

if [[ -z "$SERVER_IP" ]]; then
    echo "Ip megadása kötelező"
    exit 1
fi

echo "BIND9 telepítés"
apt-get update && apt-get install bind9 -y

ZONE_FILE="/etc/bind/db.$DOMAIN_NAME"
NAMED_CONF_LOCAL="/etc/bind/named.conf.local"

echo "Domain konfig"
cat <<EOL >> $NAMED_CONF_LOCAL

zone "$DOMAIN_NAME" {
    type master;
    file "$ZONE_FILE";
};
EOL

echo "Zónafájl létrehozása: $ZONE_FILE"
cat <<EOL > $ZONE_FILE
\$TTL 604800
@       IN      SOA     ns1.$DOMAIN_NAME. admin.$DOMAIN_NAME. (
                  2         ; Serial
             604800         ; Refresh
              86400         ; Retry
            2419200         ; Expire
             604800 )       ; Negative Cache TTL
;
@       IN      NS      ns1.$DOMAIN_NAME.
ns1     IN      A       $SERVER_IP
@       IN      A       $SERVER_IP
www     IN      A       $SERVER_IP
EOL

echo "BIND9 konfig ellenőrzés"
named-checkconf
if [[ $? -ne 0 ]]; then
    echo "Hiba történt a zóna fájl ellenőrzésekor"
    exit 1
fi

named-checkzone "$DOMAIN_NAME" "$ZONE_FILE"
if [[ $? -ne 0 ]]; then
    echo "Hiba a zóna ellenőrzésekor"
    exit 1
fi

echo "BIND9 újraindítása"
systemctl restart bind9

echo "A BIND9 sikeresen telepítve"
echo "Domain: $DOMAIN_NAME"
echo "Szerver IP: $SERVER_IP"
echo "Zónafájl: $ZONE_FILE"
systemctl status bind9 --no-pager