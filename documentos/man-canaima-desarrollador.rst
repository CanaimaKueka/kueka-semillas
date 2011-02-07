=========================
**CANAIMA-DESARROLLADOR**
=========================

----------------------------------------------------------------------------
Un conjunto de herramientas para la eliminación de las barreras tecnológicas
----------------------------------------------------------------------------

:Author: Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
:Date:   2011-01-22
:Copyright: Libre uso, modificación y distribución (GPL3)
:Version: 1.0+0
:Manual section: 1
:Manual group: Empaquetamiento

**MODO DE USO**
===============

::

	canaima-desarrollador [AYUDANTE] [PARÁMETRO-1] [PARÁMETRO-2] ... [PARÁMETRO-N] [--ayuda]

**DESCRIPCIÓN**
===============

Canaima Desarrollador (C-D) es un compendio de herramientas y ayudantes que facilitan el proceso de desarrollo de software para Canaima GNU/Linux. Está diseñado para **facilitar el trabajo** a aquellas personas que participan en dicho proceso con regularidad, como también para **iniciar a los que deseen aprender** de una manera rápida y práctica.

C-D puede ayudarte a:

* Agilizar los procesos para la creación de paquetes binarios canaima a partir de paquetes fuentes correctamente estructurados.
* Automatización personalizada de la creación de Paquetes Fuentes acordes a las Políticas de Canaima GNU/Linux.
* Creación de un depósito personal, por usuario, donde se guardan automáticamente y en carpetas separadas los siguientes tipos de archivo:

  - Proyectos en proceso de empaquetamiento
  - Paquetes Binarios (\*.deb)
  - Paquetes Fuente (\*.tar.gz, \*.dsc, \*.changes, \*.diff)
  - Registros provenientes de la creación de paquetes binarios (\*.build)

* Versionamiento asistido (basado en git) en los proyectos, brindando herramientas para realizar las siguientes operaciones, con un alto nivel de automatización y detección de posibles errores:

  - git clone
  - git commit
  - git push
  - git pull

* Ejecución de tareas en masa (empaquetar, hacer pull, push, commit, entre otros), para agilizar procesos repetitivos.


**AYUDANTES DE CANAIMA DESARROLLADOR**
======================================

* Crear Proyecto / Debianizar
* Crear Fuente
* Empaquetar
* Descargar
* Registrar
* Enviar
* Actualizar
* Descargar Todo
* Registrar Todo
* Enviar Todo
* Actualizar Todo
* Empaquetar Varios
* Empaquetar Todo
* Listar Remotos
* Listar Locales

**CREAR PROYECTO / DEBIANIZAR**
===============================

Crea un proyecto de empaquetamiento desde cero o debianiza uno existente.

USO
---

::

	canaima-desarrollador crear-proyecto|debianizar NOMBRE VERSIÓN DESTINO LICENCIA [--ayuda]

PARÁMETROS
----------

``NOMBRE``
	Un nombre para tu proyecto, que puede contener letras, números, puntos y guiones. Cualquier otro caracter no está permitido.

``VERSIÓN``
	La versión inicial de tu proyecto. Se permiten números, guiones, puntos, letras o dashes (~).

``DESTINO``
	Especifica si es un proyecto de empaquetamiento para Canaima GNU/Linux o si es un proyecto personal. Las opciones disponibles son "canaima" y "personal".

``LICENCIA``
	Especifica el tipo de licencia bajo el cuál distribuirás tu trabajo. Las licencias soportadas son: apache, artistic, bsd, gpl, gpl2, gpl3, lgpl, lgpl2 y lgpl3.

``--ayuda``
	Muestra la documentación para el ayudante.

Si estás debianizando un proyecto existente, lo que ingreses en NOMBRE y VERSIÓN se utilizará para determinar cuál es el nombre de la carpeta a debianizar dentro del directorio del desarrollador, suponiendo que tiene el nombre NOMBRE-VERSIÓN. Si no se llama así, habrá un error.

**CREAR FUENTE**
================

Crea un paquete fuente a partir de un proyecto de empaquetamiento existente. El resultado es guardado en el depósito de fuentes.

USO
---

::

	canaima-desarrollador crear-fuente DIRECTORIO [--ayuda]

PARÁMETROS
----------

``DIRECTORIO``
	Nombre del directorio dentro de la carpeta del desarrollador donde se encuentra el proyecto. El directorio debe contener un proyecto debianizado.

