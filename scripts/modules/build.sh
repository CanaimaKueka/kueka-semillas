#!/bin/sh -e
#
# ==============================================================================
# PACKAGE: canaima-semilla
# FILE: scripts/modules/build.sh
# DESCRIPCIÓN: Script de sh principal del paquete canaima-desarrollador
# COPYRIGHT:
# (C) 2010 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# (C) 2012 Niv Sardi <xaiki@debian.org>
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
	SHORTOPTS="c:a:m:s:iId"
	LONGOPTS="config:,arquitectura:,medio:,sabor:,instalador-debian,no-instalador-debian,debug"
elif [ "${ACTION}" == "build" ]; then
	SHORTOPTS="c:a:m:s:iId"
	LONGOPTS="config:,architecture:,image:,profile:,debian-installer,no-debian-installer,debug"
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

CONFIGONLY="true"
BUILDONLY="true"
INSTALADOR="true"

while true; do
	case "${1}" in
		-f|--config-file|--archivo-config)
			EXTRACONF="${2}"
			shift 2 || true
		;;

		-a|--arquitectura|--architecture)
			ARCH="${2}"
			shift 2 || true
		;;

		-m|--medio|--image)
			MEDIO="${2}"
			shift 2 || true
		;;

		-s|--sabor|--profile)
			SABOR="${2}"
			shift 2 || true
		;;

		-i|--instalador|--installer)
			INSTALADOR="true"
			shift 1 || true
		;;

		-n|--sin-instalador|--no-installer)
			INSTALADOR="false"
			shift 1 || true
		;;

		-b|--build-only|--solo-construir)
			BUILDONLY="true"
			CONFIGONLY="false"
			shift 1 || true
		;;

		-o|--config-only|--solo-configurar)
			CONFIGONLY="true"
			BUILDONLY="false"
			shift 1 || true
		;;

		-d|--debug)
			DEBUG="true"
			shift 1 || true
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

cd "${ISOS}"

