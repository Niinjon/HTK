#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

read -p "Add meg a DHCP tartomány kezdő IP-címet (pl 192.168.1.100): " RANGE_START
read -p "Add meg a Záró IP-címet: " RANGE_END

read -p "Add meg az alhálózati mszkot: " SUBNET_MASK

read -p "Add meg az alhálózat IP-címét: " SUBNET_IP

read -p "Add meg az alapértelmezett átjárót: " GATEWAY

read -p "Add meg a DNS szerver IP-t (opcionális): " DNS_SERVER

apt-get update && apt-get install isc-dhcp-server -y

DHCP_CONF="/etc/dhcp/dhcpd.conf"

cat > $DHCP_CONF <<EOL
default-lease-time 600;
max-lease-time 7200;

subnet $SUBNET_IP netmask $SUBNET_MASK {
    range $RANGE_START $RANGE_END
    option routers $GATEWAY;
    option domain-name-servers $DNS_SERVER;
}
EOL

echo "A DHCP konfiguráció módosítva."


INTERFACES_FILE="/etc/default/isc-dhcp-server"

if [ -f $INTERFACES_FILE ]; then
    sed -i "s/^INTERFACESv4=.*/INTERFACESv4=\"$INTERFACE\"/" $INTERFACES_FILE
else
    echo "INTERFACESv4=\"$INTERFACE\"" > $INTERFACES_FILE
fi

echo "Interfész beállítva: $INTERFACE"

echo "DHCP szolgáltatás újraindítása"
systemctl restart isc-dhcp-server

systemctl status isc-dhcp-server --no-pager

echo "A DHCP konfig kész"
