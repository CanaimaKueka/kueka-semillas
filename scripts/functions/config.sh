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

CS_LOAD_PROFILE() {

	PCONFFILE="${1}"
	shift || true

	if [ -z "${PCONFFILE}" ]; then
		ERROR "La función '%s' necesita un nombre de perfil válido como argumento." "${FUNCNAME}"
		exit 1
	fi

	if [ -e "${PCONFFILE}" ]; then
		. "${PCONFFILE}"	
	else
		ERROR "El archivo de configuraciones '%s' no existe." "${PCONFFILE}"
		exit 1
	fi

	if [ -z "${AUTHOR_NAME}" ]; then AUTHOR_NAME="Anonymous Developer";
	elif [ "${AUTHOR_NAME}" = "none" ]; then AUTHOR_NAME=""; fi

	if [ -z "${AUTHOR_EMAIL}" ]; then AUTHOR_EMAIL="desarrolladores@canaima.softwarelibre.gob.ve";
	elif [ "${AUTHOR_EMAIL}" = "none" ]; then AUTHOR_EMAIL=""; fi

	if [ -z "${AUTHOR_URL}" ]; then AUTHOR_URL="http://canaima.softwarelibre.gob.ve/";
	elif [ "${AUTHOR_URL}" = "none" ]; then AUTHOR_URL=""; fi

	if [ -z "${META_DISTRO}" ] || [ "${META_DISTRO}" = "none" ]; then
		META_DISTRO="$( echo "$( lsb_release -s -i )" | tr '[:upper:]' '[:lower:]' )"
	fi

	if [ -z "${META_CODENAME}" ] || [ "${META_CODENAME}" = "none" ]; then
		META_CODENAME="$( echo "$( lsb_release -s -i )" | tr '[:upper:]' '[:lower:]' )"
	fi

	case ${META_DISTRO} in
		debian)
			META_MODE="${META_MODE:-debian}"

			if [ -z "${META_REPO}" ] || [ "${META_REPO}" = "none" ]; then
				META_REPO="${META_REPO:-http://ftp.us.debian.org/debian/}"
			fi

			if [ -z "${META_REPOSECTIONS}" ] || [ "${META_REPOSECTIONS}" = "none" ]; then
				META_REPOSECTIONS="${META_REPOSECTIONS:-main contrib non-free}"
			fi
		;;

		canaima)
			META_MODE="${META_MODE:-debian}"

			if [ -z "${META_REPO}" ] || [ "${META_REPO}" = "none" ]; then
				META_REPO="${META_REPO:-http://paquetes.canaima.softwarelibre.gob.ve/}"
			fi

			if [ -z "${META_REPOSECTIONS}" ] || [ "${META_REPOSECTIONS}" = "none" ]; then
				META_REPOSECTIONS="${META_REPOSECTIONS:-main contrib extra privativo}"
			fi
		;;

		ubuntu)
			META_MODE="${META_MODE:-ubuntu}"

			if [ -z "${META_REPO}" ] || [ "${META_REPO}" = "none" ]; then
				META_REPO="${META_REPO:-http://archive.ubuntu.com/ubuntu/}"
			fi

			if [ -z "${META_REPOSECTIONS}" ] || [ "${META_REPOSECTIONS}" = "none" ]; then
				META_REPOSECTIONS="${META_REPOSECTIONS:-main restricted}"
			fi
		;;

		'')
			ERROR "Debe especificar una Metadistribución. Abortando."
			exit 1
		;;

		*)
			ERROR "Metadistribución '%s' no soportada por %s. Abortando." "${META_DISTRO}" "${CS_NAME}"
			exit 1
		;;
	esac

OS_PACKAGES="${OS_PACKAGES:-gnome-core xorg}"
OS_BOOTLOADER="${OS_BOOTLOADER:-grub}"
OS_LOCALE="${OS_LOCALE:-${LC_ALL}}"
OS_LANG="${OS_LANG:-$( echo "${OS_LOCALE}" | sed 's/_.*//g' )}"
OS_INCLUDES="${OS_INCLUDES:-${PROFILES}${DEFAULT_PROFILE}/OS_INCLUDES/}"
OS_HOOKS="${OS_HOOKS:-${PROFILES}${DEFAULT_PROFILE}/OS_HOOKS/}"

