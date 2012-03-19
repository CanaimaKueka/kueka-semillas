#!/bin/sh -e


# Inicializando variables
# Un archivo variables.conf en ${ISODIR} sobreescribe la configuración por defecto
for FILE in ${CONFIG} ${ISODIR}/variables.conf; do
	if [ -f "${FILE}" ]; then
		. "${FILE}"
	fi
done

# Inicializando funciones
# Un archivo lib.sh en ${ISODIR} sobreescribe la configuración por defecto
for FILE in ${LIBRARY} ${ISODIR}/functions.sh; do
	if [ -f "${FILE}" ]; then
		. "${FILE}"
	fi
done

# Añadiendo directorios de ejecución a ${PATH} para permitir
# ubicarlos rápidamente
export PATH="${BINDIR%/}:${SCRIPTS%/}:${MODULEDIR%/}:${PATH}"

# Comprobando estado previo a la ejecución de módulos
if [ $( id -u ) != 0 ]; then
	ERROR "Canaima Semilla debe ser ejecutado como usuario root."
	exit 1
fi

if [ -x "${CONFIG}" ]; then
	ERROR "El archivo de configuración \"${CONFIG}\" no existe o no es ejecutable."
	exit 1
fi

if [ -x "${LIBRARY}" ]; then
	ERROR "La librería de funciones principales \"${LIBRARY}\" no existe o no es ejecutable."
	exit 1
fi

if [ ! -d "${FUNCTIONDIR}" ]; then
	ERROR "El directorio que contiene las funciones \"${FUNCTIONDIR}\" no existe."
	exit 1
fi

if [ ! -d "${MODULEDIR}" ]; then
	ERROR "El directorio que contiene los módulos \"${MODULEDIR}\" no existe."
	exit 1
fi

if [ ! -d "${PROFILES}" ]; then
	ERROR "El directorio que contiene los perfiles \"${PROFILES}\" no existe."
	exit 1
fi

if [ ! -d "${SCRIPTS}" ]; then
	ERROR "El directorio que contiene los scripts \"${SCRIPTS}\" no existe."
	exit 1
fi

if [ ! -d "${ISODIR}" ]; then
	ERROR "El directorio de construcción de imágenes \"${ISODIR}\" no existe."
	exit 1
fi

FUNCTIONDIR="${FUNCTIONDIR%/}/"
MODULEDIR="${MODULEDIR%/}/"
PROFILES="${PROFILES%/}/"
SCRIPTS="${SCRIPTS%/}/"
ISODIR="${ISODIR%/}/"

echo "Iniciando ..."


