#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Root jogokkal kell futtatni!"
    exit 1
fi

read -p "Add meg az FTP megosztás helyét: " FTP_DIR
read -p "Add meg a passzivmód minimum portját (10000): " PASV_MIN_PORT
read -p "Add meg a passzivmód maximum portját (10100): " PASV_MAX_PORT
read -p "Add meg a felhasználó nevét: "

if [[  ! -d "$FTP_DIR" ]]; then
    echo "A megadott mappa nem létezik. Létrehozzuk..."
    mkdir -p "$FTP_DIR"
    chown ftp:ftp "$FTP_DIR"
fi

if id "$FTP_USER"&>/dev/null; then
    echo "A megadott felhasználó ($FTP_USER) létezik."
else
    echo "A megadott felhasználó ($FTP_USER) nem létezik. Létrehozzuk..."
    useradd -m -s /sbin/nologin "$FTP_USER"
    passwd "$FTP_USER"
    chown "$FTP_USER:$FTP_USER" "$FTP_DIR"
fi

echo "vsftpd telepítése"
apt-get update && apt-get install vsftpd -y

echo "Konfig fájl biztonsági mentése"
cp /etc/vsftpd.conf /etc/vsftpd.conf.bak

echo "Konfigfájl módosítása"
cat <<EOL > /etc/vsftpd.conf
listen=YES
anonymus_enable=NO
local_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xfrelog_enable=YES
connect_from_pot_20=YES
chroot_local_user=NO
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd.chroot_list
allow_writeable_chroot=YES
secure_chroot_dir=/var/run/vsftpd/empty
pasv_enable=YES
pasv_min_port=$PASV_MIN_PORT
pasv_max_port=$PASV_MAX_PORT
user_sub_token=\$USER
local_root=$FTP_DIR
EOL

if [[ ! -f /etc/vsftpd.chroot_list ]]; then
    touch /etc/vsftpd.chroot_list
fi

if ! grep -q "^$FTP_USER" /etc/vsftpd.chroot_list; then
    echo "$FTP_USER" >> /etc/vsftpd.chroot_list
    echo $FTP_USER felhasználó hozzá lett adva a chrootlisthez.
else
    echo "$FTP_USER felhasználó már hozzá lett adva a chrootlisthez."
fi

echo "vsftpd újraindítása..."
systemctl restart vsftpd

echo "vsftpd sikeresen telepítve"
echo "Megosztás helye: $FTP_DIR"
echo "Passzív port tartomány: $PASV_MIN_PORT - $PASV_MAX_PORT"
echo "Felhasználó: $FTP_USER"