``--ayuda``
	Muestra la documentación para el ayudante.

**EMPAQUETAR**
==============

Éste ayudante te permite empaquetar un proyecto de forma automatizada, siguiendo la metodología git-buildpackage, que se centra en el siguiente diagrama:

**COMMIT > REFLEJAR CAMBIOS EN EL CHANGELOG > COMMIT > CREAR PAQUETE FUENTE > PUSH > GIT-BUILDPACKAGE**

USO
---

::

	canaima-desarrollador empaquetar DIRECTORIO MENSAJE PROCESADORES [--ayuda]

PARÁMETROS
----------

``DIRECTORIO``
	Nombre de la carpeta dentro del directorio del desarrollador donde se encuentra el proyecto a empaquetar.

``MENSAJE``
	Mensaje representativo de los cambios para el primer commit. El segundo commit es sólo para el changelog. Colocando la palabra "auto" o dejando el campo vacío, se autogenera el mensaje.

``PROCESADORES``
	Número de procesadores con que cuenta tu computadora para optimizar el proceso de empaquetamiento.

``--ayuda``
	Muestra la documentación para el ayudante.


**DESCARGAR**
=============

Éste ayudante te permite copiar a tu disco duro un proyecto que se encuentre en el repositorio remoto para que puedas modificarlo según consideres. Utiliza git clone para realizar tal operación. Éste ayudante se encarga además de realizar las siguientes operaciones por ti:

  - Verifica e informa sobre el éxito de la descarga.
  
USO
---

::

	canaima-desarrollador descargar PROYECTO [--ayuda]

PARÁMETROS
----------

``PROYECTO``
	Nombre del proyecto (en caso de que éste se encuentre en el repositorio de Canaima GNU/Linux) o la dirección git pública del proyecto.

``--ayuda``
	Muestra la documentación para el ayudante.

**REGISTRAR**
=============

Éste ayudante te permite registar (o hacer commit de) los cambios hechos en un proyecto mediante el versionamiento basado en git. Utiliza git commit para lograr éste propósito. Éste ayudante se encarga además de realizar las siguientes operaciones por ti:

  - Verifica la existencia de la rama git "upstream". En caso de no encontrarla, la crea.
  - Verifica la existencia de la rama git "master". En caso de no encontrarla, la crea.
  - Verifica la existencia de todos los elementos necesarios para ejecutar la acción git commit (carpetas, variables de entorno, etc..). En caso de encontrar algún error, aborta e informa.
  - Autogenera el mensaje de commit, si se le instruye.
  - Hace git checkout a la rama master, si nos encontramos en una rama diferente a la hora de hace commit.
  - Hace un git merge de la rama master a la upstream, inmediatamente depués del commit.
  
USO
---

::

	canaima-desarrollador registrar DIRECTORIO MENSAJE [--ayuda]

PARÁMETROS
----------

``DIRECTORIO``
	Nombre de la carpeta dentro del directorio del desarrollador a la que se quiere hacer commit.

``MENSAJE``
	Mensaje representativo de los cambios para el commit. Colocando la palabra "auto" o dejando el campo vacío, se autogenera el mensaje.

``--ayuda``
	Muestra la documentación para el ayudante.

**ENVIAR**
==========

Éste ayudante te permite enviar los cambios realizados al repositorio remoto especificado en las configuraciones personales, mediante el uso de la acción git push. Éste ayudante se encarga además de realizar las siguientes operaciones por ti:

  - Verifica la existencia de la rama git "upstream". En caso de no encontrarla, la crea.
  - Verifica la existencia de la rama git "master". En caso de no encontrarla, la crea.
  - Verifica la existencia de todos los elementos necesarios para ejecutar la acción git push (carpetas, variables de entorno, etc..). En caso de encontrar algún error, aborta e informa.
  - Configura el repositorio remoto para el proyecto, de acuerdo a los parámetros establecidos en ~/.config/canaima-desarrollador/usuario.conf

USO
---

::

	canaima-desarrollador enviar DIRECTORIO [--ayuda]

PARÁMETROS
----------

``DIRECTORIO``
	Nombre de la carpeta dentro del directorio del desarrollador a la que se quiere hacer push.

``--ayuda``
	Muestra la documentación para el ayudante.

**ACTUALIZAR**
==============

