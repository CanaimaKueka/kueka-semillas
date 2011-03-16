===================
**CANAIMA-SEMILLA**
===================

-------------------------------------------------------------------------------------
Herramienta para facilitar la creación de distribuciones basadas en Canaima GNU/Linux
-------------------------------------------------------------------------------------

:Author: Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
:Date:   2011-03-10
:Copyright: Libre uso, modificación y distribución (GPL3)
:Version: 2.0+0
:Manual section: 1
:Manual group: Desarrollo

**MODO DE USO**
===============

::

	canaima-semilla [AYUDANTE] [PARÁMETRO-1] [PARÁMETRO-2] ... [PARÁMETRO-N] [--ayuda]

**DESCRIPCIÓN**
===============



**AYUDANTES DE CANAIMA SEMILLA**
================================

* Construir
* Instalar (En desarrollo)


**CONSTRUIR**
=============

Crea una imagen instalable (ISO o IMG) basado en los perfiles de sabores existentes. Puede especificársele el tipo de Medio, la arquitectura a construir, y el sabor. Las imágenes resultantes del proceso de construcción se guardan en el directorio /usr/share/canaima-semilla/semillero/.

USO
---

::

	canaima-semilla construir --medio="iso|usb" --arquitectura="i386|amd64" --sabor="institucional|popular|primera-base|sabor1|sabor2" [--ayuda]

PARÁMETROS
----------

``--medio``
	Tipo de imagen que será generada. Coloca "iso" para una imagen ISO grabable en CD/DVD o "usb" para una imagen IMG grabable en dispositivos USB.

``--arquitectura``
	Arquitectura soportada por la imagen resultante. Canaima GNU/Linux soporta i386 y amd64.

``--sabor``
	Sabor Canaima contenido en la imagen instalable. Debe estar definida en el directorio de los perfiles para poder funcionar.

``--ayuda``
	Muestra la documentación para el ayudante.
