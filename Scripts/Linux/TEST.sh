#!/bin/bash
touch "/home/args.txt"

OUTPUT_FILE="/home/args.txt"

SERVICES=("ssh" "apache2" "smbd" "isc-dhcp-server" "vsftpd" "bind9" "iptables")

echo "===== Szolgáltatások Állapota =====" > "$OUTPUT_FILE"

for SERVICE in "${SERVICES[@]}"; do
    if systemctl list-units --type=service --no-pager --all | grep -q "$SERVICE"; then
        echo "Szolgáltatás: $SERVICE" >> "$OUTPUT_FILE" 
        systemctl status "$SERVICE" --no-pager >> "$OUTPUT_FILE"

        CONFIG_PATH=$(systemctl show "$SERVICE" | grep -i "fragmentpath" | awk -F= '{print $2}')

        if [[ -n "$CONFIG_PATH" ]]; then
            echo "Config fájl: $CONFIG_PATH" >> "$OUTPUT_FILE"
            echo "Config tartalom:" >> "$OUTPUT_FILE"
            cat "$CONFIG_PATH" >> "$OUTPUT_FILE"
        else
            echo "A konfigurációs fájl nem található" >> "$OUTPUT_FILE"
        fi

        echo -e "\n" >> "$OUTPUT_FILE"
    fi
done

echo -e "\n===== Hálózati Adapterek IP-konfiguráció =====" >> "$OUTPUT_FILE"
ip addr show >> "$OUTPUT_FILE"

echo "A teszt lefutott az eredmények a $OUTPUT_FILE fájlban található."