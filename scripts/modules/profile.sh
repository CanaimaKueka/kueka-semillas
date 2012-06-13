#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/profile.sh
# DESCRIPCIÓN: Módulo asistente para la construcción de perfiles.
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

ACTION="${1}"
[ -n "${ACTION}" ] && shift 1 || true
BINDIR="${1}"
[ -n "${BINDIR}" ] && shift 1 || true

# Asignando directorios de trabajo
if [ "${BINDIR}" = "/usr/bin" ]; then
        BASEDIR="/usr/share/canaima-semilla"
        CONFDIR="/etc/canaima-semilla"
else
        BASEDIR="$( dirname "${BINDIR}" )"
        CONFDIR="${BASEDIR}"
fi

# Cargando valores predeterminados
. "${BASEDIR}/scripts/functions/defaults.sh"

# Corriendo rutinas de inicio
. "${BASEDIR}/scripts/init.sh"

if [ "${ACTION}" = "perfil" ]; then
	LONGOPTS="crear,listar,ayuda,uso,acerca"
	COMMAND="perfil"
	PARAMETERS="[-c|--crear]\n\
\t[-l|--listar]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

elif [ "${ACTION}" = "profile" ]; then
	LONGOPTS="create,list,help,usage,about"
	COMMAND="profile"
	PARAMETERS="[-c|--create]\n\
\t[-l|--list]\n\
\t[-h|--help]\n\
\t[-u|--usage]\n\
\t[-A|--about]\n"

else
	ERRORMSG "Error interno"
	exit 1
fi

SHORTOPTS="clhuA"
DESCRIPTION="$( NORMALMSG "Comando para la gestión de perfiles de distribuciones derivadas." )"

OPTIONS="$( ${BIN_GETOPT} --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ $? != 0 ]; then
	ERRORMSG "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

while true; do
	case "${1}" in
		-c|--crear|--create)
			PROFILE_OP_MODE="create"
			shift 1 || true
		;;

		-l|--listar|--list)
			PROFILE_OP_MODE="list"
			shift 1 || true
		;;

	        -h|--ayuda|--help)
        	        if ${BIN_MAN} -w "${CS_CMD}_${COMMAND}" 1>/dev/null 2>&1; then
                	        ${BIN_MAN} "${CS_CMD}_${COMMAND}"
                        	exit 0
	                else
        	                USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
	                fi
        	;;

	        -u|--uso|--usage)
        	        USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
	        ;;

        	-A|--acerca|--about)
                	ABOUT
        	;;

                --)
			shift
			break
		;;

                *)
			ERRORMSG "Ocurrió un problema interpretando los parámetros."
			exit 1
		;;
	esac
done

case ${PROFILE_OP_MODE} in
	create)
		PTEMPLATE="${FUNCTIONS}/profile-template.sh"
		PTMP="$( tempfile )"
		VARTMP="$( tempfile )"
		COMTMP="$( tempfile )"
		COPYTMP="$( tempfile )"

		echo
		NORMALMSG "Vamos a hacerte algunas preguntas con respecto a la distribución que deseas crear."
		NORMALMSG "Si no estás seguro de la información que se te pide, puedes presionar CTRL+C"
		NORMALMSG "en cualquier momento y volver a ejecutar el asistente cuando estés listo."
		echo
		NORMALMSG "Estás listo para crear el perfil? Presiona Y para continuar o N para cancelar."

		read -p "[Y/N]" CONTINUE

		if [ "${CONTINUE}" = "Y" ]; then
		        ${BIN_CP} ${PTEMPLATE} ${PTMP}
		        ${BIN_CAT} ${PTEMPLATE} | ${BIN_GREP} ".*=.*@@.*" > ${VARTMP}
        		${BIN_CAT} ${PTEMPLATE} | ${BIN_GREP} "INFOMSG" > ${COMTMP}
        		${BIN_CAT} ${PTEMPLATE} | ${BIN_GREP} "#\[WHERE\]" > ${COPYTMP}
		        COUNT=$( ${BIN_CAT} ${VARTMP} | ${BIN_WC} -l )

		        echo
		        NORMALMSG "Completa la siguiente información y luego presiona la tecla enter para confirmar:"
		        echo

		        for LINE in $( ${BIN_SEQ} 1 ${COUNT} ); do
		                DESCRIPTION="$( ${BIN_SED} -n ${LINE}p ${COMTMP} | ${BIN_SED} 's|INFOMSG ||g;s|"||g' )"
				eval "COPY=\"$( ${BIN_SED} -n ${LINE}p ${COPYTMP} | ${BIN_AWK} '{print $3}' )\""
                		COPYTYPE="$( ${BIN_SED} -n ${LINE}p ${COPYTMP} | ${BIN_AWK} '{print $2}' )"
                		VARONLY="$( ${BIN_SED} -n ${LINE}p ${VARTMP} | ${BIN_SED} "s/=.*//g;s/ //g" )"

		                ${BIN_ECHO} ${DESCRIPTION}
		                read -p "${VARONLY}=" VALUE

				eval "${VARONLY}=\"${VALUE}\""
                		echo

				if [ -n "${COPY}" ] && [ -n "${VALUE}" ]; then
					if  [ -e "${VALUE}" ]; then
						if [ -n "${PROFILE_NAME}" ]; then
							if [ "${COPYTYPE}" = "FOLDER" ]; then
								mkdir -p "${COPY}"
							elif [ "${COPYTYPE}" = "FILE" ]; then
								mkdir -p "$( dirname "${COPY}" )"
							fi
						else
							ERRORMSG "No puede dejar el campo 'PROFILE_NAME' vacío."
							exit 1
						fi
						${BIN_CP} "${VALUE}" "${COPY}"
                				${BIN_SED} -i "s|${VARONLY}=.*|${VARONLY}=\"profile\"|g" ${PTMP}
					else
						ERRORMSG "La ruta '%s' no existe." "${VALUE}"
						exit 1
					fi
				else
					${BIN_SED} -i "s|${VARONLY}=.*|${VARONLY}=\"${VALUE}\"|g" ${PTMP}
				fi
        		done
			${BIN_SED} -i "s|\n#\[WHAT\].*||g;s|\n#\[WHERE\].*||g" ${PTMP}

			${BIN_MKDIR} -p "${PROFILES}/${PROFILE_NAME}"
			${BIN_MV} "${PTMP}" "${PROFILES}/${PROFILE_NAME}/profile.conf"
			${BIN_CHMOD} 644 "${PROFILES}/${PROFILE_NAME}/profile.conf"
			${BIN_RM} -rf "${PTMP}" "${VARTMP}" "${COMTMP}" "${COPYTMP}"
		elif [ "${CONTINUE}" = "N" ]; then
		        ERRORMSG "Cancelado."
		        exit 1
		else
		        ERRORMSG "Opción '%s' desconocida, cancelando." "${CONTINUE}"
		        exit 1
		fi
	;;

	list)
	;;

esac
