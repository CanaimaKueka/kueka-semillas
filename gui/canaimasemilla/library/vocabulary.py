#!/usr/bin/python
#-*- coding: UTF-8 -*-

import gettext, locale
from gettext import gettext as _

from config import *

settinglocale = locale.setlocale(locale.LC_ALL, '')
naminglocale = LOCALEDIR+'/'+locale.getlocale()[0]+'/LC_MESSAGES/c-s-gui.mo'

try:
    trans = gettext.GNUTranslations(open(naminglocale, 'rb'))
except IOError:
    trans = gettext.NullTranslations()

installinglocale = trans.install()

MainWindowTitle = _('Generador de Distribuciones Derivadas')
CrearPerfilTitle = _('Crear perfil')
CrearImagenTitle = _('Crear imagen')
ProbarImagenTitle = _('Probar imagen')
GrabarImagenTitle = _('Grabar imagen')
CrearPerfilLabel = _('Inicia un asistente que permite construir un perfil para una nueva distribución derivada.')
CrearImagenLabel = _('Crea una imagen de un Sistema Operativo construido en base a un perfil.')
ProbarImagenLabel = _('Inicia un emulador que permite ejecutar el Sistema Operativo contenido en una imagen.')
GrabarImagenLabel = _('Inicia un asistente que permite grabar una imagen en un dispositivo de almacenamiento.')


BuildImageTitle = _('Creación de imágenes a partir de perfiles existentes')
BuildImageIntro = _('Canaima Semilla puede crear imágenes instalables (ISO o IMG) basado en los perfiles de sabores existentes. Puede especificársele el tipo de Medio, la arquitectura a construir, y el nombre del sabor.')
MedioOptionLabel = _('Seleccione el formato de archivo de la imagen:')
MedioOptionIso = _('ISO: Imagen para dispositivos ópticos de almacenamiento (CD/DVD).')
MedioOptionImg = _('IMG: Imagen para dispositivos de almacenamiento extraíble (USB).')
MedioOptionHybrid = _('HÍBRIDA: Imagen mixta para dispositivos variados (CD/DVD/USB) [Recomendado].')
ArchOptionLabel = _('Seleccione el tipo de arquitectura de la imagen:')
ArchOptionI386 = _('x86: Arquitectura de procesadores con soporte para 32 bits [Recomendado].')
ArchOptionAmd64 = _('x86_64: Arquitectura de procesadores con soporte para 64 bits.')
SaborOptionLabel = _('Seleccione el perfil del sistema operativo a incluir en la imagen:')
BuildImageTimeLabel = _('El proceso de construcción de la imagen puede completarse en unos cuantos minutos o en varias horas, dependiendo de la velocidad de su conexión a internet y la capacidad de procesamiento de su computador.')
BuildImageEndLabel = _('Cuando esté preparado para iniciar la construcción, presione el botón generar.')
CancelLabel = _('Cancelar')
ConfirmCancelBuildImageLabel = _('¿Está seguro que desea cancelar la creación de la imagen?')
MustSelectArchLabel = _('"\tDebe seleccionar La Arquitectura i386 o amd64\t\t"')
MustSelectArchTitle = _('Error i386 o amd64')
MustSelectSaborLabel = _('"\tDebe seleccionar un sabor\t\t"')
MustSelectSaborTitle = _('Error sabor')
LooksLikeNoInternetLabel = _('Parece que no tiene internet')
LooksLikeNoInternetTitle = _('Parece que no tiene internet')
BuildingImage = _('"CONSTRUYENDO IMAGEN"')
ImageBuiltSuccessfully = _('"\tSe ha creado una imagen ISO de canaima-%s.\n\n\tLa imagen ''canaima-%s_i386.iso'' resultante \n\tde los proceso de construcción se encuentra en la \n\tdireccion:\t\n\n\t\t/usr/share/canaima-semilla/semillero/"')
DoneLabel = _('Finalizado')
ImageBuiltError = _('"Ocurrio un error durante la generacion de la imagen. Envie un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo /usr/share/canaima-semilla/semillero/binary.log"')
ErrorLabel = _('Ocurrió un error')
ImageBuiltCancelled = _('"\tLa construcción de la imagen ISO de\n\tcanaima-%s ha sido cancelada.\t"')
CancelledLabel = _('Ocurrió un error')

