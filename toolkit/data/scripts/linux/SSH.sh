#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

echo "SSH telepítése"
apt-get update && apt-get install openssh-server -y

systemctl status ssh --no-pager

echo "Az SSH sikeresen telepítve"