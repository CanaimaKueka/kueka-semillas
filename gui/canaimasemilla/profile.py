#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import re
import os
import threading
from subprocess import Popen, PIPE, STDOUT

import config
import main
import paso2

#---Hilo Principal----#
gtk.gdk.threads_init()

class Paso1():
	
	def __init__(self):
		
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_title('Crear Nuevo Sabor')
		self.window.set_size_request(600, 600)
		self.window.set_resizable(False)
		self.window.connect("destroy", gtk.main_quit)
		self.window.set_icon_from_file('/usr/share/icons/canaima-iconos/apps/48/c-s.png')
		
		#------------------Empaquetado de cajas------------------#
		self.box1 = gtk.VBox(False, 0)
		
		self.box2 = self.make_imag1(False, 0, False, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_label1(False, 0, False, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.separator = gtk.HSeparator()
		self.box1.pack_start(self.separator, False, True,5)
		self.separator.show()
		
		self.box2 = self.make_label2(False, 0, False, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box1(False, 0, True, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box2(False, 0, True, False, 0)
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
		boton_cerrar.set_size_request(80, 30)
		boton_cerrar.connect("clicked", gtk.main_quit)
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
		boton_atras = gtk.Button("<Atras")
		
		def hilo_atras(self):
			hilo = threading.Thread(target=atras, args=(self))
			hilo.start()
		
		def atras(self):
			main.CanaimaSemilla()
			self.window.hide()
		
		boton_atras.set_size_request(80, 30)
		boton_atras.connect("clicked", hilo_atras)
		caja.pack_start(boton_atras, False, False, 10)
		boton_atras.show()
		
		#--------------------Sigueinte ventana------------------------	
		global boton_siguiente
		boton_siguiente = gtk.Button("Siguiente>")
		
		def hilo_crear_carpeta (self):
			hilo = threading.Thread(target=crear_carpeta, args=(self))
			hilo.start()	
	
		#-------------------------- condicion crear carperta------------------------------------
		def crear_carpeta(self):
			
			def prueba_inter(self):
				pru = os.system("wget http://www.google.co.ve/")
				t = next(os.walk('/usr/share/canaima-semilla-gui/scripts/'))[2]
				a = 'index.html'
				b = ''
				for b in t:
					if b == a:					
						borrar = os.system('rm /usr/share/canaima-semilla-gui/scripts/index.html')
						return True
					else:
						pass
					
			if prueba_inter(self) == True:
				
				boton_siguiente.set_sensitive(False)
				boton_atras.set_sensitive(False)
		
				gtk.gdk.threads_enter()
				pregunta=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="¿Desea crear la carpeta para continuar con la construcción del sabor?")
				pregunta.set_title('Crear Carpeta')
				respuesta = pregunta.run()
				pregunta.destroy()
				gtk.gdk.threads_leave()
			
				if respuesta == gtk.RESPONSE_YES:
					config.ruta = os.path.join(config.ruta, '/usr')
					config.ruta = os.path.join(config.ruta, 'share')
					config.ruta = os.path.join(config.ruta, 'canaima-semilla')
					config.ruta = os.path.join(config.ruta, 'perfiles')
					config.ruta = os.path.join(config.ruta, nombre_carpeta.get_text())
													
					if os.path.exists(config.ruta):
						gtk.gdk.threads_enter()
						md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tLa carpeta que desea crear ya existe con ese Nombre\t")
						md.run()
						md.destroy()
						gtk.gdk.threads_leave()	
						
					else: 
						os.makedirs(config.ruta)
						gtk.gdk.threads_enter()
						md=gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK, message_format="La carpeta ha sido creada con éxito en la dirección:\n"+config.ruta+"\n")
						md.run()
						md.destroy()
						gtk.gdk.threads_leave()
					
						#construir_iso.actualizar_lista(self)
						gtk.gdk.threads_enter()
						paso2.Paso2()
						self.window.hide()
						gtk.gdk.threads_leave()
						
				boton_siguiente.set_sensitive(True)
				boton_atras.set_sensitive(True)
						
			else:
				gtk.gdk.threads_enter()
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="FALLO LA CONEXIÓN A INTERNET:\n\nNo podrá crear el Nuevo Sabor debido a que se ejecutarán procesos que requieren una conexión a internet.")
				md.set_title('Error en Conexión')
				md.run()
				md.destroy()
				gtk.gdk.threads_leave()
		
		#boton_siguiente.set_sensitive(False)
		boton_siguiente.connect("clicked", hilo_crear_carpeta)
		boton_siguiente.set_size_request(85, 30)
		caja.pack_start(boton_siguiente, False, False, 0)
		boton_siguiente.show()
		return caja
		#------------------------------------------------------------
	
	
	def make_label1(self, homogeneous, spacing, expand, fill, padding):
		
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
			
		separator = gtk.HSeparator()
		caja.pack_start(separator, False, False,40)
		separator.show()
		
		image = gtk.Image()
		image.set_from_file('/usr/share/canaima-semilla-gui/images/distri.png')
		caja.pack_start(image, False, False,5)
		image.show()
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\n<b>CONSTRUCCIÓN DE NUEVOS SABORES CANAIMA</b>")
		caja.pack_start(descripcion, False, False,5)
		descripcion.show()
		return caja	
	
	def make_label2(self, homogeneous, spacing, expand, fill, padding):
		
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
			
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\nCanaima Semilla facilita la creación de Sabores Canaima mediante el \n"
								+"establecimiento de reglas o  perfiles que  definen  los componentes\n"
								+"que integran el sabor. Un perfil está compuesto de varios archivos con\n"
								+"nombres específicos colocados dentro de una carpeta.\n\n"
								+"Para comenzar con la construcción del nuevo sabor debe seguir\n"
								+"los pasos que a continuación se presentan:\n\n\n"
								+"<b>Paso 1. Cree la carpeta:\n\n</b>"
								+"Debe especificarle un nombre a la carpeta, el cual será el de su nuevo sabor\n\n")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,25)
		descripcion.show()
		return caja	
	
	#-----------------------------solo introducir minusculas y ' - '------------------------------------		
	def on_insert_text(self, editable, new_text, new_text_length, position):
		
		solominusculas = re.compile('^[a-z-]*$')
		if solominusculas.match(new_text) is None:
			editable.stop_emission('insert-text')
			
			
	def espacios(self, homogeneous, spacing, expand, fill, padding):
		
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
		
		etiqueta_vacia = gtk.Label("\n")
		caja.pack_start(etiqueta_vacia, False, False, 5)
		etiqueta_vacia.show()
		
		return caja
	
	def make_box1(self, homogeneous, spacing, expand, fill, padding):
   
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
	
		#-------------------------------etiqueta------------------------------------------------------					
		etiqueta = gtk.Label("Introduzca el Nombre:")
		etiqueta.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(etiqueta, True, False, 30)
		etiqueta.show()
		
		return caja
			
	def make_box2(self, homogeneous, spacing, expand, fill, padding):
   
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
		
		global nombre_carpeta
		nombre_carpeta = gtk.Entry()
		nombre_carpeta.connect('insert-text', self.on_insert_text)
		nombre_carpeta.set_max_length(18)#cantidad de caracteres
		nombre_carpeta.set_text("nombre-del-sabor")#comentario dentro del entry
		nombre_carpeta.set_sensitive(True) #permite la edicion del campo de texto
		nombre_carpeta.set_editable(True)#nombre_carpeta editable o no
		nombre_carpeta.set_visibility(True)#texto visible
		#nombre_carpeta.connect("activate", self.hilo_crear_carpeta)#conectar nombre_carpeta con funcion
		caja.pack_start(nombre_carpeta, True, True, 180)
		nombre_carpeta.show()

		return caja
		
if __name__ == "__main__":
	app = Paso1()
	gtk.main()