Éste ayudante te permite actualizar el código fuente de un determinado proyecto, mediante la ejecución de "git pull" en la carpeta del proyecto. Éste ayudante se encarga además de realizar las siguientes operaciones por ti:

  - Verifica la existencia de la rama git "upstream". En caso de no encontrarla, la crea.
  - Verifica la existencia de la rama git "master". En caso de no encontrarla, la crea.
  - Verifica la existencia de todos los elementos necesarios para ejecutar la acción git pull (carpetas, variables de entorno, etc..). En caso de encontrar algún error, aborta e informa.
  - Configura el repositorio remoto para el proyecto, de acuerdo a los parámetros establecidos en ~/.config/canaima-desarrollador/usuario.conf

USO
---

::

	canaima-desarrollador actualizar DIRECTORIO [--ayuda]

PARÁMETROS
----------

``DIRECTORIO``
	Nombre de la carpeta dentro del directorio del desarrollador a la que se quiere hacer git pull.

``--ayuda``
	Muestra la documentación para el ayudante.

**DESCARGAR TODO**
==================

Éste ayudante te permite copiar a tu disco duro todos los proyectos de Canaima GNU/Linux que se encuentren en el repositorio remoto oficial. Utiliza git clone para realizar tal operación.

USO
---

::

	canaima-desarrollador descargar-todo [--ayuda]

PARÁMETROS
----------

``--ayuda``
	Muestra la documentación para el ayudante.

**REGISTRAR TODO**
==================

Éste ayudante te permite registar (o hacer commit de) todos los cambios hechos en todos los proyectos existentes en la carpeta del desarrollador. Utiliza git commit para lograr éste propósito. Asume un mensaje de commit automático para todos.

USO
---

::

	canaima-desarrollador registrar-todo [--ayuda]

PARÁMETROS
----------

``--ayuda``
	Muestra la documentación para el ayudante.

**ENVIAR TODO**
===============

Éste ayudante te permite enviar todos los cambios realizados en todos los proyectos ubicados en la carpeta del desarrollador al repositorio remoto especificado en las configuraciones personales, mediante el uso de la acción git push.

USO
---

::

	canaima-desarrollador enviar-todo [--ayuda]

PARÁMETROS
----------

``--ayuda``
	Muestra la documentación para el ayudante.

**ACTUALIZAR TODO**
===================

Éste ayudante te permite actualizar el código fuente de todos los proyectos ubicados en la carpeta del desarrollador, mediante la ejecución de "git pull" en la carpeta del proyecto.

USO
---

::

	canaima-desarrollador actualizar-todo [--ayuda]

PARÁMETROS
----------

``--ayuda``
	Muestra la documentación para el ayudante.

**EMPAQUETAR VARIOS**
=====================

Éste ayudante te permite empaquetar varios proyectos.

USO
---

::

	canaima-desarrollador empaquetar-varios PARA-EMPAQUETAR PROCESADORES [--ayuda]

PARÁMETROS
----------

``PARA-EMPAQUETAR``
	Lista de los directorios dentro de la carpeta del desarrollador que contienen los proyectos que se quieren empaquetar, agrupados entre comillas.

``PROCESADORES``
	Número de procesadores con que cuenta tu computadora para optimizar el proceso de empaquetamiento.

``--ayuda``
	Muestra la documentación para el ayudante.

**EMPAQUETAR TODO**
===================

Éste ayudante te permite empaquetar todos los proyectos existentes en la carpeta del desarrollador.

USO
---

::

	canaima-desarrollador empaquetar-todo PROCESADORES [--ayuda]

PARÁMETROS
----------

``PROCESADORES``
	Número de procesadores con que cuenta tu computadora para optimizar el proceso de empaquetamiento.

``--ayuda``
	Muestra la documentación para el ayudante.

**LISTAR REMOTOS**
==================

Muestra todos los proyectos contenidos en el repositorio remoto y muestra su dirección git.

USO
---

::

	canaima-desarrollador listar-remotos [--ayuda]

PARÁMETROS
----------

``--ayuda``
	Muestra la documentación para el ayudante.

**LISTAR LOCALES**
==================

Muestra todos los proyectos contenidos en la carpeta del desarrollador y los clasifica según su tipo.

USO
---

::

	canaima-desarrollador listar-locales [--ayuda]

PARÁMETROS
----------

``--ayuda``
	Muestra la documentación para el ayudante.
