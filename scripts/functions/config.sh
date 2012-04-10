#!/bin/sh -e

CS_CONFIG_PROFILE() {

	PROFILE="${1}"
	shift || true

	if [ -z "${PROFILE}" ]; then
		ERRORMSG "La función '%s' necesita un nombre de perfil válido como argumento." "${FUNCNAME}"
		exit 1
	fi

        cd "${ISOS}"
        if [ -d "${PCONF}" ]; then
                INFOMSG "Respaldando árbol de configuraciones previo en '%s'." "${PCONFBKP}"
                mkdir -p "${PHISTORY}"
                mv "${PCONF}" "${PCONFBKP}"
        fi

        WARNINGMSG "Limpiando residuos de construcciones anteriores ..."
        rm -rf  ${ISOS}.stage \
                ${ISOS}auto \
                ${ISOS}binary.log \
                ${ISOS}cache/stages_bootstrap

        lb clean


        WARNINGMSG "Generando árbol de configuraciones ..."
        cd "${ISOS}"

        if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
                lb config \
                --architecture="${ARCH}" \
                --linux-flavours="${KERNEL_ARCH}" \
                --distribution="${META_CODENAME}" \
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
                --iso-preparer="${CS_ISO_PREPARER}" \
                --iso-volume="${CS_ISO_VOLUME}" \
                --iso-publisher="${CS_ISO_PUBLISHER}" \
                --iso-application="${CS_ISO_APPLICATION}" \
                --memtest="none" \
                --debian-installer="${IMG_DEBIAN_INSTALLER}" \
                --win32-loader="false" \
                --bootappend-live="${CS_BOOTAPPEND_LIVE}" \
                --bootappend-install="${CS_BOOTAPPEND_INSTALL}"
                ${NULL}
        else
                lb config \
                --architecture="${ARCH}" \
                --linux-flavours="${KERNEL_ARCH}" \
                --distribution="${META_CODENAME}" \
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
                --iso-preparer="${CS_ISO_PREPARER}" \
                --iso-volume="${CS_ISO_VOLUME}" \
                --iso-publisher="${CS_ISO_PUBLISHER}" \
                --iso-application="${CS_ISO_APPLICATION}" \
                --debian-installer="${IMG_DEBIAN_INSTALLER}" \
                --win32-loader="false" \
                --memtest="none" \
                --bootappend-live="${CS_BOOTAPPEND_LIVE}" \
                --bootappend-install="${CS_BOOTAPPEND_INSTALL}"
                ${NULL}
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

