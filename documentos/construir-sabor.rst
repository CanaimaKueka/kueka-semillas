=====================================
Cómo construir un nuevo Sabor Canaima
=====================================

Canaima Semilla facilita la creación de Sabores Canaima mediante el establecimiento de reglas o perfiles que definen los componentes que integran el sabor.
Un perfil está compuesto de varios archivos con nombres específicos colocados dentro de una carpeta que lleve por nombre el nombre del sabor en minúsculas . La carpeta contendrá:

1.- (Obligatorio) Un archivo llamado "sabor.conf" con las siguientes variables y sus valores:

	- "PUBLICADO_POR": Individuo o colectivo que publica la imagen.
		Ejemplo: PUBLICADO_POR="Canaima GNU/Linux; http://canaima.softwarelibre.gob.ve/; desarrolladores@canaima.softwarelibre.gob.ve"

	- "SABOR_DIST": Distribución Debian en la que se basa el sabor.
		Ejemplo: SABOR_DIST="squeeze"

	- "APLICACION": Nombre de la Metadistribución.
		Ejemplo: APLICACION="Canaima GNU/Linux"

	- "MIRROR_DEBIAN": Mirror de Debian desde donde se extraerán los paquetes que contendrá la la imagen. Los repositorios extra se definen en los archivos \*.binary y \*.chroot definidos más adelante. Se pueden especificar mirrors locales o remotos.
		Ejemplo: MIRROR_DEBIAN="http://universo.canaima.softwarelibre.gob.ve/"

	- "COMP_MIRROR_DEBIAN": Componentes del MIRROR_DEBIAN a estar disponibles para la construcción de la imagen.
		Ejemplo: COMP_MIRROR_DEBIAN="main contrib non-free"

	- "SABOR_PAQUETES": Lista de paquetes disponibles en MIRROR_DEBIAN o en alguna lista de repositorios extra.
		Ejemplo: SABOR_PAQUETES="canaima-base canaima-instalador-vivo canaima-blobs"

2.- (Opcional) Una imagen PNG llamada "syslinux.png" de una dimensión no mayor a 1024x768 pixeles, la cuál servirá de fondo en el menú de inicio del Medio Vivo.

.. image:: _static/syslinux.png
   :width: 640 px

3.- (Opcional) Una imagen PNG llamada "banner-instalador.png" de una dimensión exacta de 800x75 pixeles, la cuál será el banner del dialogo del instalador del Medio Vivo.

.. image:: _static/instalador.png
   :width: 800 px

4.- (Opcional) Un archivo de configuración GTKRC llamado "gtkrc-instalador", el cuál albergará los parámetros GTK para modificar la apariencia del instalador. Ver el sabor de

5.- (Opcional) Un par de archivos para definir repositorios extra en la etapa de instalación de paquetes finales (BINARY):

	- Uno de extensión \*.binary (pudiendo tener cualquier nombre), que contenga una lista de repositorios extra necesarios para la instalación de paquetes no incluídos en MIRROR_DEBIAN y especificados en SABOR_PAQUETES.
		Ejemplo: canaima.binary
			deb http://repositorio.canaima.softwarelibre.gob.ve/ pruebas usuarios
			deb http://seguridad.canaima.softwarelibre.gob.ve/ seguridad usuarios

	- Otro de extensión \*.binary.gpg, conteniendo la (o las) llave(s) GPG válida(s) correspondientes a los repositorios listados en el archivo \*.binary.

6.- (Opcional) Un par de archivos para definir repositorios extra en la etapa de instalación del sistema base inicial (CHROOT):

	- Uno de extensión \*.chroot (pudiendo tener cualquier nombre), que contenga una lista de repositorios extra necesarios para la instalación de paquetes no incluídos en MIRROR_DEBIAN y especificados en SABOR_PAQUETES.
		Ejemplo: canaima.chroot
			deb http://repositorio.canaima.softwarelibre.gob.ve/ pruebas usuarios
			deb http://seguridad.canaima.softwarelibre.gob.ve/ seguridad usuarios

	- Otro de extensión \*.chroot.gpg (con nombre igual al anterior), conteniendo la (o las) llave(s) GPG válida(s) correspondientes a los repositorios listados en el archivo \*.chroot.


Se provee en la dirección de los perfiles (/usr/share/canaima-semilla/perfiles) un perfil de ejemplo, el cuál podrá ser utilizado como base para nuevos sabores. La ausencia de alguno de los archivos Opcionales causará que Canaima Semilla use los valores por defecto (Debian).


Los perfiles se definen en la carpeta "/usr/share/canaima-semilla/perfiles", para la cual debes tener permisos de superusuario si deseas editarla. La mejor forma de crear un nuevo sabor, es duplicar la carpeta de ejemplo y comenzar a editar sus archivos hasta obtener el resultado esperado.

**SUGERENCIAS**
===============

- Optimizar la estructura de paquetes del sabor a construir. Lo ideal es que los paquetes se encuentren organizados y agrupados en metapaquetes, de forma tal de que con incluir unos pocos paquetes en SABOR_PAQUETES, todo el árbol de dependencias sea incluído.

- No utilizar scripts de postinstlación. Toda configuración adcional que se desee realizar al medio vivo, debe ser incorporado en paquetes detro de su respectivo postinst.

