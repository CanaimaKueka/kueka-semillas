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
if [ "${BINDIR}" = "/usr/bin" ]; then
        BASEDIR="/usr/share/canaima-semilla"
        CONFDIR="/etc/canaima-semilla"
else
        BASEDIR="$( dirname "${BINDIR}" )"
        CONFDIR="${BASEDIR}"
fi

# Cargando valores predeterminados
. "${BASEDIR}/scripts/functions/defaults.sh"

# Corriendo rutinas de inicio
. "${BASEDIR}/scripts/init.sh"

if [ "${ACTION}" = "construir" ]; then
	SHORTOPTS="a:m:s:f:d:bcpvq"
	LONGOPTS="arquitectura:,medio:,sabor:,archivo-config:,dir-construir:,solo-construir,solo-configurar,mostrar-variables,expresivo,silencioso"
elif [ "${ACTION}" = "build" ]; then
	SHORTOPTS="a:m:s:f:d:bcpvq"
	LONGOPTS="architecture:,image:,profile:,config-file:,build-dir:,build-only,config-only,var-dump,verbose,quiet"
else
	ERRORMSG "Error interno"
	exit 1
fi

OPTIONS="$( ${BIN_GETOPT} --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

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

		-p|--mostrar-variables|--var-dump)
			CS_OP_MODE="vardump"
			shift 1 || true
		;;

		-v|--expresivo|--verbose)
			CS_PRINT_MODE="verbose"
			shift 1 || true
		;;

		-q|--silencioso|--quiet)
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

SWITCHLOG="on"

if [ -n "${BUILDDIR}" ]; then
	if [ -d "${BUILDDIR}" ]; then
		ISOS="${BUILDDIR}"
		INFOMSG "Utilizando %s para construir la imagen." "${BUILDDIR}"
	else
		ERRORMSG "El directorio '%s' establecido a través de la opción --dir-construir no existe." "${BUILDDIR}"
		exit 1
	fi
fi

case ${CS_OP_MODE} in
	configonly|vardump|normal)

		if [ -z "${SABOR}" ]; then
			SABOR="popular"
			INFOMSG "No especificaste un sabor, utilizando sabor '%s' por defecto." "${SABOR}"
		fi

		if [ -z "${ARCH}" ]; then
			ARCH="$( ${BIN_DPKG} --print-architecture )"
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

       	        CS_CLEAN_TREE "${ISOS}" "${CS_OP_MODE}" "${CS_PRINT_MODE}"
		CS_LOAD_PROFILE "${ISOS}" "${PROFILES}" "${SABOR}" "${ARCH}" "${MEDIO}" "${CS_OP_MODE}" "${CS_PRINT_MODE}" "${EXTRACONF}"
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
