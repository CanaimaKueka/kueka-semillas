#!/bin/sh -e

DATE="$( date +%Y%m%d%H%M%S )"
LOGFILE="build.${DATE}.log"
CS_PKG="canaima-semilla"
CS_NAME="Canaima Semilla"
CS_LOG_MAIL="desarrolladores@canaima.softwarelibre.gob.ve"
LB_VERSION="$( dpkg-query --show --showformat='${Version}\n' live-build )"

DEBIAN_DEFAULT_REPO="squeeze"
DEBIAN_DEFAULT_CODENAME="squeeze"
DEBIAN_DEFAULT_REPOSECTIONS="squeeze"

UBUNTU_DEFAULT_REPO="karmic"
UBUNTU_DEFAULT_CODENAME="karmic"
UBUNTU_DEFAULT_CODENAME="karmic"

CANAIMA_DEFAULT_REPO="auyantepui"
CANAIMA_DEFAULT_CODENAME="auyantepui"
CANAIMA_DEFAULT_CODENAME="auyantepui"

CONFIG="${CONFIG:-${CONFDIR}01-core.conf}"
LIBRARY="${LIBRARY:-${BASEDIR}scripts/library.sh}"
FUNCTIONS="${FUNCTIONS:-${BASEDIR}scripts/functions/}"
MODULES="${MODULES:-${BASEDIR}scripts/modules/}"
PROFILES="${PROFILES:-${BASEDIR}profiles/}"
SCRIPTS="${SCRIPTS:-${BASEDIR}scripts/}"
ISOS="${ISOS:-${BASEDIR}isos/}"
TEMPLATES="${TEMPLATES:-${BASEDIR}templates/}"
