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

for v in ./conf/variables.conf /usr/share/canaima-semilla/variables.conf; do
	[ -f $v ] && export VARIABLES=$v && break
done

for f in ./scripts/funciones-semilla.sh /usr/share/canaima-semilla/scripts/funciones-semilla.sh; do
	[ -f $f ] && export FUNCIONES=$f && break
done

# Inicializando variables
. ${VARIABLES}

# Cargando funciones
. ${FUNCIONES}

# Comprobaciones varias
CHECK
b=`basename $0`
PATH=`echo $0 |sed s/$b$//`:$PATH

action=$1; shift 1 || true;
# Case encargado de interpretar los parámetros introducidos a
# canaima-semilla y ejecutar la función correspondiente
handler=${PKG}-${action}
[ -e ${handler} ] || handler="$handler.sh"

case ${action} in
	construir) $handler $@ ;;
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
