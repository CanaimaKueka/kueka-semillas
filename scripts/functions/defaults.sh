#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/defaults.sh
# DESCRIPCIÓN: Rutina para la definición de los valores por defecto de las
#              principales variables.
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

DATE="$( date +%Y%m%d%H%M%S )"
LOGFILE="${LOGFILE:-build.${DATE}.log}"
LB_VERSION="$( dpkg-query --show --showformat='${Version}\n' live-build )"
NATIVE_ARCH="$( dpkg --print-architecture )"

CONFIG="${CONFIG:-${BASEDIR}/scripts/config.sh}"
LIBRARY="${LIBRARY:-${BASEDIR}/scripts/library.sh}"
VARIABLES="${VARIABLES:-${CONFDIR}/config/core}"
FUNCTIONS="${FUNCTIONS:-${BASEDIR}/scripts/functions}"
MODULES="${MODULES:-${BASEDIR}/scripts/modules}"
PROFILES="${PROFILES:-${BASEDIR}/profiles}"
SCRIPTS="${SCRIPTS:-${BASEDIR}/scripts}"
ISOS="${ISOS:-${BASEDIR}/isos}"
TEMPLATES="${TEMPLATES:-${BASEDIR}/templates}"

CS_OP_MODE="${CS_OP_MODE:-normal}"
CS_PRINT_MODE="${CS_PRINT_MODE:-normal}"
PROFILE_OP_MODE="${PROFILE_OP_MODE:-create}"

KVM_IMG="${KVM_IMG:-${ISOS}/kvm-img/c-s.img}"
KVM_DISK_MODE="${KVM_DISK_MODE:-d}"

BIN_KVM="${BIN_KVM:-$( which kvm 2>/dev/null )}"
BIN_KVM_IMG="${BIN_KVM_IMG:-$( which kvm-img 2>/dev/null )}"
BIN_CAT="${BIN_CAT:-$( which cat 2>/dev/null )}"
BIN_DF="${BIN_DF:-$( which df 2>/dev/null )}"
BIN_ECHO="${BIN_ECHO:-$( which echo 2>/dev/null )}"
BIN_AWK="${BIN_AWK:-$( which awk 2>/dev/null )}"
BIN_RM="${BIN_RM:-$( which rm 2>/dev/null )}"
BIN_GETOPT="${BIN_GETOPT:-$( which getopt 2>/dev/null )}"
BIN_DPKG="${BIN_DPKG:-$( which dpkg 2>/dev/null )}"
BIN_LB="${BIN_LB:-$( which lb 2>/dev/null )}"
BIN_TEE="${BIN_TEE:-$( which tee 2>/dev/null )}"
BIN_MV="${BIN_MV:-$( which mv 2>/dev/null )}"
BIN_STAT="${BIN_STAT:-$( which stat 2>/dev/null )}"
BIN_BC="${BIN_BC:-$( which bc 2>/dev/null )}"
BIN_GETTEXT="${BIN_GETTEXT:-$( which gettext 2>/dev/null )}"
BIN_PRINTF="${BIN_PRINTF:-$( which printf 2>/dev/null )}"
BIN_FILE="${BIN_FILE:-$( which file 2>/dev/null )}"
BIN_IDENTIFY="${BIN_IDENTIFY:-$( which identify 2>/dev/null )}"
BIN_DIRNAME="${BIN_DIRNAME:-$( which dirname 2>/dev/null )}"
BIN_READLINK="${BIN_READLINK:-$( which readlink 2>/dev/null )}"
BIN_MAN="${BIN_MAN:-$( which man 2>/dev/null )}"
BIN_MKDIR="${BIN_MKDIR:-$( which mkdir 2>/dev/null )}"
BIN_CP="${BIN_CP:-$( which cp 2>/dev/null )}"
BIN_CUT="${BIN_CUT:-$( which cut 2>/dev/null )}"
BIN_GREP="${BIN_GREP:-$( which grep 2>/dev/null )}"
BIN_SED="${BIN_SED:-$( which sed 2>/dev/null )}"
BIN_SEQ="${BIN_SEQ:-$( which seq 2>/dev/null )}"
BIN_WC="${BIN_WC:-$( which wc 2>/dev/null )}"
BIN_CHMOD="${BIN_CHMOD:-$( which chmod 2>/dev/null )}"
