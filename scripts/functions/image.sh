#!/bin/sh -e

CS_BUILD_IMAGE() {

	ISOS="${1}"
	shift || true
	CS_OP_MODE="${1}"
	shift || true
	CS_PRINT_MODE="${1}"
	shift || true

	TCSCONFFILE="${ISOS}/config/c-s/tree.conf"

	if [ -f "${TCSCONFFILE}" ]; then
		. "${TCSCONFFILE}"
	else
		WARNINGMSG "El contenedor de construcción parece haber sido configurado manualmente."
		WARNINGMSG "Puede que algunas características de %s no estén disponibles." "${CS_NAME}"

		if      [ -f "${ISOS}/config/common" ] && \
			[ -f "${ISOS}/config/binary" ] && \
			[ -f "${ISOS}/config/chroot" ] && \
			[ -f "${ISOS}/config/bootstrap" ]; then

			. "${ISOS}/config/bootstrap"
			. "${ISOS}/config/chroot"
			. "${ISOS}/config/binary"
			. "${ISOS}/config/common"

			ARCH="${LB_ARCHITECTURES}"
			MEDIO="${LB_BINARY_IMAGES}"
			META_DISTRO="${LB_MODE}"

			case ${MEDIO} in
				usb-hdd|hdd)
					MEDIO_LBNAME="binary.img"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.img"
				;;

				iso)
					MEDIO_LBNAME="binary.iso"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.iso"
				;;

				iso-hybrid)
					MEDIO_LBNAME="binary-hybrid.iso"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.iso"
				;;
			esac
		else
			ERRORMSG "%s no pudo encontrar una configuración apropiada en %s." "${CS_NAME}" "${ISOS}/config"
			exit 1
		fi
	fi

	WARNINGMSG "[--- INICIANDO CONSTRUCCIÓN ---]"
	cd "${ISOS}" && lb build ${LB_QUIET} ${LB_VERBOSE} 2>&1 | tee "${ISOS}/${LOGFILE}"

	if [ -e "${ISOS}/${MEDIO_LBNAME}" ] && [ -n "${MEDIO_CSNAME}" ] && [ -n "${MEDIO_LBNAME}" ]; then

		PESO="$( echo "scale=2;$( stat --format=%s "${ISOS}/${MEDIO_LBNAME}" )/1048576" | bc )MB"
		mv "${ISOS}/${MEDIO_LBNAME}" "${ISOS}/${MEDIO_CSNAME}"

		SUCCESSMSG "Se ha creado una imagen %s con un peso de %s." "${MEDIO}" "${PESO}"
		SUCCESSMSG "Puedes encontrar la imagen '%s' en el directorio %s" "${MEDIO_CSNAME}" "${ISOS}"
		exit 0
	else
		ERRORMSG "Ocurrió un error durante la generación de la imagen."
		ERRORMSG "Si deseas asistencia, puedes enviar un correo a %s con el contenido del archivo '%s'" "${CS_LOG_MAIL}" "${ISOS}/${LOGFILE}"
		exit 1
	fi
}
