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

	SABOR="${1}"
	shift || true

	PCONFFILE="${1}"
	shift || true

	if [ -z "${PCONFFILE}" ]; then
		ERRORMSG "La función '%s' necesita un nombre de perfil válido como argumento." "${FUNCNAME}"
		exit 1
	fi

	if [ -e "${PCONFFILE}" ]; then
		. "${PCONFFILE}"	
	else
		ERRORMSG "El archivo de configuraciones '%s' no existe." "${PCONFFILE}"
		exit 1
	fi

	CONFIGMSG "Leyendo estado del nombre del autor" "AUTHOR_NAME"
	if [ -z "${AUTHOR_NAME}" ] || [ "${AUTHOR_NAME}" = "none" ]; then
		AUTHOR_NAME="${CS_NAME}"
		WARNINGMSG "No se ha especificado el nombre del autor para el sabor en construcción."
	fi
	INFOMSG "Seleccionando '%s' para identificar al autor del sabor." "${AUTHOR_NAME}"
	DEBUGMSG "AUTHOR_NAME"

	CONFIGMSG "Leyendo estado del correo electrónico del autor" "AUTHOR_EMAIL"
	if [ -z "${AUTHOR_EMAIL}" ] || [ "${AUTHOR_EMAIL}" = "none" ]; then
		AUTHOR_EMAIL="desarrolladores@canaima.softwarelibre.gob.ve"
		WARNINGMSG "No se ha especificado un correo para el autor del sabor en construcción."
	fi
	INFOMSG "Seleccionando '%s' como correo para el autor del sabor." "${AUTHOR_EMAIL}"
	DEBUGMSG "AUTHOR_EMAIL"

	CONFIGMSG "Leyendo estado de la dirección web del autor" "AUTHOR_URL"
	if [ -z "${AUTHOR_URL}" ] || [ "${AUTHOR_URL}" = "none" ]; then
		AUTHOR_URL="http://canaima.softwarelibre.gob.ve/"
		WARNINGMSG "No se ha especificado una dirección web para el autor del sabor en construcción."
	fi
	INFOMSG "Seleccionando '%s' como dirección web para el autor del sabor." "${AUTHOR_URL}"
	DEBUGMSG "AUTHOR_URL"

	CONFIGMSG "Leyendo estado del lenguaje de sistema" "OS_LOCALE"
	if [ -z "${OS_LOCALE}" ] || [ "${OS_LOCALE}" = "none" ]; then
		OS_LOCALE="${LC_ALL}"
		WARNINGMSG "No se ha definido un lenguaje de sistema para el sabor en construcción."
	fi
	if [ $( cat "${SUPPORTED_LOCALES}" | grep -wc "${OS_LOCALE}" ) = 0 ]; then
		ERRORMSG "El lenguaje de sistema '%s' no está soportado por %s." "${OS_LOCALE}" "${CS_NAME}"
		exit 1
	fi
	INFOMSG "Seleccionando '%s' como lenguaje de sistema para el sabor en construcción." "${OS_LOCALE}"
	DEBUGMSG "OS_LOCALE"

	CONFIGMSG "Leyendo estado de la Metadistribución base" "META_DISTRO"
	case "$( echo ${META_DISTRO} | tr '[:upper:]' '[:lower:]' )" in
		debian)		META_MODE="debian";;
		ubuntu)		META_MODE="ubuntu";;
		canaima)	META_MODE="debian";;
		*)
			ERRORMSG "Metadistribución '%s' no soportada por %s. Abortando." "${META_DISTRO}" "${CS_NAME}"
			exit 1
		;;
	esac
	INFOMSG "Seleccionando Metadistribución base '%s' para la construcción del sistema." "${META_DISTRO}"
	DEBUGMSG "META_DISTRO"

	CONFIGMSG "Leyendo estado de la versión para la Metadistribución base" "META_CODENAME"
	if [ -z "${META_CODENAME}" ] || [ "${META_CODENAME}" = "none" ]; then
		eval "META_CODENAME=\${$( echo ${META_DISTRO} | tr '[:lower:]' '[:upper:]' )_DEFAULT_CODENAME}"
		WARNINGMSG "No se ha especificado una versión para la Metadistribución base."
	fi
	INFOMSG "Seleccionando '%s' como versión de la Metadistribución base." "${META_CODENAME}"
	DEBUGMSG "META_CODENAME"

	CONFIGMSG "Leyendo estado del repositorio para la Metadistribución base" "META_REPO"
	if [ -z "${META_REPO}" ] || [ "${META_REPO}" = "none" ]; then
		eval "META_REPO=\${$( echo ${META_DISTRO} | tr '[:lower:]' '[:upper:]' )_DEFAULT_REPO}"
		WARNINGMSG "No se ha especificado un repositorio para la Metadistribución base."
	fi
	INFOMSG "Seleccionando '%s' como repositorio para la Metadistribución base." "${META_REPO}"
	DEBUGMSG "META_REPO"

	CONFIGMSG "Leyendo estado de las secciones para el repositorio de la Metadistribución base" "META_REPOSECTIONS"
	if [ -z "${META_REPOSECTIONS}" ] || [ "${META_REPOSECTIONS}" = "none" ]; then
		eval "META_REPOSECTIONS=\${$( echo ${META_DISTRO} | tr '[:lower:]' '[:upper:]' )_DEFAULT_REPOSECTIONS}"
		WARNINGMSG "No se han especificado las secciones para el repositorio de la Metadistribución base."
	fi
	INFOMSG "Seleccionando '%s' como secciones para el repositorio de la Metadistribución base." "${META_REPOSECTIONS}"
	DEBUGMSG "META_REPOSECTIONS"

	CONFIGMSG "Leyendo estado de la lista de paquetes de sistema" "OS_PACKAGES"
	if [ -z "${OS_PACKAGES}" ] || [ "${OS_PACKAGES}" = "none" ]; then
		OS_PACKAGES="gnome xorg"
		WARNINGMSG "No se han incluído elementos dentro de la lista de paquetes."
	fi
	INFOMSG "Seleccionando paquetes '%s' para construir el sabor."
	DEBUGMSG "OS_PACKAGES"

	CONFIGMSG "Leyendo estado de la lista de paquetes a incluir en el repositorio interno de la imagen" "OS_PACKAGES"
	if [ -z "${IMG_POOL_PACKAGES}" ] || [ "${IMG_POOL_PACKAGES}" = "none" ]; then
		IMG_POOL_PACKAGES="grub grub-pc"
		WARNINGMSG "No se han incluído elementos dentro de la lista de paquetes."
	fi
	INFOMSG "Seleccionando paquetes '%s' para incluir en el repositorio interno."
	DEBUGMSG "IMG_POOL_PACKAGES"

	CONFIGMSG "Leyendo estado de la inclusión de archivos en el sistema" "OS_INCLUDES"
	if [ -z "${OS_INCLUDES}" ] || [ "${OS_INCLUDES}" = "profile" ]; then
		OS_INCLUDES="${PROFILES}${SABOR}/OS_INCLUDES/"
		WARNINGMSG "No se han definido archivos para incluir en el sistema."
	fi
	if [ -d "${OS_INCLUDES}" ] && [ $( ls -1 "${OS_INCLUDES}" 2>/dev/null | wc -l ) >= 1 ]; then
		INFOMSG "Se incluirán en el sistema los archivos presentes en el directorio '%s'." "${OS_INCLUDES}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún archivo se incluirá en el sistema." "${OS_INCLUDES}"
		OS_INCLUDES="none"
	fi
	DEBUGMSG "OS_INCLUDES"

	CONFIGMSG "Leyendo estado de la ejecución de ganchos en el sistema" "OS_HOOKS"
	if [ -z "${OS_HOOKS}" ] || [ "${OS_HOOKS}" = "profile" ]; then
		OS_HOOKS="${PROFILES}${SABOR}/OS_HOOKS/"
		WARNINGMSG "No se han definido ganchos para ejecutar en el sistema."
	fi
	if [ -d "${OS_HOOKS}" ] && [ $( ls -1 "${OS_HOOKS}" 2>/dev/null | wc -l ) >= 1 ]; then
		INFOMSG "Se ejecutarán en el sistema los ganchos presentes en el directorio '%s'." "${OS_HOOKS}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún gancho se ejecutará en el sistema." "${OS_HOOKS}"
		OS_HOOKS="none"
	fi
	DEBUGMSG "OS_HOOKS"

	CONFIGMSG "Leyendo estado de la inclusión de archivos en la imagen" "IMG_INCLUDES"
	if [ -z "${IMG_INCLUDES}" ] || [ "${IMG_INCLUDES}" = "profile" ]; then
		IMG_INCLUDES="${PROFILES}${SABOR}/IMG_INCLUDES/"
		WARNINGMSG "No se han definido archivos para incluir en la imagen."
	fi
	if [ -d "${IMG_INCLUDES}" ] && [ $( ls -1 "${IMG_INCLUDES}" 2>/dev/null | wc -l ) >= 1 ]; then
		INFOMSG "Se incluirán en la imagen los archivos presentes en el directorio '%s'." "${IMG_INCLUDES}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún archivo se incluirá en la imagen." "${IMG_INCLUDES}"
		IMG_INCLUDES="none"
	fi
	DEBUGMSG "IMG_INCLUDES"

	CONFIGMSG "Leyendo estado de la ejecución de ganchos en la imagen" "IMG_HOOKS"
	if [ -z "${IMG_HOOKS}" ] || [ "${IMG_HOOKS}" = "profile" ]; then
		IMG_HOOKS="${PROFILES}${SABOR}/IMG_HOOKS/"
		WARNINGMSG "No se han definido ganchos para incluir en la imagen."
	fi
	if [ -d "${IMG_HOOKS}" ] && [ $( ls -1 "${IMG_HOOKS}" 2>/dev/null | wc -l ) >= 1 ]; then
		INFOMSG "Se incluirán en la imagen los ganchos presentes en el directorio '%s'." "${IMG_HOOKS}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún gancho se ejecutará en la imagen." "${IMG_HOOKS}"
		IMG_HOOKS="none"
	fi
	DEBUGMSG "IMG_HOOKS"

	CONFIGMSG "Leyendo estado de la imagen para la portada de arranque" "IMG_SYSLINUX_SPLASH"
	if [ -z "${IMG_SYSLINUX_SPLASH}" ] || [ "${IMG_SYSLINUX_SPLASH}" = "profile" ]; then
		IMG_SYSLINUX_SPLASH="${PROFILES}${SABOR}/syslinux.png"
		WARNINGMSG "No se ha definido una imagen para la portada de arranque."
	fi
	if [ -f "${IMG_SYSLINUX_SPLASH}" ]; then
		if IMG_VALIDATOR "${IMG_SYSLINUX_SPLASH}" "640" "480" "image/png"; then
			INFOMSG "Seleccionando la imagen para la portada de arranque presente en el perfil."
		else
			ERRORMSG "La imagen seleccionada para la portada de arranque es inapropiada."
			ERRORMSG "Debe utilizar una imagen PNG de dimensiones menores o iguales a 640x480px."
			exit 1
		fi
	elif [ -f "${TEMPLATES}profile/${META_DISTRO}/default/syslinux.png" ]
		IMG_SYSLINUX_SPLASH="${TEMPLATES}profile/${META_DISTRO}/default/syslinux.png"
		INFOMSG "Seleccionando la imagen predeterminada para la portada de arranque." "${IMG_SYSLINUX_SPLASH}"
	else
		ERRORMSG "Resultó imposible seleccionar una imagen para la portada de arranque."
		ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
		exit 1
	fi	
	DEBUGMSG "IMG_SYSLINUX_SPLASH"

	CONFIGMSG "Leyendo estado del instalador nativo" "IMG_DEBIAN_INSTALLER"
	if [ "${IMG_DEBIAN_INSTALLER}" = "true" ]; then
		INFOMSG "Se incluirá el instalador en la imagen."
		IMG_DEBIAN_INSTALLER="live"
		CS_BOOTAPPEND_INSTALL="locale=${OS_LOCALE}"

		CONFIGMSG "Leyendo estado de la imagen de encabezado para el instalador" "IMG_DEBIAN_INSTALLER_BANNER"
		if [ -z "${IMG_DEBIAN_INSTALLER_BANNER}" ] || [ "${IMG_DEBIAN_INSTALLER_BANNER}" = "profile" ]; then
			IMG_DEBIAN_INSTALLER_BANNER="${PROFILES}${SABOR}/DEBIAN_INSTALLER/banner.png"
			WARNINGMSG "No se ha definido una imagen de encabezado para el instalador."
		fi
		if [ -f "${IMG_DEBIAN_INSTALLER_BANNER}" ]; then
			if IMG_VALIDATOR "${IMG_DEBIAN_INSTALLER_BANNER}" "800" "75" "image/png"; then
				INFOMSG "Seleccionando la imagen de encabezado presente en el perfil."
			else
				ERRORMSG "La imagen de encabezado seleccionada es inapropiada."
				ERRORMSG "Debe utilizar una imagen PNG de dimensiones menores o iguales a 800x75px."
				exit 1
			fi
		elif [ -f "${TEMPLATES}profile/${META_DISTRO}/default/DEBIAN_INSTALLER/banner.png" ]; then
			IMG_DEBIAN_INSTALLER_BANNER="${TEMPLATES}profile/${META_DISTRO}/default/DEBIAN_INSTALLER/banner.png"
		|	INFOMSG "Seleccionando imagen de encabezado predeterminada."
		else
			ERRORMSG "Resultó imposible seleccionar una imagen de encabezado."
			ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
			exit 1
		fi
		DEBUGMSG "IMG_DEBIAN_INSTALLER_BANNER"

		CONFIGMSG "Leyendo estado de la preconfiguración para el instalador" "IMG_DEBIAN_INSTALLER_PRESEED"
		if [ -z "${IMG_DEBIAN_INSTALLER_PRESEED}" ] || [ "${IMG_DEBIAN_INSTALLER_PRESEED}" = "profile" ]; then
			IMG_DEBIAN_INSTALLER_PRESEED="${PROFILES}${SABOR}/DEBIAN_INSTALLER/preseed.cfg"
			WARNINGMSG "No se ha definido una preconfiguración para el instalador."
		fi
		if [ -f "${IMG_DEBIAN_INSTALLER_PRESEED}" ]; then
			INFOMSG "Seleccionando preconfiguración para el instalador presente en el perfil"
		elif [ -f "${TEMPLATES}profile/${META_DISTRO}/default/DEBIAN_INSTALLER/preseed.cfg" ]; then
			IMG_DEBIAN_INSTALLER_PRESEED="${TEMPLATES}profile/${META_DISTRO}/default/DEBIAN_INSTALLER/preseed.cfg"
			INFOMSG "Seleccionando los valores predeterminados de preconfiguración para el instalador."
		else
			ERRORMSG "Resultó imposible seleccionar una preconfiguración para el instalador."
			ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
			exit 1
		fi
		DEBUGMSG "IMG_DEBIAN_INSTALLER_PRESEED"

		CONFIGMSG "Leyendo estado del estilo visual para el instalador" "IMG_DEBIAN_INSTALLER_GTK"
		if [ -z "${IMG_DEBIAN_INSTALLER_GTK}" ] || [ "${IMG_DEBIAN_INSTALLER_GTK}" = "profile" ]; then
			IMG_DEBIAN_INSTALLER_GTK="${PROFILES}${SABOR}/DEBIAN_INSTALLER/gtkrc"
			WARNINGMSG "No se ha definido un estilo visual para el instalador."
		fi
		if [ -f "${IMG_DEBIAN_INSTALLER_GTK}" ]; then
			INFOMSG "Seleccionando estilo visual para el instalador presente en el perfil"
		elif [ -f "${TEMPLATES}profile/${META_DISTRO}/default/DEBIAN_INSTALLER/gtkrc" ]; then
			IMG_DEBIAN_INSTALLER_GTK="${TEMPLATES}profile/${META_DISTRO}/default/DEBIAN_INSTALLER/gtkrc"
			INFOMSG "Seleccionando estilo visual predeterminado para el instalador."
		else
			ERRORMSG "Resultó imposible seleccionar un estilo visual para el instalador."
			ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
			exit 1
		fi
		DEBUGMSG "IMG_DEBIAN_INSTALLER_GTK"
	else
		IMG_DEBIAN_INSTALLER="false"
		INFOMSG "Se incluirá el instalador en la imagen."
	fi

	OS_LANG="$( echo "${OS_LOCALE}" | sed 's/_.*//g' )"
	CS_ISO_PREPARER="${CS_ISO_PREPARER:-${CS_NAME}; http://code.google.com/p/canaima-semilla/}"
	CS_ISO_VOLUME="${CS_ISO_VOLUME:-${META_DISTRO}-${SABOR} (${DATE})}"	
	CS_ISO_PUBLISHER="${CS_ISO_PUBLISHER:-${AUTHOR_NAME}; ${AUTHOR_EMAIL}; ${AUTHOR_URL}}"	
	CS_ISO_APPLICATION="${CS_ISO_APPLICATION:-${META_DISTRO} Live}"
	CS_LIVECONFIG_VARS=""
	CS_BOOTAPPEND_LIVE="locale=${OS_LOCALE} keyb=${OS_LANG} quiet splash vga=791 live-config.user-fullname=${META_DISTRO}"
cat >  << EOF

EOF

}

CS_CONFIG_PROFILE() {

	PROFILE="${1}"
	shift || true

	if [ -z "${PROFILE}" ]; then
		ERRORMSG "La función '%s' necesita un nombre de perfil válido como argumento." "${FUNCNAME}"
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

