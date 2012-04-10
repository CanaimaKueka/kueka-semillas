#!/bin/sh -e


IMG_VALIDATOR() {

	IMG="${1}"
	shift || true
	HSIZE="${1}"
	shift || true
	VSIZE="${1}"
	shift || true
	TYPE="${1}"
	shift || true

	if [ "$( file -ib "${IMG}" )" = "${TYPE}" ]; then

		IMG_SIZE="$( identify "${IMG}" | awk '{print $3}' )"
		IMG_HSIZE="${IMG_SIZE%x*}"
		IMG_VSIZE="${IMG_SIZE#${IMG_HSIZE}x}"

		if [ ${IMG_HSIZE} -le ${HSIZE} ] && [ ${IMG_VSIZE} -le ${VSIZE} ]; then
			return true
		else
			return false
		fi
	else
		return false
	fi
}

HANDLER() {

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

	if [ -x "${MODULES}${MODULE}" ]; then
		exec "${MODULES}${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
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
