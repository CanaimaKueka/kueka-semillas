#!/bin/sh -e

DEBUGMSG() {

	DEBUGVAR="${1}"
	shift || true

	eval "DEBUGVALUE=\${DEBUGVAR}"

	if [ -n "${DEBUGVAR}" ]	&& [ -n "${DEBUGVALUE}" ] && [ -n "${CS_VARDUMP}" ] && [ -z "${CS_QUIET}" ]; then
		printf "${YELLOW}${DEBUGVAR}${END}='${DEBUGVALUE}'\n"
		echo "[DEBUG] ${DEBUGVAR}='${DEBUGVALUE}'" >> "${ISOS}${LOGFILE}"
	fi
}

CONFIGMSG() {

	CONFIGMSG="${1}"
	shift || true

	CONFIGVAR="${1}"
	shift || true

	if [ -n "${CONFIGMSG}" ] && [ -n "${CONFIGVAR}" ] && [ -z "${CS_QUIET}" ]; then
		LOCALIZED="$( gettext -s "${CONFIGMSG}" )"
		printf "${UNDERSCORE}${CONFIGVAR}${END}: ${LOCALIZED} ...\n" ${@}
		echo "[CONFIG] ${CONFIGVAR}: ${LOCALIZED} ..." >> "${ISOS}${LOGFILE}"
	fi
}

INFOMSG() {

	INFOMSG="${1}"
	shift || true

	if [ -n "${INFOMSG}" ] && [ -n "${CS_VERBOSE}" ] && [ -z "${CS_QUIET}" ]; then
		LOCALIZED="$( gettext -s "${INFOMSG}" )"
		printf "${LOCALIZED}\n" ${@}
		echo "[INFO] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}

WARNINGMSG() {

	WARNINGMSG="${1}"
	shift || true

	if [ -n "${WARNINGMSG}" ] && [ -n "${CS_VERBOSE}" ] && [ -z "${CS_QUIET}" ]; then
		LOCALIZED="$( gettext -s "${WARNINGMSG}" )"
		printf "${YELLOW}${LOCALIZED}${END}\n" ${@}
		echo "[WARNING] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}


ERRORMSG() {

	ERRORMSG="${1}"
	shift || true

	if [ -n "${ERRORMSG}" ]; then
		LOCALIZED="$( gettext -s "${ERRORMSG}" )"
		printf "${LRED}${LOCALIZED}${END}\n" ${@}
		echo "[ERROR] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}

SUCCESSMSG() {

	SUCCESSMSG="${1}"
	shift || true

	if [ -n "${SUCCESSMSG}" ]; then
		LOCALIZED="$( gettext -s "${SUCCESSMSG}" )"
		printf "${LGREEN}${LOCALIZED}${END}\n" ${@}
		echo "[SUCCESS] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}