IMG_POOL_PACKAGES="${IMG_POOL_PACKAGES:-grub grub-pc}"
IMG_SYSLINUX_SPLASH="${IMG_SYSLINUX_SPLASH:-${TEMPLATES}profiles/${DEFAULT_PROFILE}/syslinux.png}"
IMG_DEBIAN_INSTALLER="${IMG_DEBIAN_INSTALLER:-false}"
IMG_DEBIAN_INSTALLER_BANNER="${IMG_DEBIAN_INSTALLER_BANNER:-${PROFILES}${DEFAULT_PROFILE}/DEBIAN_INSTALLER/banner.png}"
IMG_DEBIAN_INSTALLER_PRESEED="${IMG_DEBIAN_INSTALLER_PRESEED:-${PROFILES}${DEFAULT_PROFILE}/DEBIAN_INSTALLER/preseed.cfg}"
IMG_DEBIAN_INSTALLER_GTK="${IMG_DEBIAN_INSTALLER_GTK:-${PROFILES}${DEFAULT_PROFILE}/DEBIAN_INSTALLER/gtkrc}"
IMG_INCLUDES="${IMG_INCLUDES:-${PROFILES}${DEFAULT_PROFILE}/IMG_INCLUDES/}"
IMG_HOOKS="${IMG_HOOKS:-${PROFILES}${DEFAULT_PROFILE}/IMG_HOOKS/}"

}

