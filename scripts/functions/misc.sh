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

	if [ "$( ${BIN_FILE} -ib "${IMG}" )" = "${TYPE}" ]; then

		IMG_SIZE="$( ${BIN_IDENTIFY} "${IMG}" | ${BIN_AWK} '{print $3}' )"
		IMG_HSIZE="${IMG_SIZE%x*}"
		IMG_VSIZE="${IMG_SIZE#${IMG_HSIZE}x}"

		if [ ${IMG_HSIZE} -le ${HSIZE} ] && [ ${IMG_VSIZE} -le ${VSIZE} ]; then
			return 1
		else
			return 0
		fi
	else
		return 0
	fi
}

