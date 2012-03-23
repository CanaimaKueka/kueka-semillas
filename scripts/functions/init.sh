#!/bin/sh -e


# Inicializando variables
# Un archivo variables.conf en ${ISOS} sobreescribe la configuración por defecto
for FILE in ${CONFIG} ${ISOS}extend.conf; do
	if [ -f "${FILE}" ]; then
		. "${FILE}"
	fi
done

# Inicializando funciones
# Un archivo lib.sh en ${ISOS} sobreescribe la configuración por defecto
for FILE in ${LIBRARY} ${ISOS}extend.sh; do
	if [ -f "${FILE}" ]; then
		. "${FILE}"
	fi
done

# Añadiendo directorios de ejecución a ${PATH} para permitir
# ubicarlos rápidamente
export PATH="${BINDIR%/}:${SCRIPTS%/}:${MODULES%/}:${PATH}"

# Comprobando estado previo a la ejecución de módulos
if [ $( id -u ) != 0 ]; then
	ERROR "Canaima Semilla debe ser ejecutado como usuario root."
	exit 1
fi

if [ -x "${CONFIG}" ]; then
	ERROR "El archivo de configuración '%s' no existe o no es ejecutable." "${CONFIG}"
	exit 1
fi

if [ -x "${LIBRARY}" ]; then
	ERROR "La librería de funciones principales '%s' no existe o no es ejecutable." "${LIBRARY}"
	exit 1
fi

if [ ! -d "${FUNCTIONS}" ]; then
	ERROR "El directorio que contiene las funciones '%s' no existe." "${FUNCTIONS}"
	exit 1
fi

if [ ! -d "${MODULES}" ]; then
	ERROR "El directorio que contiene los módulos '%s' no existe." "${MODULES}"
	exit 1
fi

if [ ! -d "${PROFILES}" ]; then
	ERROR "El directorio que contiene los perfiles '%s' no existe." "${PROFILES}"
	exit 1
fi

if [ ! -d "${SCRIPTS}" ]; then
	ERROR "El directorio que contiene los scripts '%s' no existe." "${SCRIPTS}"
	exit 1
fi

if [ ! -d "${ISOS}" ]; then
	ERROR "El directorio de construcción de imágenes '%s' no existe." "${ISOS}"
	exit 1
fi

FUNCTIONS="${FUNCTIONS%/}/"
MODULES="${MODULES%/}/"
PROFILES="${PROFILES%/}/"
SCRIPTS="${SCRIPTS%/}/"
ISOS="${ISOS%/}/"

echo "Iniciando ..."


