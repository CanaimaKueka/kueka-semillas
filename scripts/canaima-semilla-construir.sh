#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla-construir
# ARCHIVO: canaima-semilla-construir.sh
# DESCRIPCIÓN: Script de sh principal del paquete canaima-desarrollador
# COPYRIGHT:
#  © 2010 Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
#  © 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL3
# ==============================================================================
#
# Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los
# términos de la Licencia Pública General de GNU (versión 3).

# Inicializando variables
. ${VARIABLES}

# Cargando funciones
. ${FUNCIONES}

TEMP=`getopt -o c:a:m:s:iI --long conf:,arquitectura:,medio:,sabor:,instalador,no-instalador -n $0 -- "$@"`

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$TEMP"

install=1

while true; do
	case "$1" in
		-c|--conf) echo "Cargando $2"; . $2; shift 2;;
		-a|--arquitectura) arch=$2;       shift 2;;
		-m|--medio)        medio=$2;      shift 2;;
		-s|--sabor)        sabor=$2;      shift 2;;
		-i|--instalador)      install=1;  shift 1;;
		-I|--no-instalador)   install=""; shift 1;;
                --) shift ; break ;;
                *) echo "Internal error!" ; exit 1 ;;
	esac
done

#INSTALADOR
case ${install} in
	1) INSTALADOR="--debian-installer=live";;
	*)
		INSTALADOR="--debian-installer=false"
		ADVERTENCIA 'No se incluirá el instalador.'
		;;
esac

#ARQUITECTURA
if [ -z ${arch} ]; then
	arch=`dpkg --print-architecture`
	ADVERTENCIA "No especificaste una arquitectura, utilizando \"$arch\" presente en el sistema."
fi

SABOR_KERNEL=$arch

case ${arch} in
	i386)  SABOR_KERNEL=686;;
	amd64) SABOR_KERNEL=amd64;;
	*)     ERROR "Arquitectura \"$arch\" no soportada en Canaima. Abortando.";;
esac

#SABOR
if [ -z ${sabor} ]; then
	if [ -z ${SABOR} ]; then
		sabor="popular"
		ADVERTENCIA 'No especificaste un sabor, utilizando sabor "popular" por defecto.'
	else
		sabor=${SABOR}
	fi
elif [ -n ${SABOR} -a ${sabor} != ${SABOR} ]; then
	ADVERTENCIA "La configuración tiene el sabor '$SABOR', pero la linea de comando especifico '$sabor', preferiendo '$sabor'."
fi

if [ -f ${ISO_DIR}config ]; then
	mv ${ISO_DIR}config ${ISO_DIR}config.bak
fi
rm -rf ${ISO_DIR}config

if [ -d "${PLANTILLAS}/$sabor" ]; then
	CONFIGURAR_SABOR $sabor
else
	ADVERTENCIA "no se encontro ninguna plantilla para el sabor: $sabor"
fi

if [ -e ${ISO_DIR}config/sabor-configurado ]; then
EXITO "Sabor: ${sabor}"
else
ERROR 'Sabor "'${sabor}'" desconocido o no disponible. Abortando.'
fi

# Establecemos medio "iso", en caso de no especificar ninguno
if [ -z ${medio} ]; then
	medio="iso-hybrid"
	ADVERTENCIA "No especificaste un medio, utilizando sabor $medio por defecto."
fi

case ${medio} in
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

EXITO "Medio: ${TYPO_MEDIO}"

SEMILLA_BOOTSTRAP=${MIRROR_DEBIAN}
SEMILLA_CHROOT=${MIRROR_DEBIAN}
SEMILLA_BINARY=${MIRROR_DEBIAN}

if [ ! -d ${ISO_DIR} ]; then
	ADVERTENCIA "${ISO_DIR} no existe, creando"
	mkdir -p ${ISO_DIR}
fi

cd ${ISO_DIR}

ADVERTENCIA "Limpiando posibles residuos de construcciones anteriores ..."
rm -rf ${ISO_DIR}.stage ${ISO_DIR}auto ${ISO_DIR}binary.log ${ISO_DIR}cache/stages_bootstrap/
lb clean

if [ ! -z "$SABOR_PAQUETES" ]; then
	mkdir -p config/package-lists
	echo ${SABOR_PAQUETES} | xargs -n1 > config/package-lists/${DISTRO}-${sabor}.list
#	pkglist_arg="--package-lists=${DISTRO}-${sabor}"
else
	ADVERTENCIA "No tiene paquetes especificos, esta seguro ?"
fi
ADVERTENCIA "Generando árbol de configuraciones ..."
lb config --architecture="${arch}" \
	--distribution="${SABOR_DIST}" \
	--apt="aptitude" --apt-recommends="false" \
	--bootloader="syslinux" \
	--binary-images="${MEDIO}" \
	--bootstrap="debootstrap" \
	--includes="none" \
	--username="usuario-nvivo" \
	--hostname="${DISTRO}-${sabor}" \
	--mirror-chroot-security="none" \
	--mirror-binary-security="none" \
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
	--archive-areas="${COMP_MIRROR_DEBIAN}" ${INSTALADOR} \
	--win32-loader="false" \
	--bootappend-install="locale=${LOCALE}" \
	${NULL}

# 	--binary-indices="false" \
# 	--language="es" \
#	--syslinux-menu="true" \
#	--syslinux-timeout="5" \
#	--syslinux-splash="${SABOR_SYSPLASH}" \

sed -i 's/LB_SYSLINUX_MENU_LIVE_ENTRY=.*/LB_SYSLINUX_MENU_LIVE_ENTRY="Probar"/g' config/binary

ADVERTENCIA "Construyendo ..."
lb build 2>&1 | tee binary.log

case ${medio} in
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
