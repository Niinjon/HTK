#!/bin/bash

OUTPUT_FILE="args.txt"
> "$OUTPUT_FILE"

echo "===== Összes Szolgáltatás =====" >> "$OUTPUT_FILE"

systemctl list-units --type=service --all --no-pager >> "$OUTPUT_FILE"

echo "\n===== Szolgáltatások konfigurációjai =====" >> "$OUTPUT_FILE"

for SERVICE in $(systemctl list-units --type=service --all --no-pager --no-legend | awk '{print $1}'); do
    CONFIG_PATH=$(systemctl show "$SERVICE" | grep -i "fragmentpath" | awk -F= '{print $2}')
    if [ -n "$CONFIG_PATH" ]; then
        echo "Szolgáltatás: $SERVICE" >> "$OUTPUT_FILE"
        echo "Config fájl: $CONFIG_PATH" >> "$OUTPUT_FILE"
        if [ -f "$CONFIG_PATH" ]; then
            echo "Config tartalom:" >> "$OUTPUT_FILE"
            cat "$CONFIG_PATH" >> "$OUTPUT_FILE"
        else
            echo "A konfigurációs fájl nem található." >> "$OUTPUT_FILE"
        fi
        echo -e "\n" >> "$OUTPUT_FILE"
    fi
done

echo -e "\n===== Hálózati Adapterek IP-konfiguráció =====" >> "$OUTPUT_FILE"

ip addr show >> "$OUTPUT_FILE"

echo "A teszt lefutott az eredmények a $OUTPUT_FILE fájlban található."