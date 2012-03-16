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

CONFIGURAR_SABOR() {
[ -z $1 ] && ERROR "Necesito un argumento" && exit 1

if [ -e "${PLANTILLAS}${1}/sabor.conf" ]; then
	. "${PLANTILLAS}${1}/sabor.conf"
else
	ERROR "El sabor $1 no posee archivo de configuración ${PLANTILLAS}${1}/sabor.conf" && exit 1
fi

if [ -e "${PLANTILLAS}${1}/preseed-instalador.cfg" ]; then
	mkdir -p "${ISO_DIR}config/binary_debian-installer"
	cp ${PLANTILLAS}${1}/preseed-instalador.cfg ${ISO_DIR}config/binary_debian-installer/preseed.cfg
fi

if [ -e "${PLANTILLAS}${1}/banner-instalador.png" ]; then
	mkdir -p "${ISO_DIR}config/binary_debian-installer-includes/usr/share/graphics"
	cp ${PLANTILLAS}${1}/banner-instalador.png ${ISO_DIR}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png
fi

if [ -e "${PLANTILLAS}${1}/gtkrc-instalador" ]; then
	mkdir -p "${ISO_DIR}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0"
	cp ${PLANTILLAS}${1}/gtkrc-instalador ${ISO_DIR}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0/gtkrc
fi

if [ -d "${PLANTILLAS}${1}/inclusiones-iso" ]; then
        mkdir -p "${ISO_DIR}config/binary_local-includes"
        cp -r ${PLANTILLAS}${1}/inclusiones-iso/* ${ISO_DIR}config/binary_local-includes/
fi

if [ -d "${PLANTILLAS}${1}/inclusiones-fs" ]; then
        mkdir -p "${ISO_DIR}config/chroot_local-includes"
        cp -r ${PLANTILLAS}${1}/inclusiones-fs/* ${ISO_DIR}config/chroot_local-includes/
fi

if [ -e "${PLANTILLAS}${1}/syslinux.png" ]; then
	mkdir -p "${ISO_DIR}config/binary_syslinux"
	cp ${PLANTILLAS}${1}/syslinux.png ${ISO_DIR}config/binary_syslinux/splash.png
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

if [ -n "${SABOR_PAQUETES_ISOPOOL}" ]; then
	mkdir -p "${ISO_DIR}config/binary_local-packageslists"
	echo ${SABOR_PAQUETES_ISOPOOL} > ${ISO_DIR}config/binary_local-packageslists/paquetes-pool.list
fi

echo "${1}" > ${ISO_DIR}config/sabor-configurado
}

CHECK() {
#-------------------------------------------------------------#
# Nombre de la Función: CHECK
# Propósito: Comprobar que ciertos parámetros se cumplan al
#            inicio del script canaima-desarrollador.sh
# Dependencias:
#	- Requiere la carga del archivo ${VARIABLES} y ${CONF}
#	- Paquetes: findutils
#-------------------------------------------------------------#

[ $( id -u ) != 0 ] && ERROR "¡Canaima Semilla debe ser ejecutado como root!" && exit 1

[ ! -d ${ISO_DIR} ] && ERROR "¡El directorio de construcción de ISO's no existe!" && exit 1

# Asegurando que las carpetas especificadas
# terminen con un slash (/) al final
ultimo_char_iso=${ISO_DIR#${ISO_DIR%?}}
ultimo_char_pla=${PLANTILLAS#${PLANTILLAS%?}}
ultimo_char_scr=${SCRIPTS#${SCRIPTS%?}}
[ "${ultimo_char_iso}" != "/" ] && ISO_DIR="${ISO_DIR}/"
[ "${ultimo_char_pla}" != "/" ] && PLANTILLAS="${PLANTILLAS}/"
[ "${ultimo_char_scr}" != "/" ] && SCRIPTS="${SCRIPTS}/"
echo "Iniciando Canaima Semilla ..."
}
