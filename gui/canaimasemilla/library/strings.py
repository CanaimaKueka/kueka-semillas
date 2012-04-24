#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import gettext as _

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

