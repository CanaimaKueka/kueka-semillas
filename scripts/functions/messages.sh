#!/bin/sh -e

DEBUGMSG() {

	DEBUGVAR="${1}"
	shift || true

	eval "DEBUGVALUE=\${${DEBUGVAR}}"

	if [ -n "${DEBUGVAR}" ]	&& [ -n "${DEBUGVALUE}" ] && [ "${CS_OP_MODE}" = "vardump" ] && [ "${CS_PRINT_MODE}" = "normal" ]; then
			${BIN_PRINTF} "${YELLOW}${DEBUGVAR}${END}='${DEBUGVALUE}'\n"
		if [ "${SWITCHLOG}" = "on" ]; then
			${BIN_PRINTF} "[DEBUG] ${DEBUGVAR}='${DEBUGVALUE}'\n" >> "${ISOS}/${LOGFILE}"
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
		${BIN_PRINTF} "${UNDERSCORE}${CONFIGVAR}${END}: ${LOCALIZED} ...\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			${BIN_PRINTF} "[CONFIG] ${CONFIGVAR}: ${LOCALIZED} ...\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

INFOMSG() {

	INFOMSG="${1}"
	shift || true

	if [ -n "${INFOMSG}" ] && [ "${CS_PRINT_MODE}" = "verbose" ]; then
		LOCALIZED="$( gettext -s "${INFOMSG}" )"
		${BIN_PRINTF} "${LOCALIZED}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			${BIN_PRINTF} "[INFO] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

WARNINGMSG() {

	WARNINGMSG="${1}"
	shift || true

	if [ -n "${WARNINGMSG}" ] && [ "${CS_PRINT_MODE}" = "verbose" ]; then
		LOCALIZED="$( gettext -s "${WARNINGMSG}" )"
		${BIN_PRINTF} "${YELLOW}${LOCALIZED}${END}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			${BIN_PRINTF} "[WARNING] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}


ERRORMSG() {

	ERRORMSG="${1}"
	shift || true

	if [ -n "${ERRORMSG}" ]; then
		LOCALIZED="$( gettext -s "${ERRORMSG}" )"
		${BIN_PRINTF} "${LRED}${LOCALIZED}${END}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			${BIN_PRINTF} "[ERROR] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

SUCCESSMSG() {

	SUCCESSMSG="${1}"
	shift || true

	if [ -n "${SUCCESSMSG}" ]; then
		LOCALIZED="$( gettext -s "${SUCCESSMSG}" )"
		${BIN_PRINTF} "${LGREEN}${LOCALIZED}${END}\n" "${@}"

		if [ "${SWITCHLOG}" = "on" ]; then
			${BIN_PRINTF} "[SUCCESS] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

