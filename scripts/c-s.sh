#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: c-s.sh
# DESCRIPCIÓN: script principal de shell para la aplicación Canaima Semilla
# USO: 
# COPYRIGHT:
#  (C) 2010 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#  (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL3
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

# Determinando directorio de ejecución
BINDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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

ACTION=${1}
shift || true

# Delegando acciones a los módulos/comandos
case ${ACTION} in
	-h|--ayuda|--help)
		if [ -x "$( which man 2>/dev/null )" ]; then
			man canaima-semilla
			exit 0
		else
			USO
			exit 0
		fi
	;;

	-u|--uso|--usage|'')
		USO
		exit 0
	;;

	-v|--version|--about)
		VERSION
		exit 0
	;;

	build|construir)
		HANDLER "build.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;

	profile|perfil)
		HANDLER "profile.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;

	test|probar)
		HANDLER "test.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;

	burn|quemar)
		HANDLER "burn.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;

	*)
		HANDLER "${ACTION}.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;
esac
