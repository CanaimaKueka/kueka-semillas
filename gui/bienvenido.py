#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pygtk.require('2.0')
import construir_iso
import gtk
import threading
from subprocess import Popen, PIPE, STDOUT
import paso1

gtk.gdk.threads_init()

class bienvenido_1():
	
	def make_imag1(self, homogeneous, spacing, expand, fill, padding):
	
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(0)
	
		image = gtk.Image()
		image.set_from_file('/usr/share/canaima-semilla-gui/images/banner.png')
		caja.pack_start(image, False, False,0)
		image.show()
		return caja
	
	def make_label11(self, homogeneous, spacing, expand, fill, padding):
	
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(0)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(False)
		descripcion.set_markup("\n<b>Bienvenido a Canaima Semilla (c-s)</b>\n")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,0)
		descripcion.show()
		return caja
	
	def make_label1(self, homogeneous, spacing, expand, fill, padding):
	
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(0)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(False)
		descripcion.set_markup("\nCanaima Semilla  es un paquete diseñado para facilitar a individuales, \ncolectivos e instituciones la creación de distribuciones GNU/Linux \npersonalizadas y adaptadas a sus necesidades (lo que conocemos \ncomo sabores), partiendo de la Metadistribución Canaima GNU/Linux.\n\n\nLa herramienta permite crear imágenes instalables (ISO o IMG) basadas \nen los perfiles de sabores existentes y  construir nuevas \ndistribuciones Canaima GNU/linux conocidas como sabores.\n\n Seleccione alguna de las opciones:\n\n")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,0)
		descripcion.show()
		return caja
		
	def make_label2(self, homogeneous, spacing, expand, fill, padding):
	
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(1)
		
		caja2 = gtk.VBox(homogeneous, spacing)
		caja2.set_border_width(0)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(False)
		#descripcion.set_markup("\tUna imagen .iso o .img es un \n\tarchivo donde se almacena \n\tuna copia o imagen exacta de\n\t un sistema de ficheros. Grabables\n\t en dispositivos CD/DVD o USB.")
		descripcion.set_markup("<b>Crear ISO'S</b>\n\nUna imagen grabable en \ndispositivos  CD/DVD o USB, \nbasadas en los sabores existentes \nde Canaima GNU/Linux.")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, True,0)
		descripcion.show()
		
		#~ descripcion = gtk.Label()
		#~ descripcion.set_use_markup(False)
		#~ descripcion.set_markup("\tUna imagen .iso o .img es un \n\tarchivo donde se almacena \n\tuna copia o imagen exacta \n\tde un sistema de ficheros. Grabables\n\t en dispositivos CD/DVD ó USB.")
		#~ descripcion.set_justify(gtk.JUSTIFY_CENTER)
		#~ caja2.pack_start(descripcion, False, False,0)
		#~ descripcion.show()
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(False)
		#descripcion.set_markup("\t\tEs una distribución de Canaima \n\t\tGNU/Linux,personalizada mediante\n\t\tparámetros que permiten \n\t\tadaptarlo a sus necesidades \n\t\to de una institución.")
		descripcion.set_markup("<b>Construir Nuevo Sabor</b>\n\nEs una distribución de Canaima \nGNU/Linux,personalizada con\nparámetros que permiten \nadaptarlo a sus necesidades.")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, True,0)
		descripcion.show()
		
		caja.pack_start(caja2, False, False,0)

		#~ descripcion = gtk.Label()
		#~ descripcion.set_use_markup(False)
		#~ descripcion.set_markup("\t \t\t   Es una distribución de Canaima GNU/Linux,\n\t   \t\t\tpersonalizada mediantes parámetros\n\t\t   que permiten adaptarlo a sus necesidades\n\t\t\t\t\tó una institución.\n\t\t\tCD/DVD ó USB.\n")
		#~ caja.pack_start(descripcion, False, False,0)
		#~ descripcion.show()
		
		
		return caja
	
	def make_boton_check(self, homogeneous, spacing, expand, fill, padding):
	
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(0)
		
		separator = gtk.HSeparator()
		caja.pack_start(separator, False, False,25)
		separator.show()
		
		image = gtk.Image()
		image.set_from_file('/usr/share/canaima-semilla-gui/images/iso.png')
		caja.pack_start(image, False, False,10)
		image.show()
		
		def valor_iso(self, widget, data=None):
			if check1_constru_iso.get_active() == True:
				check2_nuevo_sabor.set_active(False)	
			else:
				check2_nuevo_sabor.set_active(True)
					
		def valor_const(self, widget, data=None):
			if check2_nuevo_sabor.get_active() == True:
				check1_constru_iso.set_active(False)
			else:
				check1_constru_iso.set_active(True)
		
		global check1_constru_iso
		check1_constru_iso = gtk.CheckButton("Crear IS0'S")
		check1_constru_iso.connect("toggled", valor_iso,"uno")
		caja.pack_start(check1_constru_iso, False, False, 5)
		check1_constru_iso.show()
		
		separator = gtk.HSeparator()
		caja.pack_start(separator, False, False,60)
		separator.show()
		
		image = gtk.Image()
		image.set_from_file('/usr/share/canaima-semilla-gui/images/distri.png')
		caja.pack_start(image, False, False,10)
		image.show()
		
		global check2_nuevo_sabor
		check2_nuevo_sabor = gtk.CheckButton("Construir Nuevo Sabor")
		check2_nuevo_sabor.connect("toggled", valor_const,"uno")
		caja.pack_start(check2_nuevo_sabor, False, True, 5)
		check2_nuevo_sabor.show()
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(False)
		descripcion.set_markup("\n\n")
		caja.pack_start(descripcion, False, False,0)
		descripcion.show()
	
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
		
		#--------------------Sigueinte ventana------------------------	
		boton_siguiente = gtk.Button("Siguiente>")
		
		def paso_sig(self):
			hilo = threading.Thread(target=csns, args=(self))
			hilo.start()
		
		def csns(self, data=None):
			if check1_constru_iso.get_active() == False and check2_nuevo_sabor.get_active() == False:
				gtk.gdk.threads_enter()
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar algunas de las opciones: \n\n\t  Crear IS0'S   ó   Construir Nuevo-Sabor\t")
				md.set_title('Crear ISOS o Construir Nuevo-Sabor')
				md.run()
				md.destroy()
				gtk.gdk.threads_leave()
			
			if check1_constru_iso.get_active() == True:
				gtk.gdk.threads_enter()
				construir_iso.construir_isos()
				self.window.hide()
				gtk.gdk.threads_leave()
			
			if check2_nuevo_sabor.get_active() == True:
				gtk.gdk.threads_enter()
				paso1.Paso1()
				self.window.hide()
				gtk.gdk.threads_leave()
		
		boton_siguiente.connect("clicked", paso_sig)
		boton_siguiente.set_size_request(85, 30)
		caja.pack_start(boton_siguiente, False, False, 325)
		boton_siguiente.show()
		#------------------------------------------------------------
		return caja
		
	def __init__(self):
			
		self.window = gtk.Window()
		self.window.set_border_width(0)
		self.window.set_title("Canaima Semilla Bienvenido")
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_size_request(600, 600)
		self.window.set_resizable(False)
		self.window.connect("destroy", gtk.main_quit)
		self.window.set_icon_from_file('/usr/share/icons/canaima-iconos/apps/48/c-s.png')
		
		self.vbox = gtk.VBox(False, 5)
		
		self.box2 = self.make_imag1(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_label11(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.separator = gtk.HSeparator()
		self.vbox.pack_start(self.separator, False, False, 0)
		self.separator.show()
		
		self.box2 = self.make_label1(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_label2(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_boton_check(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.separator = gtk.HSeparator()
		self.vbox.pack_start(self.separator, False, False, 0)
		self.separator.show()
		
		self.box2 = self.make_botones(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.window.add(self.vbox)
		self.window.show_all()
		
#-------------------------------ventana 1---------------------------  
if __name__ == "__main__":
	app = bienvenido_1()
	gtk.main()
