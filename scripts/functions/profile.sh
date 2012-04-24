#!/bin/sh -e

CS_LOAD_PROFILE() {

	ISOS="${1}"
	shift || true
	PROFILES="${1}"
	shift || true
	SABOR="${1}"
	shift || true
	ARCH="${1}"
	shift || true
	MEDIO="${1}"
	shift || true
	CS_OP_MODE="${1}"
	shift || true
	CS_PRINT_MODE="${1}"
	shift || true
	EXTRACONF="${1}"
	shift || true

	PCONFDIR="${PROFILES}/${SABOR}"
	PCONFFILE="${PCONFDIR}/profile.conf"
	TCSCONFDIR="${ISOS}/config/c-s"
	TCSCONFFILE="${TCSCONFDIR}/tree.conf"

	if [ -f "${PCONFFILE}" ]; then
		. "${PCONFFILE}"	
	else
		ERRORMSG "El archivo de configuraciones '%s' no existe o no es un archivo válido." "${PCONFFILE}"
		exit 1
	fi

	if [ -n "${EXTRACONF}" ] && [ -f "${EXTRACONF}" ]; then
		. "${EXTRACONF}"
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

	CONFIGMSG "Leyendo estado de la arquitectura de construcción" "ARCH"
	case ${ARCH} in
		amd64)
			ARCH="amd64"
			KERNEL_ARCH="amd64"
		;;

		i386)
			ARCH="i386"
			KERNEL_ARCH="686"
		;;

		*)
			ERRORMSG "Arquitectura '%s' no soportada por %s. Abortando." "${ARCH}" "${CS_NAME}"
			exit 1
		;;
	esac
	INFOMSG "Seleccionando '%s' como arquitectura de construcción para la imagen" "${ARCH}"
	DEBUGMSG "ARCH"

	CONFIGMSG "Leyendo estado del formato de imagen a utilizar" "MEDIO"
	case ${MEDIO} in
		img)
			if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
				MEDIO="hdd"
			else
				MEDIO="usb-hdd"
			fi
			MEDIO_LBNAME="binary.img"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}~${DATE}_${ARCH}.img"
			LB_BOOTLOADER="syslinux"
		;;

		iso)
			MEDIO="iso"
			MEDIO_LBNAME="binary.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}~${DATE}_${ARCH}.iso"
			LB_BOOTLOADER="isolinux"
		;;

		mixto|hybrid)
			MEDIO="iso-hybrid"
			MEDIO_LBNAME="binary-hybrid.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}~${DATE}_${ARCH}.iso"
			LB_BOOTLOADER="isolinux"
		;;

		*)
			ERRORMSG "Tipo de formato '%s' no reconocido por %s. Abortando." "${MEDIO}" "${CS_NAME}"
			exit 1
		;;
	esac
	INFOMSG "Seleccionando '%s' como formato de construcción para la imagen" "${MEDIO}"
	DEBUGMSG "MEDIO"

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
		WARNINGMSG "No se han incluído elementos dentro de la lista de paquetes para el sistema operativo."
	fi
	INFOMSG "Seleccionando paquetes '%s' para construir el sabor." "${OS_PACKAGES}"
	DEBUGMSG "OS_PACKAGES"

	CONFIGMSG "Leyendo estado de la lista de paquetes a incluir en el repositorio interno de la imagen" "OS_PACKAGES"
	if [ -z "${IMG_POOL_PACKAGES}" ] || [ "${IMG_POOL_PACKAGES}" = "none" ]; then
		IMG_POOL_PACKAGES="grub grub-pc"
		WARNINGMSG "No se han incluído elementos dentro de la lista de paquetes para el repositorio interno."
	fi
	INFOMSG "Seleccionando paquetes '%s' para incluir en el repositorio interno." "${IMG_POOL_PACKAGES}"
	DEBUGMSG "IMG_POOL_PACKAGES"

	CONFIGMSG "Leyendo estado de la inclusión de repositorios adicionales en el sistema" "OS_EXTRAREPOS"
	if [ -z "${OS_EXTRAREPOS}" ] || [ "${OS_EXTRAREPOS}" = "profile" ]; then
		OS_EXTRAREPOS="${PROFILES}/${SABOR}/extra-repos.list"
		WARNINGMSG "No se han definido repositorios adicionales para incluir en el sistema."
	fi
	if [ -f "${OS_EXTRAREPOS}" ] && [ $( cat "${OS_EXTRAREPOS}" | wc -l ) -ge 1 ]; then
		INFOMSG "Se incluirán en el sistema los repositorios adicionales presentes en el archivo '%s'." "${OS_EXTRAREPOS}"
	else
		INFOMSG "'%s' está vacío o no es un archivo válido. Ningún repositorio adicional se incluirá en el sistema." "${OS_EXTRAREPOS}"
		OS_EXTRAREPOS="none"
	fi
	DEBUGMSG "OS_EXTRAREPOS"

	CONFIGMSG "Leyendo estado de la inclusión de archivos en el sistema" "OS_INCLUDES"
	if [ -z "${OS_INCLUDES}" ] || [ "${OS_INCLUDES}" = "profile" ]; then
		OS_INCLUDES="${PROFILES}/${SABOR}/OS_INCLUDES/"
		WARNINGMSG "No se han definido archivos para incluir en el sistema."
	fi
	if [ -d "${OS_INCLUDES}" ] && [ $( ls -1 "${OS_INCLUDES}" 2>/dev/null | wc -l ) -ge 1 ]; then
		INFOMSG "Se incluirán en el sistema los archivos presentes en el directorio '%s'." "${OS_INCLUDES}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún archivo se incluirá en el sistema." "${OS_INCLUDES}"
		OS_INCLUDES="none"
	fi
	DEBUGMSG "OS_INCLUDES"

	CONFIGMSG "Leyendo estado de la ejecución de ganchos en el sistema" "OS_HOOKS"
	if [ -z "${OS_HOOKS}" ] || [ "${OS_HOOKS}" = "profile" ]; then
		OS_HOOKS="${PROFILES}/${SABOR}/OS_HOOKS/"
		WARNINGMSG "No se han definido ganchos para ejecutar en el sistema."
	fi
	if [ -d "${OS_HOOKS}" ] && [ $( ls -1 "${OS_HOOKS}" 2>/dev/null | wc -l ) -ge 1 ]; then
		INFOMSG "Se ejecutarán en el sistema los ganchos presentes en el directorio '%s'." "${OS_HOOKS}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún gancho se ejecutará en el sistema." "${OS_HOOKS}"
		OS_HOOKS="none"
	fi
	DEBUGMSG "OS_HOOKS"

	CONFIGMSG "Leyendo estado de la inclusión de archivos en la imagen" "IMG_INCLUDES"
	if [ -z "${IMG_INCLUDES}" ] || [ "${IMG_INCLUDES}" = "profile" ]; then
		IMG_INCLUDES="${PROFILES}/${SABOR}/IMG_INCLUDES/"
		WARNINGMSG "No se han definido archivos para incluir en la imagen."
	fi
	if [ -d "${IMG_INCLUDES}" ] && [ $( ls -1 "${IMG_INCLUDES}" 2>/dev/null | wc -l ) -ge 1 ]; then
		INFOMSG "Se incluirán en la imagen los archivos presentes en el directorio '%s'." "${IMG_INCLUDES}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún archivo se incluirá en la imagen." "${IMG_INCLUDES}"
		IMG_INCLUDES="none"
	fi
	DEBUGMSG "IMG_INCLUDES"

	CONFIGMSG "Leyendo estado de la ejecución de ganchos en la imagen" "IMG_HOOKS"
	if [ -z "${IMG_HOOKS}" ] || [ "${IMG_HOOKS}" = "profile" ]; then
		IMG_HOOKS="${PROFILES}/${SABOR}/IMG_HOOKS/"
		WARNINGMSG "No se han definido ganchos para incluir en la imagen."
	fi
	if [ -d "${IMG_HOOKS}" ] && [ $( ls -1 "${IMG_HOOKS}" 2>/dev/null | wc -l ) -ge 1 ]; then
		INFOMSG "Se incluirán en la imagen los ganchos presentes en el directorio '%s'." "${IMG_HOOKS}"
	else
		INFOMSG "'%s' está vacío o no es un directorio. Ningún gancho se ejecutará en la imagen." "${IMG_HOOKS}"
		IMG_HOOKS="none"
	fi
	DEBUGMSG "IMG_HOOKS"

	if dpkg --compare-versions "${LB_VERSION}" ge 3.0; then
		IMG_SYSLINUX_TEMPLATE="${TEMPLATES}/${LB_BOOTLOADER}/3.0/${META_DISTRO}"
	else
		IMG_SYSLINUX_TEMPLATE="${TEMPLATES}/${LB_BOOTLOADER}/2.0/${META_DISTRO}"
	fi

	CONFIGMSG "Leyendo estado de la imagen para la portada de arranque" "IMG_SYSLINUX_SPLASH"
	if [ -z "${IMG_SYSLINUX_SPLASH}" ] || [ "${IMG_SYSLINUX_SPLASH}" = "profile" ]; then
		IMG_SYSLINUX_SPLASH="${PROFILES}/${SABOR}/syslinux.png"
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
	elif [ -f "${TEMPLATES}profile/${META_DISTRO}/default/syslinux.png" ]; then
		IMG_SYSLINUX_SPLASH="${TEMPLATES}/profile/${META_DISTRO}/default/syslinux.png"
		INFOMSG "Seleccionando la imagen predeterminada para la portada de arranque." "${IMG_SYSLINUX_SPLASH}"
	else
		ERRORMSG "Resultó imposible seleccionar una imagen para la portada de arranque."
		ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
		exit 1
	fi	
	DEBUGMSG "IMG_SYSLINUX_SPLASH"


	CONFIGMSG "Leyendo estado del instalador nativo" "IMG_DEBIAN_INSTALLER"
	case ${IMG_DEBIAN_INSTALLER} in
		true)
			INFOMSG "Se incluirá el instalador en la imagen."
			IMG_DEBIAN_INSTALLER="live"
			CS_BOOTAPPEND_INSTALL="locale=${OS_LOCALE}"
		;;

		*)
			INFOMSG "No se incluirá el instalador en la imagen."
			IMG_DEBIAN_INSTALLER="false"
			CS_BOOTAPPEND_INSTALL=""
		;;
	esac
	DEBUGMSG "IMG_DEBIAN_INSTALLER"

	CONFIGMSG "Leyendo estado de la imagen de encabezado para el instalador" "IMG_DEBIAN_INSTALLER_BANNER"
	if [ -z "${IMG_DEBIAN_INSTALLER_BANNER}" ] || [ "${IMG_DEBIAN_INSTALLER_BANNER}" = "profile" ]; then
		IMG_DEBIAN_INSTALLER_BANNER="${PROFILES}/${SABOR}/DEBIAN_INSTALLER/banner.png"
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
	elif [ -f "${TEMPLATES}/profile/${META_DISTRO}/default/DEBIAN_INSTALLER/banner.png" ]; then
		IMG_DEBIAN_INSTALLER_BANNER="${TEMPLATES}/profile/${META_DISTRO}/default/DEBIAN_INSTALLER/banner.png"
		INFOMSG "Seleccionando imagen de encabezado predeterminada."
	else
		ERRORMSG "Resultó imposible seleccionar una imagen de encabezado."
		ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
		exit 1
	fi
	DEBUGMSG "IMG_DEBIAN_INSTALLER_BANNER"

	CONFIGMSG "Leyendo estado de la preconfiguración para el instalador" "IMG_DEBIAN_INSTALLER_PRESEED"
	if [ -z "${IMG_DEBIAN_INSTALLER_PRESEED}" ] || [ "${IMG_DEBIAN_INSTALLER_PRESEED}" = "profile" ]; then
		IMG_DEBIAN_INSTALLER_PRESEED="${PROFILES}/${SABOR}/DEBIAN_INSTALLER/preseed.cfg"
		WARNINGMSG "No se ha definido una preconfiguración para el instalador."
	fi
	if [ -f "${IMG_DEBIAN_INSTALLER_PRESEED}" ]; then
		INFOMSG "Seleccionando preconfiguración para el instalador presente en el perfil"
	elif [ -f "${TEMPLATES}/profile/${META_DISTRO}/default/DEBIAN_INSTALLER/preseed.cfg" ]; then
		IMG_DEBIAN_INSTALLER_PRESEED="${TEMPLATES}/profile/${META_DISTRO}/default/DEBIAN_INSTALLER/preseed.cfg"
		INFOMSG "Seleccionando los valores predeterminados de preconfiguración para el instalador."
	else
		ERRORMSG "Resultó imposible seleccionar una preconfiguración para el instalador."
		ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
		exit 1
	fi
	DEBUGMSG "IMG_DEBIAN_INSTALLER_PRESEED"

	CONFIGMSG "Leyendo estado del estilo visual para el instalador" "IMG_DEBIAN_INSTALLER_GTK"
	if [ -z "${IMG_DEBIAN_INSTALLER_GTK}" ] || [ "${IMG_DEBIAN_INSTALLER_GTK}" = "profile" ]; then
		IMG_DEBIAN_INSTALLER_GTK="${PROFILES}/${SABOR}/DEBIAN_INSTALLER/gtkrc"
		WARNINGMSG "No se ha definido un estilo visual para el instalador."
	fi
	if [ -f "${IMG_DEBIAN_INSTALLER_GTK}" ]; then
		INFOMSG "Seleccionando estilo visual para el instalador presente en el perfil"
	elif [ -f "${TEMPLATES}/profile/${META_DISTRO}/default/DEBIAN_INSTALLER/gtkrc" ]; then
		IMG_DEBIAN_INSTALLER_GTK="${TEMPLATES}/profile/${META_DISTRO}/default/DEBIAN_INSTALLER/gtkrc"
		INFOMSG "Seleccionando estilo visual predeterminado para el instalador."
	else
		ERRORMSG "Resultó imposible seleccionar un estilo visual para el instalador."
		ERRORMSG "La instalación de %s puede estar corrupta, por favor reinstala." "${CS_NAME}"
		exit 1
	fi
	DEBUGMSG "IMG_DEBIAN_INSTALLER_GTK"

        case ${CS_PRINT_MODE} in
                normal)
                        LB_QUIET=""
                        LB_VERBOSE=""
                ;;

                quiet)
                        LB_QUIET="--quiet"
                        LB_VERBOSE=""
                ;;

                verbose)
                        LB_QUIET=""
                        LB_VERBOSE="--verbose"
                ;;
        esac

	OS_INCLUDES="${OS_INCLUDES%/}"
	OS_HOOKS="${OS_HOOKS%/}"
	IMG_INCLUDES="${IMG_INCLUDES%/}"
	IMG_HOOKS="${IMG_HOOKS%/}"
	IMG_SYSLINUX_TEMPLATE="${IMG_SYSLINUX_TEMPLATE%/}"
        OS_LANG="$( echo "${OS_LOCALE}" | sed 's/_.*//g' )"
        CS_ISO_PREPARER="${CS_ISO_PREPARER:-${CS_NAME}; http://code.google.com/p/canaima-semilla/}"
        CS_ISO_VOLUME="${CS_ISO_VOLUME:-${META_DISTRO}-${SABOR}}"
        CS_ISO_VOLUME="$( echo "${CS_ISO_VOLUME}" | cut -c1-32 )"
        CS_ISO_PUBLISHER="${CS_ISO_PUBLISHER:-${AUTHOR_NAME}; ${AUTHOR_EMAIL}; ${AUTHOR_URL}}"
        CS_ISO_APPLICATION="${CS_ISO_APPLICATION:-${META_DISTRO} Live}"
        CS_BOOTAPPEND_LIVE="live-config.locales=${OS_LOCALE} \
live-config.hostname=${META_DISTRO} \
live-config.username=${META_DISTRO}-${SABOR} \
live-config.user-fullname=${META_DISTRO} \
keyb=${OS_LANG} quiet splash vga=791"

	PVARIABLES="SABOR=\"${SABOR}\"\nARCH=\"${ARCH}\"\nKERNEL_ARCH=\"${KERNEL_ARCH}\"\nMEDIO=\"${MEDIO}\"\nMEDIO_LBNAME=\"${MEDIO_LBNAME}\"\nMEDIO_CS_NAME=\"${MEDIO_CSNAME}\"\n\nAUTHOR_NAME=\"${AUTHOR_NAME}\"\nAUTHOR_EMAIL=\"${AUTHOR_EMAIL}\"\nAUTHOR_URL=\"${AUTHOR_URL}\"\n\nOS_LOCALE=\"${OS_LOCALE}\"\nOS_LANG=\"${OS_LANG}\"\n\nMETA_MODE=\"${META_MODE}\"\nMETA_CODENAME=\"${META_CODENAME}\"\nMETA_DISTRO=\"${META_DISTRO}\"\nMETA_REPO=\"${META_REPO}\"\nMETA_REPOSECTIONS=\"${META_REPOSECTIONS}\"\n\nOS_PACKAGES=\"${OS_PACKAGES}\"\nOS_EXTRAREPOS=\"${OS_EXTRAREPOS}\"\nOS_INCLUDES=\"${OS_INCLUDES}\"\nOS_HOOKS=\"${OS_HOOKS}\"\nIMG_POOL_PACKAGES=\"${IMG_POOL_PACKAGES}\"\nIMG_INCLUDES=\"${IMG_INCLUDES}\"\nIMG_HOOKS=\"${IMG_HOOKS}\"\n\nLB_BOOTLOADER=\"${LB_BOOTLOADER}\"\nIMG_SYSLINUX_SPLASH=\"${IMG_SYSLINUX_SPLASH}\"\nIMG_SYSLINUX_TEMPLATE=\"${IMG_SYSLINUX_TEMPLATE}\"\nIMG_DEBIAN_INSTALLER=\"${IMG_DEBIAN_INSTALLER}\"\nIMG_DEBIAN_INSTALLER_BANNER=\"${IMG_DEBIAN_INSTALLER_BANNER}\"\nIMG_DEBIAN_INSTALLER_PRESEED=\"${IMG_DEBIAN_INSTALLER_PRESEED}\"\nIMG_DEBIAN_INSTALLER_GTK=\"${IMG_DEBIAN_INSTALLER_GTK}\"\n\nCS_ISO_PREPARER=\"${CS_ISO_PREPARER}\"\nCS_ISO_VOLUME=\"${CS_ISO_VOLUME}\"\nCS_ISO_PUBLISHER=\"${CS_ISO_PUBLISHER}\"\nCS_ISO_APPLICATION=\"${CS_ISO_APPLICATION}\"\nCS_BOOTAPPEND_LIVE=\"${CS_BOOTAPPEND_LIVE}\"\nCS_BOOTAPPEND_INSTALL=\"${CS_BOOTAPPEND_INSTALL}\"\n\nLB_QUIET=\"${LB_QUIET}\"\nLB_VERBOSE=\"${LB_VERBOSE}\""

	case ${CS_OP_MODE} in
		configonly|normal)
			if [ ! -d "${TCSCONFDIR}" ]; then
				mkdir -p "${TCSCONFDIR}"
			fi
			echo "${PVARIABLES}" > "${TCSCONFFILE}"
		;;

		vardump)
			echo "${PVARIABLES}"
		;;
	esac
}
