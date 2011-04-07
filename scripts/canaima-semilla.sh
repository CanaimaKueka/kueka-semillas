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

VARIABLES="/usr/share/canaima-semilla/variables.conf"

# Inicializando variables
. ${VARIABLES}

# Cargando funciones
. ${FUNCIONES}

# Comprobaciones varias
CHECK

# Case encargado de interpretar los parámetros introducidos a
# canaima-semilla y ejecutar la función correspondiente
case ${1} in

# En caso de que queramos construir una ISO
construir)

# Capturamos todos los parámetros de entrada
PARAMETROS=${@}
# Removemos el ayudante
PARAMETROS=${PARAMETROS#construir}

[ $( echo ${PARAMETROS} | grep -c "\-\-arquitectura=" ) == 0 ] && PARAMETROS='--arquitectura="" '${PARAMETROS}
[ $( echo ${PARAMETROS} | grep -c "\-\-medio=" ) == 0 ] && PARAMETROS='--medio="" '${PARAMETROS}
[ $( echo ${PARAMETROS} | grep -c "\-\-sabor=" ) == 0 ] && PARAMETROS='--sabor="" '${PARAMETROS}

# Para cada argumento ...
for ARGUMENTO in ${PARAMETROS}; do

# Removemos los guiones y la igualdad para aislar el nombre de la variable
# en ${ARG_VARIABLE}
ARG_VARIABLE=${ARGUMENTO#--}
ARG_VARIABLE=${ARG_VARIABLE%=*}
# Removemos la variable para aislar el valor de la variable
ARG_VALOR=${ARGUMENTO#--${ARG_VARIABLE}=}
# Convertiomos la variable en mayúscula
ARG_VARIABLE=$( echo ${ARG_VARIABLE} | tr '[:lower:]' '[:upper:]' )
# Evaluamos la expresión para usar las variables
eval "${ARG_VARIABLE}=${ARG_VALOR}"

# Case para validaciones diversas 
case ${ARG_VARIABLE} in

ARQUITECTURA)

# Establecemos la arquitectura del host, si no se especifica
[ -z ${ARQUITECTURA} ] && ARQUITECTURA=$( uname -m ) && ADVERTENCIA 'No especificaste una arquitectura, utilizando "'${ARQUITECTURA}'" presente en el sistema.'

case ${ARQUITECTURA} in
amd64|x64|64|x86_64)
ARQUITECTURA="amd64"
SABOR_KERNEL="amd64"
EXITO "Arquitectura: amd64"
;;
i386|486|686|i686)
ARQUITECTURA="i386"
SABOR_KERNEL="686"
EXITO "Arquitectura: i386"
;;
*)
ERROR 'Arquitectura "'${ARQUITECTURA}'" no soportada en Canaima. Abortando.'
;;
esac
;;

SABOR)

# Establecemos el sabor por defecto "popular", en caso de no especificar ninguno
[ -z ${SABOR} ] && SABOR="popular" && ADVERTENCIA 'No especificaste un sabor, utilizando sabor "popular" por defecto.'

rm -rf ${ISO_DIR}config

for SABORES in $( ls -F ${PLANTILLAS} | grep "/" ); do
if [ "${SABORES}" == "${SABOR}/" ]; then
	CONFIGURAR-SABOR
fi
done

if [ -e ${ISO_DIR}config/sabor-configurado ]; then
EXITO "Sabor: ${SABOR}"
else
ERROR 'Sabor "'${SABOR}'" desconocido o no disponible. Abortando.'
fi

;;

MEDIO)

# Establecemos medio "iso", en caso de no especificar ninguno
[ -z ${MEDIO} ] && MEDIO="iso" && ADVERTENCIA 'Utilizando medio "iso"'

case ${MEDIO} in
usb|usb-hdd|img|USB)
MEDIO="usb"
EXITO "Medio: Dispositivos de almacenamiento extraíble (USB)"
;;
iso|ISO|CD|DVD)
MEDIO="iso"
EXITO "Medio: Dispositivos de almacenamiento extraíble (CD/DVD)"
;;
*)
ERROR 'Medio "'${MEDIO}'" no reconocido por Canaima. Abortando.'
;;
esac

