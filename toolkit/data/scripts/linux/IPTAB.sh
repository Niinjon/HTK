#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

apt-get update && apt-get install iptables -y && apt-get install iptables-persistent -y

echo "IP Forwarding engedélyezése..."
sysctl_conf="/etc/sysctl.conf"
cat <<EOL > /etc/sysctl.conf
    net.ipv4.ip_forward=1
EOL
sysctl -p

read -p "Add meg a belső interfészt(pl eth1): " INTERNAL_IF
read -p "Add meg a külső interfészt(pl eth0): " EXTERNAL_IF

echo "IPtables szabályok konfigurálása"
iptables -t nat -A POSTROUTING -o $EXTERNAL_IF -j MASQUERADE
iptables -A FORWARD -i $INTERNAL_IF -o $EXTERNAL_IF -j ACCEPT
iptables -A FORWARD -i $EXTERNAL_IF -o $INTERNAL_IF -m state --state RELATED,ESTABLISHED -j ACCEPT

echo "Szabályok mentése"

iptables-save > /etc/iptables/rules.v4


echo "Szolgáltatás újra indítása"

systemctl restart netfilter-persistent