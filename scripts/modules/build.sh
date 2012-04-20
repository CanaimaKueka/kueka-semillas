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
			CS_OP_MODE="buildonly"
			shift 1 || true
		;;

		-c|--solo-configurar|--config-only)
			CS_OP_MODE="configonly"
			shift 1 || true
		;;

		-p|--var-dump|--mostrar-variables)
			CS_OP_MODE="vardump"
			shift 1 || true
		;;

		-v|--verbose|--expresivo)
			CS_PRINT_MODE="verbose"
			shift 1 || true
		;;


		-q|--quiet|--silencioso)
			CS_PRINT_MODE="quiet"
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

if [ -n "${BUILDDIR}" ] && [ -d "${BUILDDIR}" ]; then
	ISOS="${BUILDDIR}"
	INFOMSG "Utilizando %s para construir la imagen." "${BUILDDIR}"
else
	ERRORMSG "El directorio '%s' establecido a través de la opción --dir-construir no existe." "${BUILDDIR}"
	exit 1
fi

case ${CS_OP_MODE} in
	configonly|vardump|normal)

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

	        if [ ! -d "${ISOS}" ]; then
	                ERRORMSG "El directorio de construcción de imágenes '%s' no existe." "${ISOS}"
			exit 1
        	fi

		if [ ! -d "${PROFILES}" ]; then
			ERRORMSG "La carpeta de perfiles '%s' no existe o no es un directorio válido." "${PROFILES}"
			exit 1
		fi

		if [ ! -d "${PROFILES}/${SABOR}" ]; then
			ERRORMSG "El perfil '%s' no existe dentro de la carpeta de perfiles '%s'." "${SABOR}" "${PROFILES}"
			exit 1
		fi

		CS_LOAD_PROFILE "${ISOS}" "${PROFILES}" "${SABOR}" "${ARCH}" "${MEDIO}" "${CS_OP_MODE}" "${CS_PRINT_MODE}" "${EXTRACONF}"
       	        CS_CLEAN_TREE "${ISOS}" "${CS_OP_MODE}" "${CS_PRINT_MODE}"
		CS_CREATE_TREE "${ISOS}" "${CS_OP_MODE}" "${CS_PRINT_MODE}"
	;;
esac

case ${CS_OP_MODE} in
	buildonly|normal)

	        if [ ! -d "${ISOS}" ]; then
	                ERRORMSG "El directorio de construcción de imágenes '%s' no existe." "${ISOS}"
			exit 1
        	fi

		CS_BUILD_IMAGE "${ISOS}" "${CS_OP_MODE}" "${CS_PRINT_MODE}"
	;;
esac
