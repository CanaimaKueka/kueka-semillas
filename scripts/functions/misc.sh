#!/bin/sh -e

function HANDLER() {

	MODULE="${1}"
	shift || true
	ACTION="${1}"
	shift || true
	BINDIR="${1}"
	shift || true

	if [ -z "${MODULE}" ]; then
		ERROR "La función \"${FUNCNAME}\" necesita el nombre de un módulo como primer argumento."
	fi

	if [ -z "${BINDIR}" ]; then
		ERROR "La función \"${FUNCNAME}\" necesita el nombre de un directorio como segundo argumento."
	fi

	if [ -x "${MODULES}${MODULE}" ]; then
		exec "${MODULES}${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	elif [ -x "/usr/share/canaima-semilla/scripts/modules/${MODULE}" ]; then
		exec "/usr/share/canaima-semilla/scripts/modules/${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	elif [ -x "$( which "${MODULE}" 2>/dev/null )" ]; then
		exec "${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	else
		ERROR "No se ha encontrado \"${MODULE}\", en la carpeta de módulos \"${MODULES}\"."
		ERROR "Por favor reinstala canaima-semilla o verifica que has escrito bien el comando."
		exit 1
	fi
}
