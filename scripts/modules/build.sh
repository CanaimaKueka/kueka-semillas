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
	SHORTOPTS="f:a:m:s:inbcd"
	LONGOPTS="archivo-config:,arquitectura:,medio:,sabor:,instalador,sin-instalador,solo-construir,solo-configurar,debug"
elif [ "${ACTION}" == "build" ]; then
	SHORTOPTS="f:a:m:s:inbcd"
	LONGOPTS="config-file:,architecture:,image:,profile:,installer,no-installer,build-only,config-only,debug"
else
	ERRORMSG "Error interno"
	exit 1
fi

OPTIONS="$( getopt --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ $? != 0 ]; then
	ERRORMSG "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

CONFIGONLY="${CONFIGONLY:-true}"
BUILDONLY="${BUILDONLY:-true}"
INSTALADOR="${INSTALADOR:-true}"

while true; do
	case "${1}" in
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

		-f|--archivo-config|--config-file)
			EXTRACONF="${2}"
			shift 2 || true
		;;

		-d|--dir-construir|--build-dir)
			BUILDDIR="${2}"
			shift 2 || true
		;;

		-b|--solo-construir|--build-only)
			BUILDONLY="true"
			CONFIGONLY="false"
			shift 1 || true
		;;

		-c|--solo-configurar|--config-only)
			CONFIGONLY="true"
			BUILDONLY="false"
			shift 1 || true
		;;

		-p|--var-dump|--mostrar-variables)
			CS_VARDUMP="true"
			shift 1 || true
		;;

		-v|--verbose|--expresivo)
			CS_VERBOSE="true"
			shift 1 || true
		;;


		-q|--quiet|--silencioso)
			CS_QUIET="true"
			shift 1 || true
		;;

                --)
			shift
			break
		;;

                *)
			ERRORMSG "Ocurrió un problema interpretando los parámetros."
			exit 1
		;;
	esac
done

if [ -n "${BUILDDIR}" ] && [ -e "${BUILDDIR}" ]; then
	ISOS="${BUILDDIR}"
	INFOMSG "Utilizando %s para construir la imagen." "${BUILDDIR}"
else
	ERRORMSG "El directorio '%s' establecido a través de la opción --dir-construir no existe." "${BUILDDIR}"
	exit 1
fi

if ${CONFIGONLY} || ${VARDUMP}; then

	cd "${ISOS}"

	if [ -z "${SABOR}" ]; then
		SABOR="popular"
		INFOMSG "No especificaste un sabor, utilizando sabor '%s' por defecto." "${SABOR}"
	fi

	if [ -z "${ARCH}" ]; then
		ARCH="$( dpkg --print-architecture )"
		INFOMSG "No especificaste una arquitectura, utilizando '%s' presente en el sistema." "${ARCH}"
	fi

	if [ -z "${MEDIO}" ]; then
		MEDIO="iso-hybrid"
		INFOMSG "No especificaste un tipo de formato para la imagen, utilizando medio '%s' por defecto." "${MEDIO}"
	fi

	PCONF="${PCONF:-${ISOS}config}"
	PHISTORY="${PHISTORY:-${ISOS}history}"
	PCONFBKP="${PCONFBKP:-${ISOS}history/config.${DATE}.backup}"
	PCONFFILE="${PCONFFILE:-${PROFILES}${SABOR}/profile.conf}"
	PCONFIGURED="${PCONFIGURED:-${ISOS}config/c-s/build-data.conf}"

	if [ -d "${PROFILES}${SABOR}" ]; then
		if [ -f "${PCONFFILE}" ]; then
			CS_LOAD_PROFILE "${SABOR}" "${PCONFFILE}"
		else
			ERRORMSG "El perfil '%s' no posee configuración en '%s'" "${SABOR}" "${PCONFFILE}"
			exit 1
		fi
	else
		ERRORMSG "El perfil '%s' no existe dentro de la carpeta de perfiles '%s'." "${SABOR}" "${PROFILES}"
		exit 1
	fi

	# ARQUITECTURA
	case ${ARCH} in
		amd64)
			ARCH="amd64"
			KERNEL_ARCH="amd64"
			SUCCESSMSG "Arquitectura: amd64"
		;;

		i386)
			ARCH="i386"
			KERNEL_ARCH="686"
			SUCCESSMSG "Arquitectura: i386"
		;;

		*)
			ERRORMSG "Arquitectura '%s' no soportada por %s. Abortando." "${ARCH}" "${CS_NAME}"
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
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}~${DATE}_${ARCH}.img"
			SUCCESSMSG "Medio: Imagen para dispositivos de almacenamiento extraíble (USB)."
		;;

		iso|ISO|CD|DVD)
			MEDIO="iso"
			MEDIO_LBNAME="binary.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}~${DATE}_${ARCH}.iso"
			SUCCESSMSG "Medio: Imagen para dispositivos ópticos de almacenamiento (CD/DVD)."
		;;

		iso-hybrid|hibrido|mixto|hybrid)
			MEDIO="iso-hybrid"
			MEDIO_LBNAME="binary-hybrid.iso"
			MEDIO_CSNAME="${META_DISTRO}-${SABOR}~${DATE}_${ARCH}.iso"
			SUCCESSMSG "Medio: Imagen mixta para dispositivos de almacenamiento (CD/DVD/USB)."
		;;

		*)
			ERRORMSG "Tipo de formato '%s' no reconocido por %s. Abortando." "${MEDIO}" "${CS_NAME}"
			exit 1
		;;
	esac

	if [ -d "${PROFILES}${SABOR}" ]; then
		if [ -f "${PCONFFILE}" ]; then
			CS_CONFIG_LB "${SABOR}" "${PCONFIG}"
		else
			ERRORMSG "El perfil '%s' no posee configuración en '%s'" "${SABOR}" "${PCONFFILE}"
			exit 1
		fi
	else
		ERRORMSG "El perfil '%s' no existe dentro de la carpeta de perfiles '%s'." "${SABOR}" "${PCONFFILE}"
		exit 1
	fi

	if [ -f "${PCONFIGURED}" ]; then
		SUCCESSMSG "Sabor: %s" "${SABOR}"
	else
		ERRORMSG "El perfil '%s' no logró configurarse correctamente. Abortando." "${SABOR}"
		exit 1
	fi
