#!/bin/sh -e

DEBUGMSG() {

	DEBUGVAR="${1}"
	shift || true

	eval "DEBUGVALUE=\${${DEBUGVAR}}"

	if [ -n "${DEBUGVAR}" ]	&& [ -n "${DEBUGVALUE}" ] && [ "${CS_OP_MODE}" = "vardump" ] && [ "${CS_PRINT_MODE}" = "normal" ]; then
			printf "${YELLOW}${DEBUGVAR}${END}='${DEBUGVALUE}'\n"
		if [ "${SWITCHLOG}" = "on" ]; then
			printf "[DEBUG] ${DEBUGVAR}='${DEBUGVALUE}'\n" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

CONFIGMSG() {

	CONFIGMSG="${1}"
	shift || true

	CONFIGVAR="${1}"
	shift || true

	if [ -n "${CONFIGMSG}" ] && [ -n "${CONFIGVAR}" ] && [ "${CS_PRINT_MODE}" = "normal" ]; then
		LOCALIZED="$( gettext -s "${CONFIGMSG}" )"
		printf "${UNDERSCORE}${CONFIGVAR}${END}: ${LOCALIZED} ...\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			printf "[CONFIG] ${CONFIGVAR}: ${LOCALIZED} ...\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

INFOMSG() {

	INFOMSG="${1}"
	shift || true

	if [ -n "${INFOMSG}" ] && [ "${CS_PRINT_MODE}" = "verbose" ]; then
		LOCALIZED="$( gettext -s "${INFOMSG}" )"
		printf "${LOCALIZED}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			printf "[INFO] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

WARNINGMSG() {

	WARNINGMSG="${1}"
	shift || true

	if [ -n "${WARNINGMSG}" ] && [ "${CS_PRINT_MODE}" = "verbose" ]; then
		LOCALIZED="$( gettext -s "${WARNINGMSG}" )"
		printf "${YELLOW}${LOCALIZED}${END}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			printf "[WARNING] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}


ERRORMSG() {

	ERRORMSG="${1}"
	shift || true

	if [ -n "${ERRORMSG}" ]; then
		LOCALIZED="$( gettext -s "${ERRORMSG}" )"
		printf "${LRED}${LOCALIZED}${END}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			printf "[ERROR] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

SUCCESSMSG() {

	SUCCESSMSG="${1}"
	shift || true

	if [ -n "${SUCCESSMSG}" ]; then
		LOCALIZED="$( gettext -s "${SUCCESSMSG}" )"
		printf "${LGREEN}${LOCALIZED}${END}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			printf "[SUCCESS] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