if ${CONFIGONLY}; then

	if [ -z "${SABOR}" ]; then
		SABOR="${DEFAULT_PROFILE}"
		ADVERTENCIA "No especificaste un sabor, utilizando sabor '%s' por defecto." "${SABOR}"
	fi

	if [ -z "${ARCH}" ]; then
		ARCH="$( dpkg --print-architecture )"
		ADVERTENCIA "No especificaste una arquitectura, utilizando '%s' presente en el sistema." "${ARCH}"
	fi

	if [ -z "${MEDIO}" ]; then
		MEDIO="iso-hybrid"
		ADVERTENCIA "No especificaste un tipo de formato para la imagen, utilizando medio '%s' por defecto." "${MEDIO}"
	fi

	PCONF="${ISOS}config"
	PCONFBKP="${ISOS}config.${DATE}.backup"
	PCONFFILE="${PROFILES}${SABOR}/profile.conf"
	PCONFIGURED="${ISOS}config/profile-configured"

	if [ -d "${PROFILES}${SABOR}" ]; then
		if [ -f "${PCONFFILE}" ]; then
			. "${PCONFFILE}"
		fi
	fi

	if [ -d "${PCONF}" ]; then
		mv "${PCONF}" "${PCONFBKP}"
	fi

	cd "${ISOS}"

	ADVERTENCIA "Limpiando residuos de construcciones anteriores ..."
	rm -rf 	${ISOS}.stage \
		${ISOS}auto \
		${ISOS}binary.log \
		${ISOS}cache/stages_bootstrap

	lb clean

	# INSTALADOR
	if [ "${IMG_DEBIAN_INSTALLER}" = "live" ] && [ "${INSTALADOR}" = "false" ]; then
		ADVERTENCIA "El perfil incluye el instalador, pero la línea de comandos lo excluye."
		ADVERTENCIA "Prefiriendo la linea de comandos sobre el perfil."
		INSTALADOR="false"
	elif [ "${IMG_DEBIAN_INSTALLER}" = "false" ] && [ "${INSTALADOR}" = "live" ]; then
		ADVERTENCIA "El perfil excluye el instalador, pero la línea de comandos lo incluye."
		ADVERTENCIA "Prefiriendo la linea de comandos sobre el perfil."
		INSTALADOR="live"
	elif [ "${IMG_DEBIAN_INSTALLER}" = "false" ] && [ "${INSTALADOR}" = "false" ]; then
		ADVERTENCIA "No se incluirá el instalador."
		INSTALADOR="false"
	elif [ "${IMG_DEBIAN_INSTALLER}" = "live" ] && [ "${INSTALADOR}" = "live" ]; then
		ADVERTENCIA "Se incluye el instalador."
		INSTALADOR="live"
	else
		ADVERTENCIA "No se incluirá el instalador."
		INSTALADOR="false"
	fi

	# METADISTRIBUCIÓN 
	case ${META_DISTRO} in
		debian)
			META_MODE="debian"
			EXITO "Metadistribución: Debian"
		;;

		canaima)
			META_MODE="canaima"
			EXITO "Metadistribución: Canaima"
		;;

		ubuntu)
			META_MODE="ubuntu"
			EXITO "Metadistribución: Ubuntu"
		;;

		''|*)
			META_MODE="debian"
			META_DISTRO="debian"
			ADVERTENCIA "Metadistribución '%s' no soportada por %s. Utilizando Debian." "${META_DISTRO}" "${CS_NAME}"
		;;
	esac

	#ARQUITECTURA
	case ${ARCH} in
		amd64)
			ARCH="amd64"
			KERNEL_ARCH="amd64"
			EXITO "Arquitectura: amd64"
		;;

		i386)
			ARCH="i386"
			KERNEL_ARCH="686"
			EXITO "Arquitectura: i386"
		;;

		*)
			ERROR "Arquitectura '%s' no soportada por %s. Abortando." "${ARCH}" "${CS_NAME}"
			exit 1
		;;
	esac

	# MEDIO
	case ${MEDIO} in
		usb|usb-hdd|img|USB)
			if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
				MEDIO="hdd"
			else
				MEDIO="usb-hdd"
			fi
			MEDIO_LBNAME="binary.img"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}_${ARCH}.img"
			MEDIO_S="Imagen para dispositivos de almacenamiento extraíble (USB)"
			EXITO "Medio: %s" "${MEDIO_S}"
		;;

		iso|ISO|CD|DVD)
			MEDIO="iso"
			MEDIO_LBNAME="binary.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}_${ARCH}.iso"
			MEDIO_S="Imagen para dispositivos ópticos de almacenamiento (CD/DVD)"
			EXITO "Medio: %s" "${MEDIO_S}"
		;;

		iso-hybrid|hibrido|mixto|hybrid)
			MEDIO="iso-hybrid"
			MEDIO_LBNAME="binary-hybrid.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}_${ARCH}.iso"
			MEDIO_S="Imagen mixta para dispositivos de almacenamiento (CD/DVD/USB)"
			EXITO "Medio: %s" "${MEDIO_S}"
		;;

		*)
			ERROR "Tipo de formato '%s' no reconocido por %s. Abortando." "${MEDIO}" "${CS_NAME}"
			exit 1
		;;
	esac

	if [ -d "${PROFILES}${SABOR}" ]; then
		if [ -f "${PCONFFILE}" ]; then
			if [ -f "${EXTRACONF}" ]; then
				. "${EXTRACONF}"
			fi

			CS_BUILD_CONFIG "${SABOR}" "${ACTION}"
		else
			ERROR "El perfil '%s' no posee configuración en '%s'" "${SABOR}" "${PCONFFILE}"
			exit 1
		fi
	else
		ERROR "El perfil '%s' no existe dentro de la carpeta de perfiles '%s'." "${SABOR}" "${PCONFFILE}"
		exit 1
	fi

	if [ -f "${PCONFIGURED}" ]; then
		EXITO "Sabor: %s" "${SABOR}"
	else
		ERROR "El perfil '%s' no logró configurarse correctamente. Abortando." "${SABOR}"
		exit 1
	fi

	ADVERTENCIA "Generando árbol de configuraciones ..."
	cd "${ISOS}"

	if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
		lb config \
		--architecture="${ARCH}" \
		--linux-flavours="${KERNEL_ARCH}" \
		--distribution="${META_DISTRO}" \
		--mode="${META_MODE}" \
		--language="${OS_LANG}" \
		--apt="aptitude" \
		--apt-recommends="false" \
		--apt-indices="none" \
		--apt-secure="false" \
		--bootloader="syslinux" \
		--binary-images="${MEDIO}" \
		--bootstrap="debootstrap" \
		--includes="none" \
		--hostname="${META_DISTRO}-${SABOR}" \
		--username="${META_DISTRO}" \
		--archive-areas="${META_REPOSECTIONS}"
		--parent-mirror-bootstrap="${META_REPO}" \
		--parent-mirror-chroot="${META_REPO}" \
		--parent-mirror-binary="${META_REPO}" \
		--parent-mirror-debian-installer="${META_REPO}" \
		--mirror-bootstrap="${META_REPO}" \
		--mirror-chroot="${META_REPO}" \
		--mirror-binary="${META_REPO}" \
		--mirror-debian-installer="${META_REPO}" \
		--parent-mirror-chroot-security="none" \
		--parent-mirror-chroot-volatile="none" \
		--parent-mirror-chroot-backports="none" \
		--parent-mirror-binary-security="none" \
		--parent-mirror-binary-volatile="none" \
		--parent-mirror-binary-backports="none" \
		--mirror-chroot-security="none" \
		--mirror-chroot-volatile="none" \
		--mirror-chroot-backports="none" \
		--mirror-binary-security="none" \
		--mirror-binary-volatile="none" \
		--mirror-binary-backports="none" \
		--security="false" \
		--volatile="false" \
		--backports="false" \
		--source="false" \
		--iso-preparer="${IDSTRING}" \
		--iso-volume="${META_DISTRO}-${SABOR} (${DATE})" \
		--iso-publisher="${AUTHOR_NAME}; ${AUTHOR_EMAIL}; ${AUTHOR_URL}" \
		--iso-application="${META_DISTRO} Live" \
		--memtest="none" \
		--debian-installer="${INSTALADOR}" \
		--win32-loader="false" \
		--bootappend-live="locale=${LOCALE} keyb=${OS_LANG} quiet splash vga=791 live-config.user-fullname=${META_DISTRO}" \
		--bootappend-install="locale=${LOCALE}" \
		${NULL}
	else
		lb config \
		--architecture="${ARCH}" \
		--linux-flavours="${KERNEL_ARCH}" \
		--distribution="${META_DISTRO}" \
		--mode="${META_MODE}" \
		--language="${OS_LANG}" \
		--apt="aptitude" \
		--apt-recommends="false" \
		--apt-secure="false" \
		--bootloader="syslinux" \
		--syslinux-menu="true" \
		--syslinux-timeout="5" \
		--syslinux-splash="${IMG_SYSLINUX_SPLASH}" \
		--binary-images="${MEDIO}" \
		--bootstrap="debootstrap" \
		--binary-indices="false" \
		--includes="none" \
		--username="${META_DISTRO}" \
		--hostname="${META_DISTRO}-${SABOR}" \
		--archive-areas="${META_REPOSECTIONS}"
		--mirror-chroot="${META_REPO}" \
		--mirror-binary="${META_REPO}" \
		--mirror-debian-installer="${META_REPO}" \
		--mirror-chroot-security="none" \
		--mirror-chroot-volatile="none" \
		--mirror-chroot-backports="none" \
		--mirror-binary-security="none" \
		--mirror-binary-volatile="none" \
		--mirror-binary-backports="none" \
		--security="false" \
		--volatile="false" \
		--backports="false" \
		--source="false" \
		--iso-preparer="${IDSTRING}" \
		--iso-volume="${META_DISTRO}-${SABOR} (${DATE})" \
		--iso-publisher="${AUTHOR_NAME}; ${AUTHOR_EMAIL}; ${AUTHOR_URL}" \
		--iso-application="${META_DISTRO} Live" \
		--debian-installer="${INSTALADOR}" \
		--win32-loader="false" \
		--memtest="none" \
		--bootappend-live="locale=${OS_LOCALE} keyb=${OS_LANG} quiet splash vga=791 live-config.user-fullname=${META_DISTRO}" \
		--bootappend-install="locale=${OS_LOCALE}"
		${NULL}
	fi
