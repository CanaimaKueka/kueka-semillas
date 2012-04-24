#!/bin/sh -e

INFOMSG "Nombre de la persona o grupo responsable del sabor (opcional)" "AUTHOR_NAME"

##-[es]-- Correo electrónico de la persona o grupo responsable del sabor (opcional)
AUTHOR_EMAIL=""

##-[es]-- Página Web de referencia para el sabor (opcional)
AUTHOR_URL=""

##-[es]-- Nombre de la Metadistribución en la que se basa el sabor (obligatorio) [canaima, debian, ubuntu]
META_DISTRO=""

##-[es]-- Nombre código de la versión de la Metadistribución (obligatorio)
META_CODENAME=""

##-[es]-- Repositorio asociado a la Metadistribución (obligatorio)
META_REPO=""

##-[es]-- Secciones del repositorio disponibles para la construcción de la imagen (obligatorio)
##-[en]-- Secciones del repositorio disponibles para la construcción de la imagen (obligatorio)
META_REPOSECTIONS=""

AUTHOR_NAME=""
AUTHOR_EMAIL=""
AUTHOR_URL=""

META_DISTRO=""
META_CODENAME=""
META_REPO=""
META_REPOSECTIONS=""

OS_LOCALE=""
OS_PACKAGES=""
OS_EXTRAREPOS=""
OS_INCLUDES=""
OS_HOOKS=""

IMG_SYSLINUX_SPLASH=""
IMG_POOL_PACKAGES=""
IMG_INCLUDES=""
IMG_HOOKS=""
IMG_DEBIAN_INSTALLER=""
IMG_DEBIAN_INSTALLER_BANNER=""
IMG_DEBIAN_INSTALLER_PRESEED=""
IMG_DEBIAN_INSTALLER_GTK=""
