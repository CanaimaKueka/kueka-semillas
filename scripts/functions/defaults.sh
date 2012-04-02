#!/bin/sh -e

DATE="$( date +%Y%m%d%H%M%S )"
LOGFILE="build.${DATE}.log"
CS_PKG="canaima-semilla"
CS_NAME="Canaima Semilla"
CS_LOG_MAIL="desarrolladores@canaima.softwarelibre.gob.ve"
LB_VERSION="$( dpkg-query --show --showformat='${Version}\n' live-build )"
IDSTRING="${CS_NAME}; http://code.google.com/p/canaima-semilla/"

DEBIAN_CODENAMES="lenny squeeze wheezy sid"
UBUNTU_CODENAMES="lenny squeeze wheezy sid"
CANAIMA_CODENAMES="roraima auyantepui"

CONFIG="${CONFIG:-${CONFDIR}01-core.conf}"
LIBRARY="${LIBRARY:-${BASEDIR}scripts/library.sh}"
FUNCTIONS="${FUNCTIONS:-${BASEDIR}scripts/functions/}"
MODULES="${MODULES:-${BASEDIR}scripts/modules/}"
PROFILES="${PROFILES:-${BASEDIR}profiles/}"
SCRIPTS="${SCRIPTS:-${BASEDIR}scripts/}"
ISOS="${ISOS:-${BASEDIR}isos/}"
TEMPLATES="${TEMPLATES:-${BASEDIR}templates/}"