fi

if ${BUILDONLY}; then
	cd "${ISOS}"

	if [ ! -e "${ISOS}config/profile-configured" ]; then
		ADVERTENCIA "El directorio de construcción no fué configurado por ${CS_NAME}, ¡Buena Suerte!"
	fi

	ADVERTENCIA "Construyendo ..."
	lb build 2>&1 | tee "${ISOS}${LOGFILE}"

	. "${ISOS}config/bootstrap"
	. "${ISOS}config/binary"
	. "${ISOS}config/common"

	ARCH="${LB_ARCHITECTURES}"
	MEDIO="${LB_BINARY_IMAGES}"
	META_DISTRO="${LB_MODE}"
	SABOR="${LB_DISTRIBUTION}"

	case ${MEDIO} in
		usb-hdd|hdd)
			MEDIO_LBNAME="binary.img"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}_${ARCH}.img"
		;;

		iso)
			MEDIO_LBNAME="binary.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}_${ARCH}.iso"
		;;

		iso-hybrid)
			MEDIO_LBNAME="binary-hybrid.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}_${ARCH}.iso"
		;;
	esac
fi

if [ -e "${ISOS}${MEDIO_LBNAME}" ]; then
	PESO="$( ls -lah "${ISOS}${MEDIO_LBNAME}" | awk '{print $5}' )"
	mv "${ISOS}${MEDIO_LBNAME}" "${ISOS}${MEDIO_CSNAME}"
	EXITO "¡Felicitaciones! Has creado una imagen '%s' para %s-%s, con un peso de %s." "${MEDIO}" "${META_DISTRO}" "${SABOR}" "${PESO}"
	EXITO "Puedes encontrar la imagen '%s' en el directorio %s" "${MEDIO_CSNAME}" "${ISOS}"
	exit 0
else
	ERROR "Ocurrió un error durante la generación de la imagen."
	ERROR "Envía un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo '%s'" "${ISOS}${LOGFILE}"
	exit 1
fi
