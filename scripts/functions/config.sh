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
		ERROR "La función '%s' necesita un nombre de perfil válido como argumento." "${FUNCNAME}"
	fi

	if [ -f "${PROFILES}${PROFILE}/syslinux.png" ]; then
		mkdir -p "${ISOS}config/binary_syslinux"
		cp "${PROFILES}${PROFILE}/syslinux.png" "${ISOS}config/binary_syslinux/splash.png"
		IMG_SYSLINUX_SPLASH="config/binary_syslinux/splash.png"
	fi

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

	if [ -e "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/banner.png" ]; then
		mkdir -p "${ISOS}config/binary_debian-installer-includes/usr/share/graphics"
		cp "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/banner.png" "${ISOS}config/binary_debian-installer-includes/usr/share/graphics/logo_debian.png"
	fi

	if [ -e "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/preseed.cfg" ]; then
		mkdir -p "${ISOS}config/binary_debian-installer"
		cp "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/preseed.cfg" "${ISOS}config/binary_debian-installer/preseed.cfg"
	fi

	if [ -e "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/gtkrc" ]; then
		mkdir -p "${ISOS}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0"
		cp "${PROFILES}${PROFILE}/DEBIAN_INSTALLER/gtkrc" "${ISOS}config/binary_debian-installer-includes/usr/share/themes/Clearlooks/gtk-2.0/gtkrc"
	fi


sed -i 's/LB_SYSLINUX_MENU_LIVE_ENTRY=.*/LB_SYSLINUX_MENU_LIVE_ENTRY="Probar"/g' config/binary

echo "${1}" > ${ISO_DIR}config/sabor-configurado
}

