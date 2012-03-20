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

ACTION="${1}"
shift || true
BINDIR="${1}"
shift || true

# Asignando directorios de trabajo
if [ "${BINDIR}" == "/usr/bin" ]; then
        BASEDIR="/usr/share/canaima-semilla/"
        CONFDIR="/etc/canaima-semilla/"
else
        BASEDIR="$( dirname "${BINDIR}" )/"
        CONFDIR="${BASEDIR}"
fi

# Cargando valores predeterminados
. "${BASEDIR}scripts/functions/defaults.sh"

# Corriendo rutinas de inicio
. "${BASEDIR}scripts/functions/init.sh"

if [ "${ACTION}" == "construir" ]; then
	SHORTOPTS="c:a:m:s:i"
	LONGOPTS="conf:,arquitectura:,medio:,sabor:,sin-instalador"
elif [ "${ACTION}" == "build" ]; then
	SHORTOPTS="c:a:m:s:i"
	LONGOPTS="conf:,arquitectura:,medio:,sabor:,sin-instalador"
else
	ERROR "Error interno"
	exit 1
fi

OPTIONS="$( getopt --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ $? != 0 ]; then
	ERROR "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

while true; do
	case "${1}" in
		-c|--config)
			EXTRACONF="${2}"
			shift 2 || true
		;;

		-a|--arquitectura|--arch)
			ARCH="${2}"
			shift 2 || true
		;;

		-m|--medio|--)
			MEDIO="${2}"
			shift 2 || true
		;;

		-s|--sabor|--profile)
			SABOR="${2}"
			shift 2 || true
		;;

		-i|--instalador-debian|--debian-installer)
			INSTALADOR=1
			shift 1
		;;

		-I|--no-instalador-debian|--no-debian-installer)
			INSTALADOR=0
			shift 1
		;;

                --)
			shift
			break
		;;

                *)
			ERROR "Ocurrió un problema interpretando los parámetros."
			exit 1
		;;
	esac
done

PCONF="${ISODIR}config"
PCONFBKP="${ISODIR}config.${DATE}.backup"

if [ -d "${PCONF}" ]; then
        mv "${PCONF}" "${PCONFBKP}"
fi

ADVERTENCIA "Limpiando residuos de construcciones anteriores ..."
rm -rf 	${ISODIR}.stage \
	${ISODIR}auto \
	${ISODIR}binary.log \
	${ISODIR}cache/stages_bootstrap

lb clean

# INSTALADOR
case ${INSTALADOR} in
	1)
		INSTALADOR="live"
	;;

	*)
		INSTALADOR="false"
		ADVERTENCIA "No se incluirá el Instalador Debian."
	;;
esac

# ARQUITECTURA
if [ -z "${ARCH}" ]; then
	ARCH="$( dpkg --print-architecture )"
	ADVERTENCIA "No especificaste una arquitectura, utilizando \"${ARCH}\" presente en el sistema."
fi

case ${ARCH} in
	amd64|x64|64|x86_64)
		ARCH="amd64"
		KERNEL_ARCH="amd64"
		EXITO "Arquitectura: amd64"
	;;

	i386|486|686|i686)
		ARCH="i386"
		KERNEL_ARCH="686"
		EXITO "Arquitectura: i386"
	;;

	*)
		ERROR "Arquitectura \"${ARCH}\" no soportada por ${CS_NAME}. Abortando."
		exit 1
	;;
esac

# MEDIO
if [ -z "${MEDIO}" ]; then
	MEDIO="iso-hybrid"
	ADVERTENCIA "No especificaste un tipo de formato para la imagen, utilizando medio \"${MEDIO}\" por defecto."
fi

case ${MEDIO} in
	usb|usb-hdd|img|USB)
		MEDIO="usb-hdd"
		MEDIO_S="Imagen para dispositivos de almacenamiento extraíble (USB)"
		EXITO "Medio: ${MEDIO_S}"
	;;

	iso|ISO|CD|DVD)
		MEDIO="iso"
		MEDIO_S="Imagen para dispositivos ópticos de almacenamiento (CD/DVD)"
		EXITO "Medio: ${MEDIO_S}"
	;;

	iso-hybrid|hibrido|mixto|hybrid)
		MEDIO="iso-hybrid"
		MEDIO_S="Imagen mixta para dispositivos de almacenamiento (CD/DVD/USB)"
		EXITO "Medio: ${MEDIO_S}"
	;;

	*)
		ERROR "Tipo de formato \"${MEDIO}\" no reconocido por ${CS_NAME}. Abortando."
		exit 1
	;;
