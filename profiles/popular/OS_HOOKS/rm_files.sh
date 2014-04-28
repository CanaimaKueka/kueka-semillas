# PACKAGE: rm_file.sh
# FILE: rm_file.sh
# DESCRIPTION: hook para borrar archivos de la ISO canaima.
# COPYRIGHT:
# (C) 2013 Francisco Javier Vasquez Guerrero <franjvasquezg@gmail.com>
# LICENCE: GPL3
# ====================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY


rm -rf /var/cache/apt-xapian-index/*
rm -rf /var/cache/apt/pkgcache.bin
rm -rf /var/cache/apt/srcpkgcache.bin
rm -rf /var/lib/apt/lists/paquetes*
rm -rf /usr/share/doc/*   
