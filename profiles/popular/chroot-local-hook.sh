#!/bin/bash -e

apt-get clean
apt-get autoclean

[ -e /var/cache/apt/pkgcache.bin ] && rm -rf /var/cache/apt/pkgcache.bin
[ -e /var/cache/apt/srcpkgcache.bin ] && rm -rf /var/cache/apt/srcpkgcache.bin

rm -rf /var/lib/apt/lists/repositorio*
rm -rf /var/lib/apt/lists/seguridad*
rm -rf /var/lib/apt/lists/universo*

[ -e /usr/share/icons/gnome/icon-theme.cache ] && rm -rf /usr/share/icons/gnome/icon-theme.cache
[ -e /usr/share/icons/canaima-iconos/icon-theme.cache ] && rm -rf /usr/share/icons/canaima-iconos/icon-theme.cache


