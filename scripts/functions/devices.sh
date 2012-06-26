#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/devices.sh
# DESCRIPCIÓN: Lista los dispositivos ópticos y/o usb disponibles para grabar
#              imágenes instalables.
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

LIST_DEV() {

        # ======================================================================
        # FUNCIÓN: LIST_DEV
        # DESCRIPCIÓN: Lista los dispositivos ópticos y/o usb disponibles.
        # ENTRADAS:
        #       [ISOS]: Directorio donde se encuentra el árbol de configuración.
        #       [BUILD_OP_MODE]: Modo de operación. 
        #       [BUILD_PRINT_MODE]: Modo de verbosidad.
        # ======================================================================

        TYPE="${1}"
        [ -n "${TYPE}" ] && shift 1 || true



}
