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

