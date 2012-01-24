#!/bin/bash -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: canaima-semilla.sh
# DESCRIPCIÓN: Script de bash principal del paquete canaima-desarrollador
# COPYRIGHT:
#  (C) 2010 Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
# LICENCIA: GPL3
# ==============================================================================
#
# Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los
# términos de la Licencia Pública General de GNU (versión 3).

function ERROR() {
echo -e ${ROJO}${1}${FIN}
}

function ADVERTENCIA() {
echo -e ${AMARILLO}${1}${FIN}
}

function EXITO() {
echo -e ${VERDE}${1}${FIN}
}

function CONFIGURAR-SABOR() {
[ -z $1 ] && ERROR 'Nececito un argumento' && exit 1

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

if [ -e ${PLANTILLAS}${1}/*.binary ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${1}/*.binary ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${1}/*.binary.gpg ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${1}/*.binary.gpg ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${1}/*.chroot ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${1}/*.chroot ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${1}/*.chroot.gpg ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${1}/*.chroot.gpg ${ISO_DIR}config/chroot_sources/
fi

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

function CHECK() {
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
