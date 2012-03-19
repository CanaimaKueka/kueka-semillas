#!/bin/sh -e

function HANDLER() {

	if [ -z "${1}" ]; then
		ERROR "La función \"${FUNCNAME}\" necesita un argumento."
	fi

	MODULE=${1}

	if [ -x "${MODULEDIR}${MODULE}" ]; then
		exec "${MODULEDIR}${MODULE}" "$@"
	elif [ -x "/usr/share/canaima-semilla/scripts/modules/${MODULE}" ]; then
		exec "/usr/share/canaima-semilla/scripts/modules/${MODULE}" "$@"
	elif [ -x "$( which "${MODULE}" 2>/dev/null )" ]; then
		exec "${MODULE}" "$@"
	else
		ERROR "No se ha encontrado \"${MODULE}\", en la carpeta de módulos \"${MODULEDIR}\"."
		ERROR "Por favor reinstala canaima-semilla o verifica que has escrito bien el comando."
		exit 1
	fi
}
