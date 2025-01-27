#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

echo "Samba telepítés"
apt-get update && apt-get install samba -y

echo "Elérhető hálózati interfészek: "
ip -o link show | awk -F': ' '{print $2}' | grep -v lo

read -p "Add meg a Samba által használni kívántat" NETWORK_INTERFACE

echo "Hálózati interfész beállítása"

sed -i "/^\[global]/a interfaces = 127.0.0.1/8 $NETWORK_INTERFACE\nbind interfaces only = yes" /etc/samba/smb.conf

read -p "Add meg a megosztás helyét" SHARE_PATH

if [ ! -d "$SHARE_PATH" ]; then
    echo "Könyvtár létrehozása: $SHARE_PATH"
    mkdir -p "$SHARE_PATH"
fi

chmod 0777 "$SHARE_PATH"

read -p "Add meg a samba felhasználó nevét" SMB_USER

if ! id "$SMB_USER" &>/dev/null; then
    echo "Felhasználó Létrehozása: $SMB_USER"
    useradd -M -s /sbin/nologin "$SMB_USER"
fi

echo "Jelszó beállítás"
smbpasswd -a "$SMB_USER"

read -p "Add meg a megosztás nevét: " NEV


echo "Konfig"
cat <<EOL >> /etc/samba/smb.conf

[$NEV]
    path = $SHARE_PATH
    valid users = $SMB_USER
    browseable = yes
    writeable = yes
    read only = no
    create mask = 0777
    directory mask = 0777
EOL

echo "Samba újraindítása"
systemctl restart smbd

echo "A(z) $NEV megosztás sikeresen létrehozva"
echo "Könyvtár: $SHARE_PATH"
echo "Felhasználó: $SMB_USER"
echo "Hálózati interfész: $NETWORK_INTERFACE"