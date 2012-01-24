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

VARIABLES="/usr/share/canaima-semilla/variables.conf"

# Inicializando variables
. ${VARIABLES}

# Cargando funciones
. ${FUNCIONES}

# Comprobaciones varias
CHECK

action=$1; shift 1 || true;
# Case encargado de interpretar los parámetros introducidos a
# canaima-semilla y ejecutar la función correspondiente
case ${action} in

# En caso de que queramos construir una ISO
construir)
TEMP=`getopt -o a:m:s:iI --long arquitectura:,medio:,sabor:,instalador,no-instalador -n $0 -- "$@"`

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$TEMP"

while true; do
	case "$1" in
		-a|--arquitectura) ARQUITECTURA=$2;       shift 2;;
		-m|--medio)        MEDIO=$2;      shift 2;;
		-s|--sabor)        SABOR=$2;      shift 2;;
		-i|--instalador)      INSTALADOR=1;  shift 1;;
		-I|--no-instalador)   INSTALADOR=""; shift 1;;
		;;
                --) shift ; break ;;
                *) echo "Internal error!" ; exit 1 ;;
	esac
done

#INSTALADOR
if [ ${INSTALADOR} == "1" ]; then
	INSTALADOR="--debian-installer=live"
else
	INSTALADOR="--debian-installer=false"
	ADVERTENCIA 'No se incluirá el instalador.'
	INSTALADOR
fi

#ARQUITECTURA
if [ -z ${ARQUITECTURA} ]; then
	eval `dpkg-architecture`
	arch=${DEB_BUILD_ARCH}
	ADVERTENCIA 'No especificaste una arquitectura, utilizando ${ARQUITECTURA} presente en el sistema.'
fi

SABOR_KERNEL=${ARQUITECTURA}

case ${ARQUITECTURA} in
	i386)  SABOR_KERNEL=686;;
	amd64) SABOR_KERNEL=amd64;;
	*)     ERROR 'Arquitectura "'${ARQUITECTURA}'" no soportada en Canaima. Abortando.';;
esac
;;

#SABOR
if [ -z ${SABOR} ]; then
	SABOR="popular"
	ADVERTENCIA 'No especificaste un sabor, utilizando sabor "popular" por defecto.'
fi

rm -rf ${ISO_DIR}config

if [ -d "${PLANTILLAS}/${SABOR}" ]; then
	CONFIGURAR-SABOR ${SABOR}
else
	ADVERTENCIA "no se encontro ninguna plantilla para el sabor: ${SABOR}"
fi

if [ -e ${ISO_DIR}config/sabor-configurado ]; then
EXITO "Sabor: ${SABOR}"
else
ERROR 'Sabor "'${SABOR}'" desconocido o no disponible. Abortando.'
fi

;;

MEDIO)

# Establecemos medio "iso", en caso de no especificar ninguno
if [ -z ${MEDIO} ]; then
	MEDIO="iso-hybrid"
	ADVERTENCIA "No especificaste un medio, utilizando sabor $medio por defecto."
fi

case ${MEDIO} in
	usb|usb-hdd|img|USB)
		MEDIO="usb-hdd"
		TYPO_MEDIO="Dispositivos de almacenamiento extraíble (USB)"
		;;
	iso|ISO|CD|DVD)
		MEDIO="iso"
		TYPO_MEDIO="Dispositivos de almacenamiento extraíble (CD/DVD)"
		;;
	iso-hybrid|hibrido|mixto)
		MEDIO="iso-hybrid"
		TYPO_MEDIO="Dispositivo de almacenamiento extraíble (CD/DVD) con multi-arquitectura"
		;;
	*)
		ERROR 'Medio "'${MEDIO}'" no reconocido por Canaima. Abortando.'
		;;
esac

done

SEMILLA_BOOTSTRAP=${MIRROR_DEBIAN}
SEMILLA_CHROOT=${MIRROR_DEBIAN}
SEMILLA_BINARY=${MIRROR_DEBIAN}

cd ${ISO_DIR}

ADVERTENCIA "Limpiando posibles residuos de construcciones anteriores ..."
rm -rf ${ISO_DIR}.stage ${ISO_DIR}auto ${ISO_DIR}binary.log ${ISO_DIR}cache/stages_bootstrap/
lb clean

ADVERTENCIA "Generando árbol de configuraciones ..."
lb config --architecture="${arch}" \
	--distribution="${SABOR_DIST}" \
	--apt="aptitude" --apt-recommends="false" \
	--bootloader="syslinux" \
	--binary-images="${MEDIO}" \
	--bootstrap="debootstrap" \
	--binary-indices="false" \
	--includes="none" \
	--username="usuario-nvivo" \
	--hostname="${DISTRO}-${sabor}" \
	--mirror-chroot-security="none" \
	--mirror-binary-security="none" \
	--language="es" \
	--bootappend-live="locale=${LOCALE} keyb=es quiet splash vga=791 live-config.user-fullname=${DISTRO}" \
	--security="false" \
	--volatile="false" \
	--backports="false" \
	--source="false" \
	--iso-preparer="${PREPARADO_POR}" \
	--iso-volume="${DISTRO}-${sabor}" \
	--iso-publisher="${PUBLICADO_POR}" \
	--iso-application="${APLICACION}" \
	--mirror-bootstrap="${SEMILLA_BOOTSTRAP}" \
	--mirror-binary="${SEMILLA_BINARY}" \
	--mirror-chroot="${SEMILLA_CHROOT}" \
	--memtest="none" \
	--linux-flavours="${SABOR_KERNEL}" \
	--syslinux-menu="true" \
	--syslinux-timeout="5" \
	--archive-areas="${COMP_MIRROR_DEBIAN}" ${INSTALADOR} \
	--packages="${SABOR_PAQUETES}" \
	--syslinux-splash="${SABOR_SYSPLASH}" \
	--win32-loader="false" \
	--bootappend-install="locale=${LOCALE}"

sed -i 's/LB_SYSLINUX_MENU_LIVE_ENTRY=.*/LB_SYSLINUX_MENU_LIVE_ENTRY="Probar"/g' config/binary

ADVERTENCIA "Construyendo ..."
lb build 2>&1 | tee binary.log

case ${MEDIO} in
	iso) ext="iso";;
	usb) ext="img";;
	*)   ERROR "Algo fallo";;
esac


if [ -e ${ISO_DIR}binary.${ext} ]; then
	PESO=$( ls -lah ${ISO_DIR}binary.${ext} | awk '{print $5}' )
	dest="${DISTRO}-${sabor}_${arch}.${ext}"
	mv ${ISO_DIR}binary.${ext} ${dest}
	EXITO "¡Enhorabuena! Se ha creado una imagen \"${TYPO_MEDIO}\" de ${DISTRO}-${sabor}, que pesa ${PESO}."
	EXITO "Puedes encontrar la imagen \"$dest\" en el directorio ${ISO_DIR}"
	exit 0
else
	ERROR "Ocurrió un error durante la generación de la imagen."
	ERROR "Envía un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo ${ISO_DIR}binary.log"
	exit 1
fi

;;

instalar)
# En Desarrollo
# aptitude install ${SABOR_PAQUETES}
;;

probar)
# En Desarrollo
# qemu ISO
;;

gui)
# En Desarrollo
;;

--ayuda|--help|'')
# Imprimiendo la ayuda
man canaima-semilla
;;

esac
