#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/save.sh
# DESCRIPCIÓN: Módulo para grabar imágenes en médios de almacenamiento digitales
#	      u ópticos.
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

ACTION="${1}"
[ -n "${ACTION}" ] && shift 1 || true
BINDIR="${1}"
[ -n "${BINDIR}" ] && shift 1 || true

# Asignando directorios de trabajo
if [ "${BINDIR}" = "/usr/bin" ]; then
	BASEDIR="/usr/share/canaima-semilla"
	CONFDIR="/etc/canaima-semilla"
else
	BASEDIR="${BINDIR}"
	CONFDIR="${BASEDIR}"
fi

# Cargando valores predeterminados
. "${BASEDIR}/scripts/functions/defaults.sh"

# Corriendo rutinas de inicio
. "${BASEDIR}/scripts/init.sh"

if [ "${ACTION}" = "grabar" ]; then
	LONGOPTS="imagen:,dispositivo:"
	COMMAND="probar"
	PARAMETERS="[-i|--imagen ARCHIVO]\n\
\t[-m|--memoria 256|512|...]\n\
\t[-p|--procesadores 1|2|4|...]\n\
\t[-c|--iniciar-cd]\n\
\t[-d|--iniciar-dd]\n\
\t[-n|--nuevo-disco]\n\
\t[-s|--dimensiones-disco 10|50|...]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

elif [ "${ACTION}" = "save" ]; then
	LONGOPTS="image:,device:"
	COMMAND="probar"
	PARAMETERS="[-i|--imagen ARCHIVO]\n\
\t[-m|--memoria 256|512|...]\n\
\t[-p|--procesadores 1|2|4|...]\n\
\t[-c|--iniciar-cd]\n\
\t[-d|--iniciar-dd]\n\
\t[-n|--nuevo-disco]\n\
\t[-s|--dimensiones-disco 10|50|...]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

else
	ERRORMSG "Error interno"
	exit 1
fi

SHORTOPTS="i:d:"
DESCRIPTION="$( NORMALMSG "Comando para simulación de imágenes instalables." )"

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

		-v|--expresivo|--verbose)
			SAVE_PRINT_MODE="verbose"
			shift 1 || true
		;;

		-q|--silencioso|--quiet)
			SAVE_PRINT_MODE="quiet"
			shift 1 || true
		;;

		-l|--listar-opticos|--list-optical)
			SAVE_OP_MODE="list-optical"
			shift 1 || true
		;;

		-L|--listar-usb|--list-usb)
			SAVE_OP_MODE="list-usb"
			shift 1 || true
		;;

		-h|--ayuda|--help)
			if ${MAN} -w "${CS_CMD}_${COMMAND}" 1>/dev/null 2>&1; then
				${MAN} "${CS_CMD}_${COMMAND}"
				exit 0
			else
				USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
			fi
		;;

		-u|--uso|--usage)
			USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
		;;

		-A|--acerca|--about)
			ABOUT
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


case ${SAVE_OP_MODE} in
	list-usb)

	;;

	list-usb)

	;;

	normal)

	;;
esac
	/dev/cdrom|/dev/cdrw|/dev/dvd|/dev/dvdrw|/dev/scd0|/dev/sr0|cd|dvd)
		BURNDEVICE="$( wodim -devices | grep '/dev/' | awk '{print $2}' )"
		if wodim ${BURNDEVICE} -data ${IMAGE}; then
			SUCCESSMSG ""
			exit 0
		else
			ERRORMSG ""
			exit 1
		fi
	;;
	*)
		if dd if="${IMAGE}" of="${DEVICE}"; then
			SUCCESSMSG ""
			exit 0
		else
			ERRORMSG ""
			exit 1
		fi
	;;
esac
