#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----Librerias-----#
import os
import gtk
import re
import urllib
import threading
from subprocess import Popen, PIPE, STDOUT

import config
import paso1, paso3

#---Hilo Principal----#
gtk.gdk.threads_init()

class Paso2():
	
	def __init__(self):
		
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_title('Crear Nuevo Sabor: Paso 2')
		self.window.set_size_request(600, 600)
		self.window.set_resizable(False)
		self.window.connect("delete_event", self.on_delete)
		self.window.connect("destroy", gtk.main_quit)
		self.window.set_icon_from_file('/usr/share/icons/canaima-iconos/apps/48/c-s.png')
		
		#------------------Empaquetado de cajas------------------#
		self.box1 = gtk.VBox(False, 0)
		
		self.box2 = self.make_imag1(False, 0, False, False, 0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.etiqueta1(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		separator = gtk.HSeparator()
		self.box1.pack_start(separator, False, False, 0)
		separator.show()
	
		self.box2 = self.caja1(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja2(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja3(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja4(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja5(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja6(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja_buffer(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja7(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja_buffer2(False, 0, False, False,0)
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
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Si regresa al paso anterior la carpeta creada será eliminada.\n ¿Desea regresar al paso anterior?")
			md.set_title('Cerrar')
			respuesta = md.run()
			md.destroy()
			gtk.gdk.threads_leave()
		
		
			if respuesta == gtk.RESPONSE_YES:
			
				gtk.gdk.threads_enter()
				os.system('rm -r '+config.ruta)
				paso1.Paso1()
				self.window.hide()
				gtk.gdk.threads_leave()
		
		boton_atras.set_size_request(80, 30)
		boton_atras.connect("clicked", hilo_atras)
		caja.pack_start(boton_atras, False, False, 10)
		boton_atras.show()
		
		#--------------------Sigueinte ventana------------------------	
		global boton_siguiente
		boton_siguiente = gtk.Button("Siguiente>")
		
		#-------------Método para crear el hilo del método funciones-------------#		
		def funciones_clic(self):
			hilo=threading.Thread(target = funciones, args=self)
			hilo.start()
				
		#-------------Método que valida todos los campos del archivo sabor.conf-------------#			
		def funciones(self):
			
			boton_siguiente.set_sensitive(False)
			boton_atras.set_sensitive(False)
			boton.set_sensitive(False)
			boton2.set_sensitive(False)
			
			if texto1.get_text() == "": 
				gtk.gdk.threads_enter()
				error=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe especificar en \"Publicado por:\" el nombre de quien publica la imagen")
				error.run()
				error.destroy()
				gtk.gdk.threads_leave()
				
			elif texto3.get_text() == "":
				gtk.gdk.threads_enter()
				error=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe especificar el \"Nombre de la Metadistribución:\"")
				error.run()
				error.destroy()
				gtk.gdk.threads_leave()
				
			elif textbuffer.get_text(*textbuffer.get_bounds()) == "":
				
				gtk.gdk.threads_enter()
				error=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe especificar los \"Paquetes a incluir\" escribiendo el nombre del paquete en el campo de texto y luego dar clic en el botón \"Validar\"")
				error.run()
				error.destroy()
				gtk.gdk.threads_leave()
				
			else:
				#if texto4.get_text():
				try:
					urllib.urlopen(texto4.get_text())
					
									
					f=open(config.ruta+"/sabor.conf","w")
					f.write("PUBLICADO_POR=\""+texto1.get_text()+"\"\n"+"SABOR_DIST=\""+combo.get_active_text()+"\"\n"
							+"APLICACION=\""+texto3.get_text()+"\"\n"+"MIRROR_DEBIAN=\""+texto4.get_text()+"\"\n"
							+"COMP_MIRROR_DEBIAN=\""+combo1.get_active_text()+"\"\n"+"SABOR_PAQUETES=\""+textbuffer.get_text(*textbuffer.get_bounds())+"\"\n"
							+"SABOR_PAQUETES_ISOPOOL=\""+textbuffer2.get_text(*textbuffer2.get_bounds())+"\"")
					f.close()
					
					os.system('cp /usr/share/canaima-semilla/perfiles/institucional/gtkrc-instalador '+config.ruta)
					os.system('cp /usr/share/canaima-semilla/perfiles/institucional/preseed-debconf.cfg '+config.ruta)
					os.system('cp /usr/share/canaima-semilla/perfiles/institucional/preseed-instalador.cfg '+config.ruta)
					os.system('cp /usr/share/canaima-semilla/perfiles/institucional/canaima.chroot '+config.ruta)
					os.system('cp /usr/share/canaima-semilla/perfiles/institucional/canaima.chroot.gpg '+config.ruta)
					os.system('cp /usr/share/canaima-semilla/perfiles/institucional/canaima.binary.gpg '+config.ruta)
					
									
					if os.path.exists(config.ruta):
						gtk.gdk.threads_enter()
						message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="Cambios aplicados con éxito en "+config.ruta)
						message.run()
						message.hide()
						gtk.gdk.threads_leave()
						
						gtk.gdk.threads_enter()
						paso3.Paso3()
						self.window.hide()
						gtk.gdk.threads_leave()
				
					else:
						gtk.gdk.threads_enter()
						md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe crear la carpeta con el nombre del nuevo sabor antes de continuar")
						md.run()
						md.destroy()
						gtk.gdk.threads_leave()
				
				except IOError:
					gtk.gdk.threads_enter()
					global errorURL
					errorURL=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe introducir una URL valida de donde seran descargados los paquetes con el protocolo \"http://\"")
					errorURL.run()
					errorURL.destroy()
					gtk.gdk.threads_leave()
					
			boton_siguiente.set_sensitive(True)
			boton_atras.set_sensitive(True)
			boton.set_sensitive(True)
			boton2.set_sensitive(True)
			
		boton_siguiente.connect("clicked", funciones_clic)
		boton_siguiente.set_size_request(85, 30)
		caja.pack_start(boton_siguiente, False, False, 0)
		boton_siguiente.show()
		return caja
		#------------------------------------------------------------
		
	def etiqueta1(self, homogeneous, spacing, expand, fill, padding):

		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
	
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("<b>Paso 2. Configure el archivo \"sabor.conf\":</b>")
		caja.pack_start(descripcion, True, False,5)
		descripcion.show()
		return caja
	
	def caja1(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Publicado por:\t\t\t\t\t")
		etiqueta.set_justify(gtk.JUSTIFY_LEFT)
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
		
		global texto1	
		texto1 = gtk.Entry()
		texto1.connect('insert-text', self.insertar)
		texto1.set_text("Canaima GNU/Linux; http://canaima.softwarelibre.gob.ve/")
		texto1.set_sensitive(True)
		caja.pack_start(texto1, True, True, 5)
		texto1.show()
			
		return caja		
			
	def caja2(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Distribución Debian:\t\t\t")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global combo
		combo = gtk.combo_box_new_text()
		#combo.append_text('Selecccione:')
		combo.append_text('lenny')
		combo.append_text('squeeze')
		combo.append_text('wheezy')
		combo.append_text('sid')
		#combo.connect('changed', hacer)
		combo.set_active(1)
		caja.pack_start(combo, True, True, 5)
		combo.show()
			
		return caja
		
	def caja3(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Nombre de la Metadistribución:\t")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global texto3
		texto3 = gtk.Entry()
		texto3.connect('insert-text', self.insertar)
		texto3.set_text("Canaima GNU/Linux")
		caja.pack_start(texto3, True, True, 5)
		texto3.show()
			
		return caja
		
		
	def caja4(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Mirror de Debian:\t\t\t\t")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()

		global texto4
		texto4 = gtk.Entry()
		texto4.set_text("http://universo.canaima.softwarelibre.gob.ve/")
		texto4.connect('activate',self.validarURL)
		caja.pack_start(texto4, True, True, 5)
		texto4.show()
			
		return caja
			
			
	def caja5(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Componentes del Mirror:\t\t")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
		
		global combo1
		combo1 = gtk.combo_box_new_text()
		combo1.append_text('main')
		combo1.append_text('contrib')
		combo1.append_text('non-free')
		combo1.append_text('main contrib')
		combo1.append_text('main non-free')
		combo1.append_text('contrib non-free')
		combo1.append_text('main contrib non-free')
		#combo1.connect('changed', hacer)
		combo1.set_active(6)
		caja.pack_start(combo1, True, True, 5)
		combo1.show()
			
		return caja
		
		
	def caja6(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Paquetes a incluir:\t\t\t\t")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global texto6
		texto6 = gtk.Entry()
		texto6.connect('insert-text', self.espacio)
		texto6.set_text("canaima-semilla")
		caja.pack_start(texto6, True, True, 5)
		texto6.show()
			
		global boton
		boton = gtk.Button("  Validar  ")
		
		#-------------Método para crear el hilo del método buscar_paquetes-------------#					
		def buscar_paquetes_clic(self):
			hilo=threading.Thread(target = buscar_paquetes, args=self)
			hilo.start()
		
		#-------------Método para hacer la busqueda de los paquetes------------#			
		def buscar_paquetes(self):
			
			boton.set_sensitive(False)
			boton2.set_sensitive(False)
			boton_siguiente.set_sensitive(False)
			boton_atras.set_sensitive(False)
			#a= os.system('aptitude search '+texto6.get_text())
			p = Popen('aptitude search '+texto6.get_text(), stdout=PIPE, stderr = STDOUT, shell=True)
			validar = p.stdout.read()
			boton.set_sensitive(True)
			boton2.set_sensitive(True)
			boton_siguiente.set_sensitive(True)
			boton_atras.set_sensitive(True)
			
			if texto6.get_text() == "":
				gtk.gdk.threads_enter()
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe introducir un paquete para realizar la busqueda")
				md.run()
				md.destroy()
				gtk.gdk.threads_leave()
				
			else:
				if (texto6.get_text() == "a" or texto6.get_text() =='b' or texto6.get_text() =='c' or texto6.get_text() =='d' or texto6.get_text() =='e' or texto6.get_text() =='f' or texto6.get_text() =='g' or texto6.get_text() =='h' 
					or texto6.get_text() =='i' or texto6.get_text() =='j' or texto6.get_text() =='k' or texto6.get_text() =='l' or texto6.get_text() =='m' or texto6.get_text() =='n' or texto6.get_text() =='o' or texto6.get_text() =='p' or texto6.get_text() =='q' or texto6.get_text() =='r' 
					or texto6.get_text() =='s' or texto6.get_text() =='t' or texto6.get_text() =='u' or texto6.get_text() =='v' or texto6.get_text() =='w' or texto6.get_text() =='x' or texto6.get_text() =='y' or texto6.get_text() =='z'
					or texto6.get_text() =='0' or texto6.get_text() =='1' or texto6.get_text() =='2' or texto6.get_text() =='3' or texto6.get_text() =='4' or texto6.get_text() =='5' or texto6.get_text() =='' or texto6.get_text() =='6' or texto6.get_text() =='7' or texto6.get_text() =='8' or texto6.get_text() =='9'):
					
					gtk.gdk.threads_enter()
					message = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_CLOSE, message_format="Debe especificar el nombre completo del paquete")
					message.run()
					message.hide()
					gtk.gdk.threads_leave()
				else:
					if textbuffer.get_text(*textbuffer.get_bounds()).find(texto6.get_text()) >= 0:
						gtk.gdk.threads_enter()
						message = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_CLOSE, message_format="El paquete ya ha sido agregado")
						message.run()
						message.hide()
						gtk.gdk.threads_leave()
					else:
						if validar:
							gtk.gdk.threads_enter()
							message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="El paquete fue encontrado")
							message.run()
							message.hide()
							#almacenar.set_text(almacenar.get_text()+texto6.get_text()+" ")
							textbuffer.set_text(textbuffer.get_text(*textbuffer.get_bounds())+texto6.get_text()+" ")
							gtk.gdk.threads_leave()
							#print validar
									
						else:
							gtk.gdk.threads_enter()
							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="El paquete introducido no se encuentra")
							md.run()
							md.destroy()
							gtk.gdk.threads_leave()
					
		
		boton.connect("clicked", buscar_paquetes_clic)
		caja.pack_start(boton, False, False, 5)
		boton.show()
			
			
		return caja
		
	def caja_buffer(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(2)
			
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
			
		textview.set_size_request(50, 50)		
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
		
	def caja7(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
			
		etiqueta=gtk.Label("Paquetes Extras:\t\t\t\t")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global texto7
		texto7 = gtk.Entry()
		texto7.connect('insert-text', self.espacio)
		texto7.set_text("")
		caja.pack_start(texto7, True, True, 5)
		texto7.show()
			
		global boton2
		boton2 = gtk.Button("  Validar  ")
		
		#-------------Método para crear el hilo del método buscar_paquetes-------------#					
		def buscar_isopool_clic(self):
			hilo=threading.Thread(target = buscar_isopool, args=self)
			hilo.start()			
				
		#-------------Método para hacer la busqueda de los paquetes------------#			
		def buscar_isopool(self):
			
			boton2.set_sensitive(False)
			boton.set_sensitive(False)
			boton_siguiente.set_sensitive(False)
			boton_atras.set_sensitive(False)
			#a= os.system('aptitude search '+texto6.get_text())
			p = Popen('aptitude search '+texto7.get_text(), stdout=PIPE, stderr = STDOUT, shell=True)
			validar = p.stdout.read()
			boton2.set_sensitive(True)
			boton.set_sensitive(True)
			boton_siguiente.set_sensitive(True)
			boton_atras.set_sensitive(True)
			
			
			if texto7.get_text() == "":
				gtk.gdk.threads_enter()
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe introducir un paquete para realizar la busqueda")
				md.run()
				md.destroy()
				gtk.gdk.threads_leave()
				
			else:
				if (texto7.get_text() == "a" or texto7.get_text() =='b' or texto7.get_text() =='c' or texto7.get_text() =='d' or texto7.get_text() =='e' or texto7.get_text() =='f' or texto7.get_text() =='g' or texto7.get_text() =='h' 
					or texto7.get_text() =='i' or texto7.get_text() =='j' or texto7.get_text() =='k' or texto7.get_text() =='l' or texto7.get_text() =='m' or texto7.get_text() =='n' or texto7.get_text() =='o' or texto7.get_text() =='p' or texto7.get_text() =='q' or texto7.get_text() =='r' 
					or texto7.get_text() =='s' or texto7.get_text() =='t' or texto7.get_text() =='u' or texto7.get_text() =='v' or texto7.get_text() =='w' or texto7.get_text() =='x' or texto7.get_text() =='y' or texto7.get_text() =='z'
					or texto7.get_text() =='0' or texto7.get_text() =='1' or texto7.get_text() =='2' or texto7.get_text() =='3' or texto7.get_text() =='4' or texto7.get_text() =='5' or texto7.get_text() =='' or texto7.get_text() =='6' or texto7.get_text() =='7' or texto7.get_text() =='8' or texto7.get_text() =='9'):
					
					gtk.gdk.threads_enter()
					message = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_CLOSE, message_format="Debe especificar el nombre completo del paquete")
					message.run()
					message.hide()
					gtk.gdk.threads_leave()
				else:
					if textbuffer2.get_text(*textbuffer2.get_bounds()).find(texto7.get_text()) >= 0:
						gtk.gdk.threads_enter()
						message = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_CLOSE, message_format="El paquete ya ha sido agregado")
						message.run()
						message.hide()
						gtk.gdk.threads_leave()
					else:
						if validar:
							gtk.gdk.threads_enter()
							message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="El paquete fue encontrado")
							message.run()
							message.hide()
							#almacenar.set_text(almacenar.get_text()+texto6.get_text()+" ")
							textbuffer2.set_text(textbuffer2.get_text(*textbuffer2.get_bounds())+texto7.get_text()+" ")
							gtk.gdk.threads_leave()
							#print validar
										
						else:
							gtk.gdk.threads_enter()
							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="El paquete introducido no se encuentra")
							md.run()
							md.destroy()
							gtk.gdk.threads_leave()
		
		boton2.connect("clicked", buscar_isopool_clic)
		caja.pack_start(boton2, False, False, 5)
		boton2.show()
			
		return caja
			
	def caja_buffer2(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(2)
			
		scrolledwindow = gtk.ScrolledWindow()
		scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
   
		marco = gtk.Frame()
		alineacion = gtk.Alignment(xalign=0.5, yalign=0.1, xscale=0.98, yscale=0.5)
   
		global textview2
		textview2 = gtk.TextView()
		global textbuffer2
		textbuffer2 = textview2.get_buffer()
		
		start, end = textbuffer2.get_bounds()
		textview2.set_wrap_mode(gtk.WRAP_WORD)
		
		textview2.set_size_request(50, 50)	
		textview2.set_editable(False)
		scrolledwindow.add(textview2)
		alineacion.add(scrolledwindow)
		marco.add(alineacion)
		caja.pack_start(marco, True, True, 5)
   
		textview2.show()
		scrolledwindow.show()
		alineacion.show()
		marco.show()
			
		return caja
		
	def espacios(self, homogeneous, spacing, expand, fill, padding):
		
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
		
		etiqueta_vacia = gtk.Label("")
		caja.pack_start(etiqueta_vacia, False, False,0)
		etiqueta_vacia.show()
		
		return caja
		
#-------------Método para no permitir signos en los campos-------------#			
	def insertar(self, editable, new_text, new_text_length, position):
		sin_signos = re.compile('[.a-zA-Z0-9_ -]')
			
		if sin_signos.match(new_text) is None:
			editable.stop_emission('insert-text')
				
#-------------Método para no permitir espacios en el campo buscar paquetes-------------#			
	def espacio(self, editable, new_text, new_text_length, position):
		sin_espacios = re.compile('[a-z0-9-]')
			
		if sin_espacios.match(new_text) is None:
			editable.stop_emission('insert-text')
		
#-------------Método para validar las URL-------------#					
	def validarURL(self, url):
		try:
			urllib.urlopen(texto4.get_text())
		except IOError:
			errorURL=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe introducir una URL valida de donde seran descargados los paquetes")
			errorURL.run()
			errorURL.destroy()
							

if __name__ == "__main__":
	app = Paso2()
	gtk.main()