fi

if ${BUILDONLY}; then

	if [ -f "${ISOS}config/c-s/build-data.conf" ]; then
		. "${ISOS}config/c-s/build-data.conf"
	else
		WARNINGMSG "El contenedor de construcción parece haber sido configurado manualmente."
		WARNINGMSG "Puede que algunas características de %s no estén disponibles." "${CS_NAME}"
		
		if 	[ -f "${ISOS}config/common" ] && \
			[ -f "${ISOS}config/binary" ] && \
			[ -f "${ISOS}config/chroot" ] && \
			[ -f "${ISOS}config/bootstrap" ]; then

			. "${ISOS}config/bootstrap"
			. "${ISOS}config/chroot"
			. "${ISOS}config/binary"
			. "${ISOS}config/common"

			ARCH="${LB_ARCHITECTURES}"
			MEDIO="${LB_BINARY_IMAGES}"
			META_DISTRO="${LB_MODE}"

			case ${MEDIO} in
				usb-hdd|hdd)
					MEDIO_LBNAME="binary.img"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.img"
				;;

				iso)
					MEDIO_LBNAME="binary.iso"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.iso"
				;;

				iso-hybrid)
					MEDIO_LBNAME="binary-hybrid.iso"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.iso"
				;;
			esac
		else
			ERRORMSG "%s no pudo encontrar una configuración apropiada en %s." "${CS_NAME}" "${ISOS}config"
			exit 1
		fi
	fi

	cd "${ISOS}"
	echo ""
	WARNINGMSG "[--- INICIANDO CONSTRUCCIÓN ---]"
	echo ""
	lb build 2>&1 | tee "${ISOS}${LOGFILE}"

	if [ -e "${ISOS}${MEDIO_LBNAME}" ] && [ -n "${MEDIO_CSNAME}" ] && [ -n "${MEDIO_LBNAME}" ]; then

		PESO="$( echo "scale=2;$( stat --format=%s "${ISOS}${MEDIO_LBNAME}" )/1048576" | bc )MB"
		mv "${ISOS}${MEDIO_LBNAME}" "${ISOS}${MEDIO_CSNAME}"

		SUCCESSMSG "Se ha creado una imagen %s con un peso de %s." "${MEDIO}" "${PESO}"
		SUCCESSMSG "Puedes encontrar la imagen '%s' en el directorio %s" "${MEDIO_CSNAME}" "${ISOS}"
		exit 0
	else
		ERRORMSG "Ocurrió un error durante la generación de la imagen."
		ERRORMSG "Si deseas asistencia, puedes enviar un correo a %s con el contenido del archivo '%s'" "${CS_LOG_MAIL}" "${ISOS}${LOGFILE}"
		exit 1
	fi
fi
