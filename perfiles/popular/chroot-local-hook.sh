#!/bin/bash -e

apt-get clean
apt-get autoclean

[ -e /var/cache/apt/pkgcache.bin ] && rm -rf /var/cache/apt/pkgcache.bin
[ -e /var/cache/apt/srcpkgcache.bin ] && rm -rf /var/cache/apt/srcpkgcache.bin

rm -rf /var/lib/apt/lists/repositorio*
rm -rf /var/lib/apt/lists/seguridad*
rm -rf /var/lib/apt/lists/universo*


