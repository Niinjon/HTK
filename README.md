# HTK
Hókuszpók Toolkit

Linux használat:

Ennek a parancsnak a kimenetéből megállapítod melyik számodra a megfelelő meghajtót:
# lsblk

Ezután csatolod a rendszerhez a mount (/mnt) mappába a következő parancsal: 
# mount /dev/{A meghajtó} /mnt

Ezután belépsz a csatolt meghajtó könyvtárába következő képpen:
# cd /mnt

És futtatod az install.sh fájlt ezen a módon:
# ./install.sh
