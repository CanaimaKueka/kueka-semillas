#!/bin/sh -e

MENSAJE() {

	MESSAGE="${1}"
	shift || true

	if [ -n "${MESSAGE}" ]; then
		LOCALIZED="$( gettext -s "${MESSAGE}" )"
		printf "${LOCALIZED}\n" ${@}
		echo "[MENSAJE] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}

ADVERTENCIA() {

	MESSAGE="${1}"
	shift || true

	if [ -n "${MESSAGE}" ]; then
		LOCALIZED="$( gettext -s "${MESSAGE}" )"
		printf "${YELLOW}${LOCALIZED}${END}\n" ${@}
		echo "[ADVERTENCIA] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}


ERROR() {

	MESSAGE="${1}"
	shift || true

	if [ -n "${MESSAGE}" ]; then
		LOCALIZED="$( gettext -s "${MESSAGE}" )"
		printf "${LRED}${LOCALIZED}${END}\n" ${@}
		echo "[ERROR] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}

EXITO() {

	MESSAGE="${1}"
	shift || true

	if [ -n "${MESSAGE}" ]; then
		LOCALIZED="$( gettext -s "${MESSAGE}" )"
		printf "${LGREEN}${LOCALIZED}${END}\n" ${@}
		echo "[EXITO] ${LOCALIZED}" >> "${ISOS}${LOGFILE}"
	fi
}

