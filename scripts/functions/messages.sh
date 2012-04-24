#!/bin/sh -e

DEBUGMSG() {

	DEBUGVAR="${1}"
	shift || true

	eval "DEBUGVALUE=\${DEBUGVAR}"

	if [ -n "${DEBUGVAR}" ]	&& [ -n "${DEBUGVALUE}" ] && [ "${CS_OP_MODE}" = "vardump" ] && [ "${CS_PRINT_MODE}" = "normal" ]; then
		if [ "${SWITCHLOG}" = "on" ]; then
			printf "${YELLOW}${DEBUGVAR}${END}='${DEBUGVALUE}'\n"
			printf "[DEBUG] ${YELLOW}${DEBUGVAR}${END}='${DEBUGVALUE}'\n" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

CONFIGMSG() {

	CONFIGMSG="${1}"
	shift || true

	CONFIGVAR="${1}"
	shift || true

	if [ -n "${CONFIGMSG}" ] && [ -n "${CONFIGVAR}" ] && [ "${CS_PRINT_MODE}" = "normal" ]; then
		if [ "${SWITCHLOG}" = "on" ]; then
			LOCALIZED="$( gettext -s "${CONFIGMSG}" )"
			printf "${UNDERSCORE}${CONFIGVAR}${END}: ${LOCALIZED} ...\n" ${@}
			printf "[CONFIG] ${UNDERSCORE}${CONFIGVAR}${END}: ${LOCALIZED} ...\n" ${@} >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

INFOMSG() {

	INFOMSG="${1}"
	shift || true

	if [ -n "${INFOMSG}" ] && [ "${CS_PRINT_MODE}" = "verbose" ]; then
		if [ "${SWITCHLOG}" = "on" ]; then
			LOCALIZED="$( gettext -s "${INFOMSG}" )"
			printf "${LOCALIZED}\n" ${@}
			printf "[INFO] ${LOCALIZED}\n" ${@} >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

WARNINGMSG() {

	WARNINGMSG="${1}"
	shift || true

	if [ -n "${WARNINGMSG}" ] && [ "${CS_PRINT_MODE}" = "verbose" ]; then
		if [ "${SWITCHLOG}" = "on" ]; then
			LOCALIZED="$( gettext -s "${WARNINGMSG}" )"
			printf "${YELLOW}${LOCALIZED}${END}\n" ${@}
			printf "[WARNING] ${YELLOW}${LOCALIZED}${END}\n" ${@} >> "${ISOS}/${LOGFILE}"
		fi
	fi
}


ERRORMSG() {

	ERRORMSG="${1}"
	shift || true

	if [ -n "${ERRORMSG}" ]; then
		if [ "${SWITCHLOG}" = "on" ]; then
			LOCALIZED="$( gettext -s "${ERRORMSG}" )"
			printf "${LRED}${LOCALIZED}${END}\n" ${@}
			printf "[ERROR] ${LRED}${LOCALIZED}${END}\n" ${@} >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

SUCCESSMSG() {

	SUCCESSMSG="${1}"
	shift || true

	if [ -n "${SUCCESSMSG}" ]; then
		if [ "${SWITCHLOG}" = "on" ]; then
			LOCALIZED="$( gettext -s "${SUCCESSMSG}" )"
			printf "${LGREEN}${LOCALIZED}${END}\n" ${@}
			printf "[SUCCESS] ${LGREEN}${LOCALIZED}${END}\n" ${@} >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