PROFILE_TITLE = _('Creación de perfiles para distribuciones derivadas')
PROFILE_PROFILE_NAME_1 = _('Introduzca el nombre del sabor a crear:')
PROFILE_PROFILE_NAME_2 = _('Debe introducir el nombre con el que desea identificar la distribución derivada que está creando, en minúsculas y sin espacios.')
PROFILE_AUTHOR_NAME_1 = _('Introduzca el nombre de la persona o grupo responsable:')
PROFILE_AUTHOR_NAME_2 = _('Debe introducir el nombre de la persona o grupo responsable de la creación y mantenimiento del sabor.')
PROFILE_AUTHOR_EMAIL_1 = _('Introduzca el correo electrónico de la persona o grupo responsable:')
PROFILE_AUTHOR_EMAIL_2 = _('Debe introducir un correo electrónico válido para contacto de la persona o grupo responsable de la creación y mantenimiento del sabor.')
PROFILE_AUTHOR_URL_1 = _('Introduzca una dirección web para la persona o grupo responsable:')
PROFILE_AUTHOR_URL_2 = _('Puede introducir una dirección web de referencia para mayor información acerca del sabor.')
PROFILE_META_DIST_1 = _('Seleccione la Metadistribución base de sabor:')
PROFILE_META_DIST_2 = _('Seleccione la Metadistribución que será la base del sabor en construcción.')
PROFILE_META_CODENAME_1 = _('Seleccione el nombre código de la Metadistribución:')
PROFILE_META_CODENAME_2 = _('Seleccione la Metadistribución que será la base del sabor en construcción.')
PROFILE_META_REPO_1 = _('Introduzca el espejo del repositorio a utilizar:')
PROFILE_META_REPO_2 = _('Puede utilizar el espejo del repositorio de la Metadistribución que más le convenga. Se recomienda la utilización de un espejo local para mayor rapidez. Si no está seguro, deje el valor por defecto.')
PROFILE_META_REPOSECTIONS_1 = _('Seleccione las secciones que estarán disponibles:')
PROFILE_META_REPOSECTIONS_2 = _('Cada Metadistribución tiene secciones del repositorio particulares. Seleccione segun su conveniencia.')
PROFILE_OS_LOCALE_1 = _('Seleccione el idioma predeterminado del Sistema Operativo:')
PROFILE_OS_LOCALE_2 = _('Debe seleccionar de la lista el idioma que vendrá configurado en la imagen resultante.')
PROFILE_OS_PACKAGES_1 = _('Introduzca los paquetes que conformarán el Sistema Operativo:')
PROFILE_OS_PACKAGES_2 = _('')
PROFILE_OS_PACKAGES_NAME = _('Paquetes')
PROFILE_OS_EXTRAREPOS_2 = _('Los repositorios adicionales permiten agregar software no oficial o desarrollado localmente a la imagen en construcción. Introduzca la dirección web, la rama y las secciones (separadas por espacios) correspondientes al repositorio.')
PROFILE_OS_EXTRAREPOS_CHECK = _('Deseo incluir repositorios adicionales')
PROFILE_OS_EXTRAREPOS_URL = _('Dirección URL del Repositorio')
PROFILE_OS_EXTRAREPOS_BRANCH = _('Rama')
PROFILE_OS_EXTRAREPOS_SECTIONS = _('Secciones')
PROFILE_OS_EXTRAREPOS_VALIDATE = _('Validación')
PROFILE_OS_EXTRAREPOS_VALIDATE_URL = _('Validando arquitectura "%s" de la rama "%s" ...')
PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR = _('La dirección web introducida es inválida')
PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE = _('ERROR')
PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_INCOMPLETE = _('Ocurrió un error durante la descarga de los componentes')
PROFILE_OS_EXTRAREPOS_UPDATE_DB = _('Ocurrió un error durante la descarga de los componentes')
PROFILE_OS_INCLUDES_1 = _('')
PROFILE_OS_INCLUDES_2 = _('')
PROFILE_OS_HOOKS_1 = _('')
PROFILE_OS_HOOKS_2 = _('')
PROFILE_IMG_SYSLINUX_SPLASH_1 = _('')
PROFILE_IMG_SYSLINUX_SPLASH_2 = _('')
PROFILE_IMG_POOL_PACKAGES_1 = _('')
PROFILE_IMG_POOL_PACKAGES_2 = _('')
PROFILE_IMG_INCLUDES_1 = _('')
PROFILE_IMG_INCLUDES_2 = _('')
PROFILE_IMG_HOOKS_1 = _('')
PROFILE_IMG_HOOKS_2 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_1 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_2 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_BANNER_1 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_BANNER_2 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_1 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_2 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_GTK_1 = _('')
PROFILE_IMG_DEBIAN_INSTALLER_GTK_2 = _('')


ProfileExists = _('El nombre escogido para la distribución derivada ya está siendo utilizado por otro perfil.')