CS_CONFIG_PROFILE() {

	PROFILE="${1}"
	shift || true

	if [ -z "${PROFILE}" ]; then
		ERROR "La función '%s' necesita un nombre de perfil válido como argumento." "${FUNCNAME}"
		exit 1
	fi

	if [ -d "${TEMPLATES}syslinux" ]
		mkdir -p "${ISOS}config/templates"
		cp -r "${TEMPLATES}syslinux" "${ISOS}config/templates/"
	fi

	if [ -f "${PROFILES}${PROFILE}/syslinux.png" ]; then
		mkdir -p "${ISOS}config/binary_syslinux"
		cp "${PROFILES}${PROFILE}/syslinux.png" "${ISOS}config/binary_syslinux/splash.png"
		cp "${PROFILES}${PROFILE}/syslinux.png" "${ISOS}config/templates/syslinux/menu/splash.png"
	elif [ -d "${TEMPLATES}syslinux/menu/splash.png" ]
		mkdir -p "${ISOS}config/binary_syslinux"
		cp "${TEMPLATES}syslinux/menu/splash.png" "${ISOS}config/binary_syslinux/splash.png"
		cp "${TEMPLATES}syslinux/menu/splash.png" "${ISOS}config/templates/syslinux/menu/splash.png"
	fi

	IMG_SYSLINUX_SPLASH="${ISOS}config/binary_syslinux/splash.png"

	if [ -d "${PROFILES}${PROFILE}/IMG_INCLUDES" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
			mkdir -p "${ISOS}config/includes.binary"
			cp -r "${PROFILES}${PROFILE}/IMG_INCLUDES/*" "${ISOS}config/includes.binary/"
		else
			mkdir -p "${ISOS}config/binary_local-includes"
			cp -r "${PROFILES}${PROFILE}/IMG_INCLUDES/*" "${ISOS}config/binary_local-includes/"
		fi
	fi

	if [ -d "${PROFILES}${PROFILE}/OS_INCLUDES" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
		       	mkdir -p "${ISOS}config/includes.chroot"
			cp -r "${PROFILES}${PROFILE}/OS_INCLUDES/*" "${ISOS}config/includes.chroot/"
		else
		       	mkdir -p "${ISOS}config/chroot_local-includes"
			cp -r "${PROFILES}${PROFILE}/OS_INCLUDES/*" "${ISOS}config/chroot_local-includes/"
		fi
	fi

	if [ -d "${PROFILES}${PROFILE}/IMG_HOOKS" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
			mkdir -p "${ISOS}config/hooks"
			for HOOK in "${PROFILES}${PROFILE}/IMG_HOOKS/*"; do
				cp -r "${HOOK}" "${ISOS}config/hooks/$( basename "${HOOK}").binary"
			done
		else
			mkdir -p "${ISOS}config/binary_local-hooks"
			cp -r "${PROFILES}${PROFILE}/IMG_HOOKS/*" "${ISOS}config/binary_local-hooks/"
		fi
	fi

	if [ -d "${PROFILES}${PROFILE}/OS_HOOKS" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
			mkdir -p "${ISOS}config/hooks"
			for HOOK in "${PROFILES}${PROFILE}/OS_HOOKS/*"; do
				cp -r "${HOOK}" "${ISOS}config/hooks/$( basename "${HOOK}").chroot"
			done
		else
			mkdir -p "${ISOS}config/chroot_local-hooks"
			cp -r "${PROFILES}${PROFILE}/OS_HOOKS/*" "${ISOS}config/chroot_local-hooks/"
		fi
	fi

	if [ -f "${PROFILES}${PROFILE}/extra-repos.list" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
			mkdir -p "${ISOS}config/archives"
			cp "${PROFILES}${PROFILE}/extra-repos.list" "${ISOS}config/archives/sources.list.binary"
			cp "${PROFILES}${PROFILE}/extra-repos.list" "${ISOS}config/archives/sources.list.chroot"
		else
			mkdir -p "${ISOS}config/chroot_sources"
			cp "${PROFILES}${PROFILE}/extra-repos.list" "${ISOS}config/chroot_sources/sources.binary"
			cp "${PROFILES}${PROFILE}/extra-repos.list" "${ISOS}config/chroot_sources/sources.chroot"
		fi
	fi

	if [ -n "${OS_PACKAGES}" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
			mkdir -p "${ISOS}config/package-lists"
			echo "${OS_PACKAGES}" >> "${ISOS}config/package-lists/packages.list.chroot"
		else
			mkdir -p "${ISOS}config/chroot_local-packageslists"
			echo "${OS_PACKAGES}" >> "${ISOS}config/chroot_local-packageslists/packages.list"
		fi
	fi

	if [ -n "${IMG_POOL_PACKAGES}" ]; then
		if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
			mkdir -p "${ISOS}config/package-lists"
			echo "${IMG_POOL_PACKAGES}" >> "${ISOS}config/package-lists/packages.list.binary"
		else
			mkdir -p "${ISOS}config/binary_local-packageslists"
			echo "${IMG_POOL_PACKAGES}" >> "${ISOS}config/binary_local-packageslists/packages.list"
		fi
	fi

	if [ "${IMG_DEBIAN_INSTALLER}" = "true" ]; then
		if [ -e "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/banner.png" ]; then
			mkdir -p "${ISOS}config/binary_debian-installer-includes/usr/share/graphics"
			cp "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/banner.png" "${ISOS}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png"
		elif [ -n "${IMG_DEBIAN_INSTALLER_BANNER}" ] && [ -e "${IMG_DEBIAN_INSTALLER_BANNER}" ]; then
			mkdir -p "${ISOS}config/binary_debian-installer-includes/usr/share/graphics"
			cp "${IMG_DEBIAN_INSTALLER_BANNER}" "${ISOS}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png"
		elif [ -e "${TEMPLATES}/profile/DEBIAN_INSTALLER/banner.png" ]; then
			mkdir -p "${ISOS}config/binary_debian-installer-includes/usr/share/graphics"
			cp "${TEMPLATES}/profile/DEBIAN_INSTALLER/banner.png" "${ISOS}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png"
		fi

		if [ -e "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/preseed.cfg" ]; then
			mkdir -p "${ISOS}config/binary_debian-installer"
			cp "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/preseed.cfg" "${ISOS}config/binary_debian-installer/preseed.cfg"
		fi

		if [ -e "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/gtkrc" ]; then
			mkdir -p "${ISOS}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0"
			cp "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/gtkrc" "${ISOS}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0/gtkrc"
		fi
	fi

sed -i 's/LB_SYSLINUX_MENU_LIVE_ENTRY=.*/LB_SYSLINUX_MENU_LIVE_ENTRY="Probar"/g' config/binary

echo "${1}" > ${ISO_DIR}config/sabor-configurado
}

