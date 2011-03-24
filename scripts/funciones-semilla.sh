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

if [ -e "${PLANTILLAS}${SABOR}/sabor.conf" ]; then
	. "${PLANTILLAS}${SABOR}/sabor.conf"
else
	ERROR 'El sabor "'${SABOR}'" no posee archivo de configuración ${PLANTILLAS}${SABOR}/sabor.conf' && exit 1
fi

if [ -e "${PLANTILLAS}${SABOR}/preseed-instalador.cfg" ]; then
	mkdir -p "${ISO_DIR}config/binary_debian-installer"
	cp ${PLANTILLAS}${SABOR}/preseed-instalador.cfg ${ISO_DIR}config/binary_debian-installer/preseed.cfg
fi

if [ -e "${PLANTILLAS}${SABOR}/banner-instalador.png" ]; then
	mkdir -p "${ISO_DIR}config/binary_debian-installer-includes/usr/share/graphics"
	cp ${PLANTILLAS}${SABOR}/banner-instalador.png ${ISO_DIR}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png
fi

if [ -e "${PLANTILLAS}${SABOR}/gtkrc-instalador" ]; then
	mkdir -p "${ISO_DIR}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0"
	cp ${PLANTILLAS}${SABOR}/gtkrc-instalador ${ISO_DIR}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0/gtkrc
fi

if [ -e "${PLANTILLAS}${SABOR}/syslinux.png" ]; then
	mkdir -p "${ISO_DIR}config/binary_syslinux"
	cp ${PLANTILLAS}${SABOR}/syslinux.png ${ISO_DIR}config/binary_syslinux/splash.png
	SABOR_SYSPLASH="config/binary_syslinux/splash.png"
fi

if [ -e ${PLANTILLAS}${SABOR}/*.binary ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${SABOR}/*.binary ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${SABOR}/*.binary.gpg ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${SABOR}/*.binary.gpg ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${SABOR}/*.chroot ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${SABOR}/*.chroot ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${SABOR}/*.chroot.gpg ]; then
	mkdir -p "${ISO_DIR}config/chroot_sources"
	cp ${PLANTILLAS}${SABOR}/*.chroot.gpg ${ISO_DIR}config/chroot_sources/
fi

if [ -e ${PLANTILLAS}${SABOR}/preseed-debconf.cfg ]; then
	mkdir -p "${ISO_DIR}config/chroot_local-preseed"
	cp ${PLANTILLAS}${SABOR}/preseed-debconf.cfg ${ISO_DIR}config/chroot_local-preseed/
fi

if [ -e ${PLANTILLAS}${SABOR}/chroot-local-hook.sh ]; then
        mkdir -p "${ISO_DIR}config/chroot_local-hooks"
        cp ${PLANTILLAS}${SABOR}/chroot-local-hook.sh ${ISO_DIR}config/chroot_local-hooks/
fi

echo "${SABOR}" > ${ISO_DIR}config/sabor-configurado
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
