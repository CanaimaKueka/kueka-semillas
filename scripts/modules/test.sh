#!/bin/sh -e
#
# ==============================================================================
# PACKAGE: canaima-semilla
# FILE: scripts/modules/build.sh
# DESCRIPCIÓN: Script de sh principal del paquete canaima-desarrollador
# COPYRIGHT:
# (C) 2010 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL3
# ==============================================================================
#
# Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los
# términos de la Licencia Pública General de GNU (versión 3).

ACTION="${1}"
shift || true
BINDIR="${1}"
shift || true

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

if [ "${ACTION}" = "probar" ]; then
	SHORTOPTS="i:memoria:disco:procesadores:"
	LONGOPTS="imagen:"
elif [ "${ACTION}" = "test" ]; then
	SHORTOPTS="i:memory:disk:processors:"
	LONGOPTS="image:"
else
	ERRORMSG "Error interno"
	exit 1
fi

OPTIONS="$( getopt --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ $? != 0 ]; then
	ERRORMSG "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

while true; do
	case "${1}" in
		-i|--imagen|--image)
			IMAGE="${2}"
			shift 2 || true
		;;

		-m|--memoria|--memory)
			MEM="${2}"
			shift 2 || true
		;;

		-d|--disco|--disk-size)
			DISK_SIZE="${2}"
			shift 2 || true
		;;

		-p|--procesadores|--processors)
			PROC="${2}"
			shift 2 || true
		;;

		-c|--iniciar-cd|--start-cd)
			KVM_DISK_MODE="d"
			shift 1 || true
		;;

		-h|--iniciar-dd|--start-hd)
			KVM_DISK_MODE="c"
			shift 1 || true
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

FREE_MEM="$( echo "scale=0;$( cat /proc/meminfo | grep "MemFree:" | awk '{print $2}' )/(10^3)" | bc )"
FREE_DISK="$( echo "scale=0;$( df ${BASEDIR} | grep "/" | awk '{print $4}' )/(10^6)" | bc )"
PROC_NUM="$( cat /proc/cpuinfo | grep -c "processor" )"

if [ -z "${IMAGE}" ]; then
	ERRORMSG "No especificaste una imagen. Abortando."
	exit 1
fi

if [ -z "${DISK_SIZE}" ]; then
	DISK_SIZE="10"
fi

if [ ${FREE_DISK} -lt ${DISK_SIZE} ]; then
	ERRORMSG "El espacio en disco es insuficiente para crear el disco virtual para la prueba. Abortando."
	exit 1
fi

if [ -z "${PROC}" ]; then
	PROC="1"
fi

if [ ${PROC_NUM} -lt ${PROC} ]; then
	ERRORMSG "Se ha asignado un número de procesadores mayor al presente en el sistema. Abortando."
	exit 1
fi

if [ -z "${MEM}" ]; then
	MEM="256"	
fi

if [ ${FREE_MEM} -lt ${MEM} ]; then
	ERRORMSG "El espacio libre en memoria es menor al asignado para la prueba. Abortando."
	exit 1
fi

if kvm-img info ${KVM_IMG} > /dev/null 2>&1 ; then
	if [ "$( kvm-img info hola.img | grep "virtual size: " | sed 's/virtual size: //g' | awk '{print $1}' )" != "${DISK_SIZE}G" ]; then
		rm -rf ${KVM_IMG}
		kvm-img -f qcow2 "${KVM_IMG}" "${DISK_SIZE}G"
	fi
else
	kvm-img -f qcow2 "${KVM_IMG}" "${DISK_SIZE}G"
fi

kvm -snapshot -m "${MEM}" -smp "${PROC}" -boot "${KVM_DISK_MODE}" -hda "${KVM_IMG}" ${IMAGE}
