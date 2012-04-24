#!/bin/sh -e

MODULE() {

	MODULE="${1}"
	shift || true
	ACTION="${1}"
	shift || true
	BINDIR="${1}"
	shift || true

	if [ -z "${MODULE}" ]; then
		ERROR "La función '%s' necesita el nombre de un módulo como primer argumento." "${FUNCNAME}"
	fi

	if [ -z "${BINDIR}" ]; then
		ERROR "La función '%s' necesita el nombre de un directorio como segundo argumento." "${FUNCNAME}"
	fi

	if [ -x "${MODULES}/${MODULE}" ]; then
		exec "${MODULES}/${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	elif [ -x "/usr/share/canaima-semilla/scripts/modules/${MODULE}" ]; then
		exec "/usr/share/canaima-semilla/scripts/modules/${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	elif [ -x "$( which "${MODULE}" 2>/dev/null )" ]; then
		exec "${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	else
		ERROR "No se ha encontrado '%s', en la carpeta de módulos '%s'."  "${MODULE}" "${MODULES}"
		ERROR "Por favor reinstala canaima-semilla o verifica que has escrito bien el comando."
		exit 1
	fi
}