;;

esac

done

SEMILLA_BOOTSTRAP=${MIRROR_DEBIAN}
SEMILLA_CHROOT=${MIRROR_DEBIAN}
SEMILLA_BINARY=${MIRROR_DEBIAN}

cd ${ISO_DIR}

ADVERTENCIA "Limpiando posibles residuos de construcciones anteriores ..."
rm -rf ${ISO_DIR}.stage ${ISO_DIR}auto ${ISO_DIR}binary.log ${ISO_DIR}cache/stages_bootstrap/
lb clean

ADVERTENCIA "Generando árbol de configuraciones ..."
lb config --architecture="${ARQUITECTURA}" --distribution="${SABOR_DIST}" --apt="aptitude" --apt-recommends="false" --bootloader="syslinux" --binary-images="${MEDIO}" --bootstrap="debootstrap" --binary-indices="false" --includes="none" --username="usuario-nvivo" --hostname="canaima-${SABOR}" --mirror-chroot-security="none" --mirror-binary-security="none" --language="es" --bootappend-live="locale=es_VE.UTF-8 keyb=es quiet splash vga=791 live-config.user-fullname=Canaima" --security="false" --volatile="false" --backports="false" --source="false" --iso-preparer="${PREPARADO_POR}" --iso-volume="canaima-${SABOR}" --iso-publisher="${PUBLICADO_POR}" --iso-application="${APLICACION}" --mirror-bootstrap="${SEMILLA_BOOTSTRAP}" --mirror-binary="${SEMILLA_BINARY}" --mirror-chroot="${SEMILLA_CHROOT}" --memtest="none" --linux-flavours="${SABOR_KERNEL}" --syslinux-menu="true" --syslinux-timeout="5" --archive-areas="${COMP_MIRROR_DEBIAN}" --debian-installer="live" --packages="${SABOR_PAQUETES}" --syslinux-splash="${SABOR_SYSPLASH}" --win32-loader="false" --bootappend-install="locale=es_VE.UTF-8"

sed -i 's/LB_SYSLINUX_MENU_LIVE_ENTRY=.*/LB_SYSLINUX_MENU_LIVE_ENTRY="Probar"/g' config/binary

ADVERTENCIA "Construyendo ..."
lb build 2>&1 | tee binary.log

if [ ${MEDIO} == "iso" ] && [ -e ${ISO_DIR}binary.iso ]; then
	PESO=$( ls -lah ${ISO_DIR}binary.iso | awk '{print $5}' )
	mv ${ISO_DIR}binary.iso canaima-${SABOR}_${ARQUITECTURA}.iso
	EXITO "¡Enhorabuena! Se ha creado una imagen ISO de canaima-${SABOR}, que pesa ${PESO}."
	EXITO "Puedes encontrar la imagen \"canaima-${SABOR}_${ARQUITECTURA}.iso\" en el directorio /usr/share/canaima-semilla/semillero/"
elif [ ${MEDIO} == "usb" ] && [ -e ${ISO_DIR}binary.img ]; then
	PESO=$( ls -lah ${ISO_DIR}binary.img | awk '{print $5}' )
	mv ${ISO_DIR}binary.img canaima-${SABOR}_${ARQUITECTURA}.img
	EXITO "¡Enhorabuena! Se ha creado una imagen IMG de canaima-${SABOR}, que pesa ${PESO}."
	EXITO "Puedes encontrar la imagen \"canaima-${SABOR}_${ARQUITECTURA}.img\" en el directorio /usr/share/canaima-semilla/semillero/"
else
	ERROR "Ocurrió un error durante la generación de la imagen."
	ERROR "Envía un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo ${ISO_DIR}binary.log"
fi

;;

instalar)
# En Desarrollo
# aptitude install ${SABOR_PAQUETES}
;;

probar)
# En Desarrollo
# qemu ISO
;;

gui)
# En Desarrollo
;;

--ayuda|--help|'')
# Imprimiendo la ayuda
man canaima-semilla
;;

esac

exit 0
