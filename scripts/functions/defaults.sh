#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: .sh
# TIPO: función
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

CS="canaima-semilla"

IDSTRING="${CS}; http://code.google.com/p/canaima-semilla/"

DISTRIBUTION="${DISTRIBUTION:-$( lsb_release -s -i )}"

LOCALE="${LOCALE:-${LC_ALL}}"

CONFIG="${VARFILE:-${CONFDIR}variables.conf}"

LIBRARY="${FUNCTIONS:-${BASEDIR}scripts/functions.sh}"

FUNCTIONDIR="${FUNCTIONDIR:-${BASEDIR}scripts/functions/}"

MODULEDIR="${MODULEDIR:-${BASEDIR}scripts/modules/}"

PROFILES="${PROFILES:-${BASEDIR}profiles/}"

SCRIPTS="${SCRIPTS:-${BASEDIR}scripts/}"

ISODIR="${ISODIR:-${BASEDIR}semillero/}"





