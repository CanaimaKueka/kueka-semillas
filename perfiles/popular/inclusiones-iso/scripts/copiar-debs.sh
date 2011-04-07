#!/bin/bash

MOUNTPOINT="/target"

mkdir -p ${MOUNTPOINT}/root/debs/

cp ${MOUNTPOINT}/media/cdrom/pool/main/g/gettext/gettext-base*.deb  ${MOUNTPOINT}/root/debs/
cp ${MOUNTPOINT}/media/cdrom/pool/main/b/burg/burg*.deb ${MOUNTPOINT}/root/debs/
cp ${MOUNTPOINT}/media/cdrom/pool/main/b/burg-themes/burg*.deb ${MOUNTPOINT}/root/debs/

PARTICION=$( mount | grep "/target " | awk '{print $1}' )
DRIVE=${PARTITION%?}

echo "#!/bin/bash" > ${MOUNTPOINT}/root/instalar-debs.sh
echo "" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "echo \"burg-pc burg/linux_cmdline string\" | debconf-set-selections" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "echo \"burg-pc burg/linux_cmdline_default string quiet splash vga=791\" | debconf-set-selections" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "echo \"burg-pc burg-pc/install_devices multiselect ${DRIVE}\" | debconf-set-selections" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/gettext-base*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-themes-common*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-themes_*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-common*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-emu*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-pc*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "aptitude purge canaima-instalador-vivo --assume-yes" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "dpkg-reconfigure cunaguaro guacharo canaima-estilo-visual canaima-plymouth canaima-escritorio-gnome canaima-chat canaima-bienvenido canaima-escritorio-gnome canaima-base" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "update-burg" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "rm -rf /root/debs/" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "rm /root/instalar-debs.sh" >> ${MOUNTPOINT}/root/instalar-debs.sh

chmod +x ${MOUNTPOINT}/root/instalar-debs.sh


