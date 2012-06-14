#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/save.sh
# DESCRIPCIÓN: Módulo para grabar imágenes en médios de almacenamiento digitales
#              u ópticos.
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

		-v|--expresivo|--verbose)
			SAVE_PRINT_MODE="verbose"
			shift 2 || true
		;;

		-q|--silencioso|--quiet)
			SAVE_PRINT_MODE="quiet"
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
