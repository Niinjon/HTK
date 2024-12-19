#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi