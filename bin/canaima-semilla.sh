#!/bin/bash -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: canaima-semilla.sh
# DESCRIPCIÓN: Script de bash principal del paquete canaima-desarrollador
# COPYRIGHT:
#  (C) 2010 Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
# LICENCIA: GPL3
# ==============================================================================
#
# Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los
# términos de la Licencia Pública General de GNU (versión 3).

VARIABLES="/home/luis/desarrollo/canaima-semilla/conf/variables.conf"

# Inicializando variables
. ${VARIABLES}

# Cargando configuración
. ${CONF}

# Cargando funciones
. ${FUNCIONES}

# Case encargado de interpretar los parámetros introducidos a
# canaima-desarrollador y ejecutar la función correspondiente
case ${1} in

construir)

PARAMETROS=${@}
PARAMETROS=${PARAMETROS#construir}

for ARGUMENTO in ${PARAMETROS}
do
ARG_VARIABLE=${ARGUMENTO#--}
ARG_VARIABLE=${ARG_VARIABLE%=*}
ARG_VALOR=${ARGUMENTO#--${ARG_VARIABLE}=}
ARG_VARIABLE=$( echo ${ARG_VARIABLE} | tr '[:lower:]' '[:upper:]' )
eval "${ARG_VARIABLE}=${ARG_VALOR}"
case ${ARG_VARIABLE} in

ARQUITECTURA)
case ${ARQUITECTURA} in
amd64|x64|64|x86_64)
ARQUITECTURA="amd64"
SABOR_KERNEL="amd64"
ADVERTENCIA "Arquitectura: amd64"
;;
i386|486|686|i686)
ARQUITECTURA="i386"
SABOR_KERNEL="686"
ADVERTENCIA "Arquitectura: i386"
;;
*|'')
ERROR "Arquitectura ${ARQUITECTURA} no soportada en Canaima. Abortando."
;;
esac
;;

SABOR)

for SABORES in $( ls -F ${PLANTILLAS} | grep "/" )
do
if [ ${SABORES} == ${SABOR} ]
then
. "${PLANTILLAS}${SABOR}/sabor.conf"
else
ERROR "Sabor ${SABOR} desconocido o no disponible. Abortando."
fi
done


;;


MEDIO)
;;

esac

done

cd ${ISO_DIR}
lb clean
rm -rf auto config .stage
rm -rf binary.log

lb config --architecture="${ARQUITECTURA}" --distribution="${SABOR_DIST}" --apt="aptitude" \
--apt-recommends="false" --bootloader="syslinux" --binary-images="${IMAGEN}" \
--bootstrap="debootstrap" --binary-indices="false" --includes="none" --username="usuario-nvivo" \
--hostname="canaima-${SABOR}" --mirror-chroot-security="none" --mirror-binary-security="none" \
--language="es" --bootappend-live="locale=es_VE.UTF-8 keyb=es quiet splash vga=791" --security="false" \
--volatile="false" --source="false" --iso-preparer="${PREPARADO_POR}" \
--iso-volume="Canaima \$(date +%Y%m%d-%H:%M)" --iso-publisher="${PUBLICADO_POR}" \
--iso-application="${APLICACION}" --mirror-bootstrap="${SEMILLA_BOOTSTRAP}" --mirror-binary="${SEMILLA_BINARY}" \
--mirror-chroot="${SEMILLA_CHROOT}" --mirror-security="${SEMILLA_SEGURIDAD}" --memtest="none" --linux-flavours="${SABOR_KERNEL}" --syslinux-menu="true" \
--syslinux-timeout="3"


;;

instalar)

;;

probar)
;;

gui)
;;

--ayuda|--help|'')
# Imprimiendo la ayuda
echo "Canaima Desarrollador es una herramienta destinada a facilitar la creación de"
;;

esac

exit 0
