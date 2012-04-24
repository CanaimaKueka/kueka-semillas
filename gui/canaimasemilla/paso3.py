#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----Librerias-----#
import os
import re
import gtk
import urllib
import threading
from subprocess import Popen, PIPE, STDOUT

import config
import paso2, paso4

#---Hilo Principal----#
gtk.gdk.threads_init()

class Paso3():
	
	def __init__(self):
		
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_title('Crear Nuevo Sabor:')
		self.window.set_size_request(600, 600)
		self.window.set_resizable(False)
		self.window.connect("delete_event", self.on_delete)
		self.window.connect("destroy", gtk.main_quit)
#	self.window.set_icon_from_file('/usr/share/icons/canaima-iconos/apps/48/c-s.png')
		
		#------------------Empaquetado de cajas------------------#
		self.box1 = gtk.VBox(False, 0)
		
		self.box2 = self.make_imag1(False, 0, False, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.etiqueta1(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja1(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		separator = gtk.HSeparator()
		self.box1.pack_start(separator, False, True, 2)
		separator.show()
		
		self.box2 = self.etiqueta2(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja2(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja3(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja_buffer(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.espacios(False, 0, True, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.separator = gtk.HSeparator()
		self.box1.pack_start(self.separator, False, False, 0)
		self.separator.show()
		
		self.box2 = self.make_botones(False, 0, True, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
	
		self.box1.show()
		self.window.add(self.box1)
		self.window.show_all()
		
	def close(self):
		md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Al cerrar, todos los procedimientos que ha realizado serán eliminados.\n ¿Desea salir de la aplicación?")
		md.set_title('Cerrar')
		respuesta = md.run()
		md.destroy()
		
		if respuesta == gtk.RESPONSE_YES:
			os.system('rm -r '+config.ruta)
			self.window.destroy()
			gtk.main_quit()
	
	def on_delete(self, widget, data=None):
		return not self.close()
	

	def make_imag1(self, homogeneous, spacing, expand, fill, padding):
	
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(0)
	
		image = gtk.Image()
		image.set_from_file('/usr/share/canaima-semilla-gui/images/banner.png')
		caja.pack_start(image, False, False,0)
		image.show()
		
		return caja
	
	def make_botones(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
		
		#--------------------------Cerrar--------------------------	
		boton_cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
		
		def hilo_cerrar(self):
			hilo = threading.Thread(target=cerrar, args=(self))
			hilo.start()
		
		def cerrar(self):
			gtk.gdk.threads_enter()
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Al cerrar, todos los procedimientos que ha realizado serán eliminados.\n ¿Desea salir de la aplicación?")
			md.set_title('Cerrar')
			respuesta = md.run()
			md.destroy()
			gtk.gdk.threads_leave()
		
			if respuesta == gtk.RESPONSE_YES:
				os.system('rm -r '+config.ruta)
				self.window.destroy()
				gtk.main_quit()
		
		boton_cerrar.set_size_request(80, 30)
		boton_cerrar.connect("clicked", hilo_cerrar)
		caja.pack_start(boton_cerrar, False, False, 5)
		boton_cerrar.show()
		#----------------------------------------------------------
		
		#-----------------------ayuda--------------------------
		boton_ayuda = gtk.Button("Ayuda")
		def clic_ayuda(self):
			hilo = threading.Thread(target=ayuda_1, args=(self))
			hilo.start()
		
		def ayuda_1(self, widget=None):			
			x= Popen(["yelp /usr/share/gnome/help/canaima-semilla-gui/es/c-s.xml"], shell=True, stdout=PIPE)
		
		boton_ayuda.connect("clicked", clic_ayuda)
		boton_ayuda.set_size_request(80, 30)
		caja.pack_start(boton_ayuda, False, False, 5)
		boton_ayuda.show()
		#--------------------------------------------------------
		separator = gtk.HSeparator()
		caja.pack_start(separator, False, False,110)
		separator.show()
		#--------------------atras--------------------------------
		global boton_atras
		boton_atras = gtk.Button("<Atras")
		
		def hilo_atras(self):
			hilo = threading.Thread(target=atras, args=(self))
			hilo.start()
		
		def atras(self):
			gtk.gdk.threads_enter()
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Si regresa al paso anterior los cambios realizados al archivo \"sabor.config\" serán eliminados.\n ¿Desea regresar al paso anterior?")
			md.set_title('Cerrar')
			respuesta = md.run()
			md.destroy()
			gtk.gdk.threads_leave()
		
		
			if respuesta == gtk.RESPONSE_YES:
			
				gtk.gdk.threads_enter()
				os.system('rm '+config.ruta+"/sabor.conf")
				paso2.Paso2()
				self.window.hide()
				gtk.gdk.threads_leave()
		
		boton_atras.set_size_request(80, 30)
		boton_atras.connect("clicked", hilo_atras)
		caja.pack_start(boton_atras, False, False, 10)
		boton_atras.show()
		
		#--------------------Sigueinte ventana------------------------	
		global boton_siguiente
		boton_siguiente = gtk.Button("Siguiente>")
		
		#-------------Método para crear el hilo del método hacer lo cambios del archivo .binary-------------#					
		def hilo_hacer(self):
			hilo=threading.Thread(target = hacer, args=self)
			hilo.start()
					
		#~~~~~~~~~~~~~ Método para construir el archivo .binary ~~~~~~~~~~~~~~~~~~~~# 
		
		def hacer(self):
			
			boton_siguiente.set_sensitive(False)
			boton_atras.set_sensitive(False)
			boton.set_sensitive(False)
			
			if texto1.get_text() == "":
				gtk.gdk.threads_enter()
				error=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe especificar el nombre del archivo")
				error.run()
				error.destroy()
				gtk.gdk.threads_leave()
				
			else:
				if textbuffer.get_text(*textbuffer.get_bounds()) == "":
					gtk.gdk.threads_enter()
					errorURL=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe introducir la lista de repositorios llenando todos los campos y dando clic en \"Validar\"")
					errorURL.run()
					errorURL.destroy()
					gtk.gdk.threads_leave()
				
				
				else:
					gtk.gdk.threads_enter()
					f=open(config.ruta+"/"+texto1.get_text()+".binary","w")
					f.write(textbuffer.get_text(*textbuffer.get_bounds()))
					f.close()
					gtk.gdk.threads_leave()
				
					if os.path.exists(config.ruta):
						gtk.gdk.threads_enter()
						message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="Cambios aplicados con éxito en "+config.ruta)
						message.run()
						message.hide()
						gtk.gdk.threads_leave()
						
						gtk.gdk.threads_enter()
						paso4.Paso4()
						self.window.hide()
						gtk.gdk.threads_leave()
				
					else:
						gtk.gdk.threads_enter()
						md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe crear la carpeta con el nombre del nuevo sabor antes de continuar")
						md.run()
						md.destroy()
						gtk.gdk.threads_leave()
						
			boton_siguiente.set_sensitive(True)
			boton_atras.set_sensitive(True)
			boton.set_sensitive(True)
		
		boton_siguiente.connect("clicked", hilo_hacer)
		boton_siguiente.set_size_request(85, 30)
		caja.pack_start(boton_siguiente, False, False, 0)
		boton_siguiente.show()
		return caja
		#------------------------------------------------------------
	
	def espacios(self, homogeneous, spacing, expand, fill, padding):
		
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
		
		etiqueta_vacia = gtk.Label("")
		caja.pack_start(etiqueta_vacia, True, False,0)
		etiqueta_vacia.show()
		
		return caja
	
	def etiqueta1(self, homogeneous, spacing, expand, fill, padding):

		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
	
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\n\n<b>Paso 3. Cree un archivo .binary (con cualquier nombre) que contenga\nla lista de repositorios necesarios para la instalación\nde paquetes en su nueva distribución.\n\n</b>")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,20)
		descripcion.show()
		return caja
			
	def etiqueta2(self, homogeneous, spacing, expand, fill, padding):

		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)

		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("Configure el archivo \".binary\":\nDebe introducir direcciones validas para los repositorios y\nespecificar la Rama y la Sección para poder Validarlos.\n")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,10)
		descripcion.show()
		return caja
			
	def caja1(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
			
		etiqueta=gtk.Label("Nombre del archivo:  ")
		caja.pack_start(etiqueta, False, False, 10)
		etiqueta.show()
			
		global texto1
		texto1 = gtk.Entry()
		#texto1.connect("activate", hacer)
		caja.pack_start(texto1, True, True, 5)
		texto1.show()
		
		etiqueta2=gtk.Label(".binary")
		caja.pack_start(etiqueta2, False, False, 10)
		etiqueta2.show()

		return caja	
	
	
	
	def caja2(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(7)
			
		etiqueta=gtk.Label("Repositorio Remoto:")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global texto5
		texto5 = gtk.Entry()
		texto5.connect('insert-text', self.espacio)
		texto5.set_text("http://repositorio.canaima.softwarelibre.gob.ve/")
		caja.pack_start(texto5, True, True, 5)
		texto5.show()
		
		return caja
			
	
	def caja3(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(7)
			
		rama=gtk.Label("Rama:")
		caja.pack_start(rama, False, False, 5)
		rama.show()
			
		global texto2
		texto2 = gtk.Entry()
		texto2.set_text("pruebas")
		texto2.set_sensitive(True)
		caja.pack_start(texto2, True, True, 5)
		texto2.show()
		
		seccion=gtk.Label("Sección:")
		caja.pack_start(seccion, False, False, 5)
		seccion.show()
		
		global texto3
		texto3 = gtk.Entry()
		texto3.set_text("usuarios")
		texto3.set_sensitive(True)
		caja.pack_start(texto3, True, True, 5)
		texto3.show()
		
		global boton
		boton = gtk.Button("   Validar   ")
		
		#-------------Método para crear el hilo del método validar los repositorios-------------#					
		def hilo_validar_remotos(self):
			hilo=threading.Thread(target = validar_remotos, args=self)
			hilo.start()
				
		#~~~~~~~~ Método para validar los repositorios remotos ~~~~~~~~~#			
		def validar_remotos(self):
			
			boton.set_sensitive(False)
			boton_siguiente.set_sensitive(False)
			boton_atras.set_sensitive(False)
			
			if texto5.get_text() == "" or texto2.get_text() == "" or texto3.get_text() == "":
				gtk.gdk.threads_enter()
				error=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe tener todos los campos llenos para validar")
				error.run()
				error.destroy()
				gtk.gdk.threads_leave()
			else:
				try:
					urllib.urlopen(texto5.get_text())
					
					if textbuffer.get_text(*textbuffer.get_bounds()).find(texto5.get_text()) >= 0:
						gtk.gdk.threads_enter()
						message = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_CLOSE, message_format="La dirección ya ha sido agregada")
						message.run()
						message.hide()
						gtk.gdk.threads_leave()
					
					else:
						gtk.gdk.threads_enter()
						textbuffer.set_text(textbuffer.get_text(*textbuffer.get_bounds())+"deb "+texto5.get_text()+' '+texto2.get_text()+' '+texto3.get_text()+"\n")
						gtk.gdk.threads_leave()
					
				except IOError:
					gtk.gdk.threads_enter()
					errorURL=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe introducir URL validas para el repositorio")
					errorURL.run()
					errorURL.destroy()
					gtk.gdk.threads_leave()

			boton.set_sensitive(True)
			boton_siguiente.set_sensitive(True)
			boton_atras.set_sensitive(True)
			
		boton.connect("clicked", hilo_validar_remotos)
		caja.pack_start(boton, False, False, 5)
		boton.show()
					
		return caja
	
	def caja_buffer(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(7)
			
		scrolledwindow = gtk.ScrolledWindow()
		scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
   
		marco = gtk.Frame()
		alineacion = gtk.Alignment(xalign=0.5, yalign=0.1, xscale=0.98, yscale=0.5)
		
		global textview
		textview = gtk.TextView()
		global textbuffer
		textbuffer = textview.get_buffer()
   
		start, end = textbuffer.get_bounds()
		textview.set_wrap_mode(gtk.WRAP_WORD)
			
		textview.set_editable(False)
		scrolledwindow.add(textview)
		alineacion.add(scrolledwindow)
		marco.add(alineacion)
		caja.pack_start(marco, True, True, 5)
   
		textview.show()
		scrolledwindow.show()
		alineacion.show()
		marco.show()
			
		return caja
		
#-------------Método para no permitir espacios en el campo buscar paquetes-------------#			
	def espacio(self, editable, new_text, new_text_length, position):
		sin_espacios = re.compile('[!/*+=?|$%&@()a-zA-Z0-9-"_.]')
			
		if sin_espacios.match(new_text) is None:
			editable.stop_emission('insert-text')

					
	def siguiente(self, data=None):
		paso4.Paso4()
		self.window.hide()

if __name__ == "__main__":
	app = Paso3()
	gtk.main()
