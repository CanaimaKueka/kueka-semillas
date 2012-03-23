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

DATE="$( date +%Y%m%d%H%M%S )"
LOGFILE="build.${DATE}.log"
CS_PKG="canaima-semilla"

CS_NAME="Canaima Semilla"

LB_VERSION="$( dpkg-query --show --showformat='${Version}\n' live-build )"

IDSTRING="${CS_NAME}; http://code.google.com/p/canaima-semilla/"

CONFIG="${CONFIG:-${CONFDIR}01-core.conf}"
LIBRARY="${LIBRARY:-${BASEDIR}scripts/library.sh}"
FUNCTIONS="${FUNCTIONS:-${BASEDIR}scripts/functions/}"
MODULES="${MODULES:-${BASEDIR}scripts/modules/}"
PROFILES="${PROFILES:-${BASEDIR}profiles/}"
SCRIPTS="${SCRIPTS:-${BASEDIR}scripts/}"
ISOS="${ISOS:-${BASEDIR}isos/}"
TEMPLATES="${TEMPLATES:-${BASEDIR}templates/}"

AUTHOR_NAME="${AUTHOR_NAME:-Equipo de desarrollo de Canaima GNU/Linux}"
AUTHOR_EMAIL="${AUTHOR_EMAIL:-desarrolladores@canaima.softwarelibre.gob.ve}"
AUTHOR_URL="${AUTHOR_URL:-http://canaima.softwarelibre.gob.ve/}"

META_DISTRO="${META_DISTRO:-$( echo "$( lsb_release -s -i )" | tr '[:upper:]' '[:lower:]' )}"
META_CODENAME="${META_CODENAME:-$( echo "$( lsb_release -s -c )" | tr '[:upper:]' '[:lower:]' )}"
DEFAULT_PROFILE="${DEFAULT_PROFILE:-default}"

case ${META_DISTRO} in
	debian)
		META_MODE="${META_MODE:-debian}"
		META_REPO="${META_REPO:-http://ftp.us.debian.org/debian/}"
		META_REPOSECTIONS="${META_REPOSECTIONS:-main contrib non-free}"
	;;

	canaima)
		META_MODE="${META_MODE:-debian}"
		META_REPO="${META_REPO:-http://universo.canaima.softwarelibre.gob.ve/}"
		META_REPOSECTIONS="${META_REPOSECTIONS:-main contrib non-free}"
	;;

	ubuntu)
		META_MODE="${META_MODE:-ubuntu}"
		META_REPO="${META_REPO:-http://archive.ubuntu.com/ubuntu/}"
		META_REPOSECTIONS="${META_REPOSECTIONS:-main restricted}"
	;;

	*)
		META_REPO="${META_REPO:-http://universo.canaima.softwarelibre.gob.ve/}"
		META_REPOSECTIONS="${META_REPOSECTIONS:-main contrib non-free}"
	;;
esac

OS_PACKAGES="${OS_PACKAGES:-gnome-core xorg}"
OS_BOOTLOADER="${OS_BOOTLOADER:-grub}"
OS_LOCALE="${OS_LOCALE:-${LC_ALL}}"
OS_LANG="${OS_LANG:-$( echo "${OS_LOCALE}" | sed 's/_.*//g' )}"
#OS_INCLUDES="${OS_INCLUDES:-${PROFILES}${DEFAULT_PROFILE}/OS_INCLUDES/}"
#OS_HOOKS="${OS_HOOKS:-${PROFILES}${DEFAULT_PROFILE}/OS_HOOKS/}"

IMG_POOL_PACKAGES="${IMG_POOL_PACKAGES:-grub grub-pc}"
IMG_SYSLINUX_SPLASH="${IMG_SYSLINUX_SPLASH:-${TEMPLATES}profiles/${DEFAULT_PROFILE}/syslinux.png}"
IMG_DEBIAN_INSTALLER="${IMG_DEBIAN_INSTALLER:-false}"
#IMG_DEBIAN_INSTALLER_BANNER="${IMG_DEBIAN_INSTALLER_BANNER:-${PROFILES}${DEFAULT_PROFILE}/DEBIAN_INSTALLER/banner.png}"
#IMG_DEBIAN_INSTALLER_PRESEED="${IMG_DEBIAN_INSTALLER_PRESEED:-${PROFILES}${DEFAULT_PROFILE}/DEBIAN_INSTALLER/preseed.cfg}"
#IMG_DEBIAN_INSTALLER_GTK="${IMG_DEBIAN_INSTALLER_GTK:-${PROFILES}${DEFAULT_PROFILE}/DEBIAN_INSTALLER/gtkrc}"
#IMG_INCLUDES="${IMG_INCLUDES:-${PROFILES}${DEFAULT_PROFILE}/IMG_INCLUDES/}"
#IMG_HOOKS="${IMG_HOOKS:-${PROFILES}${DEFAULT_PROFILE}/IMG_HOOKS/}"




