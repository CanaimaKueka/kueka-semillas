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

# Determinando directorios de trabajo
BINDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ "${BINDIR}" == "/usr/bin"]; then
	LIBFILE="/usr/share/canaima-semilla/scripts/lib.sh"
        VARFILE="/etc/canaima-semilla/variables.conf"
else
        LIBFILE="$( dirname "${BINDIR}" )/scripts/lib.sh"
        VARFILE="$( dirname "${BINDIR}" )/variables.conf"
fi

# Inicializando variables
# Un archivo variables.conf en ${ISO_DIR} sobreescribe la configuración por defecto
for VARIABLES in ${VARFILE} ./variables.conf; do
	if [ -f ${VARIABLES} ]; then
		. ${VARIABLES}
	fi
done

# Inicializando funciones
# Un archivo lib.sh en ${ISO_DIR} sobreescribe la configuración por defecto
for LIBRARIES in ${LIBFILE} ./lib.sh; do
	if [ -f ${LIBRARIES} ]; then
		. ${LIBRARIES}
	fi
done

# Comprobaciones varias
CHECK

# Permite probar desde el directorio de instalación.
#b=`basename $0`
#PATH=`echo $0 |sed s/$b$//`:$SCRIPTS:$PATH

ACTION=${1}; shift 1 || true

# Case encargado de interpretar los parámetros introducidos a
# canaima-semilla y ejecutar la función correspondiente
handler=${PKG}-${action}
which $handler || handler="$handler.sh"
which $handler || ALERT "No se pudo encontrar un handler para $action"

case ${action} in
	construir) $handler $@ ;;
	instalar)
# En Desarrollo
# aptitude install ${SABOR_PAQUETES}
		;;
	probar)
# En Desarrollo
# qemu ISO
		;;
	gui)
# En Desarrollo
		;;
	--ayuda|--help|'')
# Imprimiendo la ayuda
		man canaima-semilla
		;;
esac