esac

# SABOR
if [ -z "${SABOR}" ]; then
	SABOR="popular"
	ADVERTENCIA "No especificaste un sabor, utilizando sabor \"popular\" por defecto."
fi

PCONFFILE="${PROFILES}${SABOR}/profile.conf"
PCONFIGURED="${ISODIR}config/profile-configured"

if [ -d "${PROFILES}${SABOR}" ]; then
	if [ -f "${PCONFFILE}" ]; then
		. "${PCONFFILE}"

		if [ -f "${EXTRACONF}" ]; then
			. "${EXTRACONF}"
		fi

		CS_BUILD_CONFIG "${SABOR}" "${ACTION}"
	else
		ERROR "El perfil \"${SABOR}\" no posee configuración en \"${PCONFFILE}\""
		exit 1
	fi
else
	ERROR "El perfil \"${SABOR}\" no existe dentro de la carpeta de perfiles \"${PROFILES}\"."
	exit 1
fi

if [ -f "${PCONFIGURED}" ]; then
	EXITO "Sabor: ${SABOR}"
	rm -rf "${PCONFIGURED}"
else
	ERROR "El perfil \"${SABOR}\" no logró configurarse correctamente. Abortando."
	exit 1
fi

CS_BOOTSTRAP="${MIRROR_DEBIAN}"
CS_CHROOT="${MIRROR_DEBIAN}"
CS_BINARY="${MIRROR_DEBIAN}"

ADVERTENCIA "Generando árbol de configuraciones ..."
cd ${ISODIR}
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

	--architecture="${ARCH}" \
	--distribution="${SABOR_DIST}" \
	--apt="aptitude" \
	--apt-recommends="false" \
	--bootloader="syslinux" \
	--binary-images="${MEDIO}" \
	--bootstrap="debootstrap" \
	--binary-indices="false" \
	--includes="none" \
	--username="canaima" \
	--hostname="${DISTRIBUTION}-${SABOR}" \
	--mirror-chroot-security="none" \
	--mirror-binary-security="none" \
	--language="es" \
	--bootappend-live="locale=es_VE.UTF-8 keyb=es quiet splash vga=791 live-config.user-fullname=Canaima" \
	--security="false" \
	--volatile="false" \
	--backports="false" \
	--source="false" \
	--iso-preparer="${PREPARADO_POR}" \
	--iso-volume="canaima-${SABOR}" \
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
	--bootappend-install="locale=es_VE.UTF-8"

# 	--binary-indices="false" \
# 	--language="es" \
#	--syslinux-menu="true" \
#	--syslinux-timeout="5" \
#	--syslinux-splash="${SABOR_SYSPLASH}" \

sed -i 's/LB_SYSLINUX_MENU_LIVE_ENTRY=.*/LB_SYSLINUX_MENU_LIVE_ENTRY="Probar"/g' config/binary

ADVERTENCIA "Construyendo ..."
lb build 2>&1 | tee binary.log

img_name=binary
case ${MEDIO} in
	iso-hybrid)
	     ext="iso"; img_name="$name-hybrid";;
	iso) ext="iso";;
	usb) ext="img";;
	*)   ERROR "Algo fallo";;
esac

final=${ISO_DIR}$img_name.${ext}

echo "--> $MEDIO --> $final"

if [ -e ${final} ]; then
	PESO=$( ls -lah ${final} | awk '{print $5}' )
	dest="${DISTRO}-${sabor}_${arch}.${ext}"
	mv ${final} ${dest}
	EXITO "¡Enhorabuena! Se ha creado una imagen \"${TYPO_MEDIO}\" de ${DISTRO}-${sabor}, que pesa ${PESO}."
	EXITO "Puedes encontrar la imagen \"$dest\" en el directorio ${ISO_DIR}"
	exit 0
else
	ERROR "Ocurrió un error durante la generación de la imagen."
	ERROR "Envía un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo ${ISO_DIR}binary.log"
	exit 1
fi
