#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

echo "Apache2 webszerver telepítése"
apt-get update && apt-get install apache2 -y

systemctl status apache2 --no-pager