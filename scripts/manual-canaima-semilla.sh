#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: manual-semilla.sh
# DESCRIPCIÓN: Script que inicia el Manual de Canaima Semilla
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

${NAVEGADOR} /usr/share/doc/canaima-semilla/html/index.html
