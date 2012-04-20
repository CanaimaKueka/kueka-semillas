#!/bin/sh -e

DATE="$( date +%Y%m%d%H%M%S )"
LOGFILE="build.${DATE}.log"
LB_VERSION="$( dpkg-query --show --showformat='${Version}\n' live-build )"

CONFIG="${CONFIG:-${BASEDIR}/scripts/config.sh}"
LIBRARY="${LIBRARY:-${BASEDIR}/scripts/library.sh}"
VARIABLES="${VARIABLES:-${CONFDIR}/variables}"
FUNCTIONS="${FUNCTIONS:-${BASEDIR}/scripts/functions}"
MODULES="${MODULES:-${BASEDIR}/scripts/modules}"
PROFILES="${PROFILES:-${BASEDIR}/profiles}"
SCRIPTS="${SCRIPTS:-${BASEDIR}/scripts}"
ISOS="${ISOS:-${BASEDIR}/isos}"
TEMPLATES="${TEMPLATES:-${BASEDIR}/templates}"

CS_OP_MODE="${CS_OP_MODE:-normal}"
CS_PRINT_MODE="${CS_PRINT_MODE:-normal}"
