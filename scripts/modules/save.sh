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

if [ "${ACTION}" = "grabar" ]; then
	SHORTOPTS="i:d:"
	LONGOPTS="imagen:,dispositivo:"
elif [ "${ACTION}" = "save" ]; then
	SHORTOPTS="i:d:"
	LONGOPTS="image:,device:"
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
		-i|--imagen|--image)
			IMAGE="${2}"
			shift 2 || true
		;;

		-d|--dispositivo|--device)
			DEVICE="${2}"
			shift 2 || true
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

case ${DEVICE} in
	/dev/cdrom|/dev/cdrw|/dev/dvd|/dev/dvdrw|/dev/scd0|/dev/sr0)
		BURNDEVICE="$( wodim -devices | grep '/dev/' | awk '{print $2}' )"
		wodim ${BURNDEVICE} -data ''
	;;
	*)
		dd if="${IMAGE}" of="${DEVICE}"
	;;
esac
