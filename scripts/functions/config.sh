#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: canaima-semilla.sh
# DESCRIPCIÓN: libreria de sh principal del paquete canaima-desarrollador
# COPYRIGHT:
#  (C) 2010 Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
# LICENCIA: GPL3
# ==============================================================================
#
# Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los
# términos de la Licencia Pública General de GNU (versión 3).

function CS_BUILD_CONFIG() {

        PROFILE="${1}"
	shift || true

	if [ -z "${PROFILE}" ]; then
		ERROR "La función \"${FUNCNAME}\" necesita un nombre de perfil válido como argumento."
	fi

	if [ -e "${PROFILES}${PROFILE}/preseed-instalador.cfg" ]; then
		mkdir -p "${ISODIR}config/binary_debian-installer"
		cp "${PROFILES}${PROFILE}/preseed-instalador.cfg" "${ISODIR}config/binary_debian-installer/preseed.cfg"
	fi

	if [ -e "${PROFILES}${PROFILE}/banner-instalador.png" ]; then
		mkdir -p "${ISODIR}config/binary_debian-installer-includes/usr/share/graphics"
		cp "${PROFILES}${PROFILE}/banner-instalador.png" "${ISODIR}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png"
	fi

	if [ -e "${PROFILES}${PROFILE}/gtkrc-instalador" ]; then
		mkdir -p "${ISODIR}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0"
		cp "${PROFILES}${PROFILE}/gtkrc-instalador" "${ISODIR}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0/gtkrc"
	fi

	if [ -d "${PROFILES}${PROFILE}/inclusiones-iso" ]; then
		mkdir -p "${ISODIR}config/binary_local-includes"
        	cp -r "${PROFILES}${PROFILE}/inclusiones-iso/*" "${ISODIR}config/binary_local-includes/"
	fi

	if [ -d "${PROFILES}${PROFILE}/inclusiones-fs" ]; then
        	mkdir -p "${ISODIR}config/chroot_local-includes"
        	cp -r "${PROFILES}${PROFILE}/inclusiones-fs/*" "${ISODIR}config/chroot_local-includes/"
	fi

	if [ -e "${PROFILES}${PROFILE}/syslinux.png" ]; then
		mkdir -p "${ISODIR}config/binary_syslinux"
		cp "${PROFILES}${PROFILE}/syslinux.png" "${ISODIR}config/binary_syslinux/splash.png"
		SABOR_SYSPLASH="config/binary_syslinux/splash.png"
	fi

# damn you daniel bauman
for i in "binary     list.binary" \
	"binary.gpg  key.binary"  \
	"chroot      list.chroot" \
	"chroot.gpg  key.chroot"; do
	echo $i | while read ext dext; do
		if [ -e ${PLANTILLAS}${1}/*.${ext} ]; then
			mkdir -p "${ISO_DIR}config/archives"
			for l in `ls ${PLANTILLAS}${1}/*.${ext}`; do
				b=`basename $l | sed s/\.${ext}$//`
				cp $l ${ISO_DIR}config/archives/$b.$dext
				echo "$l\t->\t$b.$dext"
			done
		fi
	done
done

if [ -e ${PLANTILLAS}${1}/preseed-debconf.cfg ]; then
	mkdir -p "${ISO_DIR}config/chroot_local-preseed"
	cp ${PLANTILLAS}${1}/preseed-debconf.cfg ${ISO_DIR}config/chroot_local-preseed/
fi

if [ -e ${PLANTILLAS}${1}/chroot-local-hook.sh ]; then
        mkdir -p "${ISO_DIR}config/chroot_local-hooks"
        cp ${PLANTILLAS}${1}/chroot-local-hook.sh ${ISO_DIR}config/chroot_local-hooks/
fi

if [ ! -z "$SABOR_PAQUETES" ]; then
        mkdir -p config/package-lists
        echo ${SABOR_PAQUETES} | xargs -n1 > config/package-lists/${DISTRO}-${sabor}.list
#       pkglist_arg="--package-lists=${DISTRO}-${sabor}"
else
        ADVERTENCIA "No tiene paquetes especificos, esta seguro ?"
fi

if [ -n "${SABOR_PAQUETES_ISOPOOL}" ]; then
	mkdir -p "${ISO_DIR}config/binary_local-packageslists"
	echo ${SABOR_PAQUETES_ISOPOOL} > ${ISO_DIR}config/binary_local-packageslists/paquetes-pool.list
fi

echo "${1}" > ${ISO_DIR}config/sabor-configurado
}

