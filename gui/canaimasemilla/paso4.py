#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----Librerias-----#
import os
import gtk
import threading
import Image
from PIL import Image
from subprocess import Popen, PIPE, STDOUT


import config
import paso3, paso5

#---Hilo Principal----#
gtk.gdk.threads_init()

class Paso4():
	
	def __init__(self):
		
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_title('Crear Nuevo Sabor:')
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
		
		self.box2 = self.caja1(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		separator = gtk.HSeparator()
		self.box1.pack_start(separator, False, True, 35)
		separator.show()
		
		self.box2 = self.etiqueta2(False, 0, False, False,0)
		self.box1.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.caja2(False, 0, False, False,0)
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
		boton_atras = gtk.Button("<Atras")
		
		def hilo_atras(self):
			hilo = threading.Thread(target=atras, args=(self))
			hilo.start()
		
		def atras(self):
			gtk.gdk.threads_enter()
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Si regresa al paso anterior los cambios realizados al archivo \""+paso3.texto1.get_text()+".binary\" serán eliminados.\n ¿Desea regresar al paso anterior?")
			md.set_title('Cerrar')
			respuesta = md.run()
			md.destroy()
			gtk.gdk.threads_leave()
		
		
			if respuesta == gtk.RESPONSE_YES:
			
				gtk.gdk.threads_enter()
				paso3.Paso3()
				self.window.hide()
				gtk.gdk.threads_leave()
		
		boton_atras.set_size_request(80, 30)
		boton_atras.connect("clicked", hilo_atras)
		caja.pack_start(boton_atras, False, False, 10)
		boton_atras.show()
		
		#--------------------Sigueinte ventana------------------------	
		global boton_siguiente
		boton_siguiente = gtk.Button("Siguiente>")
		
		#-------------Método para crear el hilo del método validar-------------#					
		def hilo_validar(self):
			hilo=threading.Thread(target = validar, args=self)
			hilo.start()
				
		#~~~~~~~~~~~~~ Método para validar la busqueda de las imagenes ~~~~~~~~~~~~~~~~~~~~# 				
		
		def validar (self):
			
			gtk.gdk.threads_enter()
			pregunta=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Las imágenes syslinux y banner-instalador son opcionales.\n\nSi selecciona NO el proceso continuará de forma normal\n\n¿Desea introducir la imágenes?\n")
			pregunta.set_title('Insertar Imágenes')
			respuesta = pregunta.run()
			pregunta.destroy()
			gtk.gdk.threads_leave()
			
			if respuesta == gtk.RESPONSE_NO:
				gtk.gdk.threads_enter()
				paso5.Paso5()
				self.window.hide()
				gtk.gdk.threads_leave()
		
			if respuesta == gtk.RESPONSE_YES:
			
		#~~~~~~~~~~~~~ Validar para la imagen syslinux.png ~~~~~~~~~~~~~~~~~~~~# 
			
				if texto_sys.get_text() == "":
					gtk.gdk.threads_enter()
					mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="Debe eligir la ubicación de la imagen “syslinux.png”")
					mensaje.run()
					mensaje.destroy()
					gtk.gdk.threads_leave()
				
				elif os.path.isfile(texto_sys.get_text()):
					gtk.gdk.threads_enter()
					img = Image.open(texto_sys.get_text())
					i=img.size
					gtk.gdk.threads_leave()
							
					if i <= (1024, 768):
						gtk.gdk.threads_enter()
						os.system('cp '+texto_sys.get_text()+' '+config.ruta)
						gtk.gdk.threads_leave()
				
						if os.path.exists(config.ruta):
							gtk.gdk.threads_enter()
							message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="Cambios aplicados con éxito en "+config.ruta)
							message.run()
							message.hide()
							gtk.gdk.threads_leave()
				
						else:
							gtk.gdk.threads_enter()
							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe crear la carpeta con el nombre del nuevo sabor antes de continuar")
							md.run()
							md.destroy()
							gtk.gdk.threads_leave()
				
					else:
						gtk.gdk.threads_enter()
						mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="La imagen “syslinux.png” debe tener una dimensión no mayor a 1024x768 pixeles")
						mensaje.run()
						mensaje.destroy()
						gtk.gdk.threads_leave()
				
						texto_sys.set_text("")
					
				else:
					gtk.gdk.threads_enter()
					mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK, message_format="La ruta especificada para la imagen “syslinux.png” no es correcta")
					mensaje.run()
					mensaje.destroy()
					gtk.gdk.threads_leave()

				
				#~~~~~~~~~~~~~ Validar para la imagen banner-instalador.png ~~~~~~~~~~~~~~~~~~~~# 
					
				if texto2.get_text() == "":
					gtk.gdk.threads_enter()
					mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="Debe eligir la ubicación de la imagen “banner-instalador.png”")
					mensaje.run()
					mensaje.destroy()
					gtk.gdk.threads_leave()
				
				elif os.path.isfile(texto2.get_text()):
					gtk.gdk.threads_enter()
					img = Image.open(texto2.get_text())
					i=img.size
					gtk.gdk.threads_leave()
					
					if i <= (800, 75):
						gtk.gdk.threads_enter()
						os.system('cp '+texto2.get_text()+' '+config.ruta)
						gtk.gdk.threads_leave()
				
						if os.path.exists(config.ruta):
							gtk.gdk.threads_enter()
							message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="Cambios aplicados con éxito en "+config.ruta)
							message.run()
							message.hide()
							gtk.gdk.threads_leave()
							
							gtk.gdk.threads_enter()
							paso5.Paso5()
							self.window.hide()
							gtk.gdk.threads_leave()
				
						else:
							gtk.gdk.threads_enter()
							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe crear la carpeta con el nombre del nuevo sabor antes de continuar")
							md.run()
							md.destroy()
							gtk.gdk.threads_leave()
				
					else:
						gtk.gdk.threads_enter()
						mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="La imagen “banner-instalador.png” debe tener una dimensión exacta de 800x75 pixeles")
						mensaje.run()
						mensaje.destroy()
						gtk.gdk.threads_leave()
				
						texto2.set_text("")
					
				else:
					gtk.gdk.threads_enter()
					mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK, message_format="La ruta especificada para la imagen “banner-instalador.png” no es correcta")
					mensaje.run()
					mensaje.destroy()
					gtk.gdk.threads_leave()
					
			
		#boton_siguiente.set_sensitive(False)
		boton_siguiente.connect("clicked", hilo_validar)
		boton_siguiente.set_size_request(85, 30)
		caja.pack_start(boton_siguiente, False, False, 0)
		boton_siguiente.show()
		return caja
		#------------------------------------------------------------
	
	def espacios(self, homogeneous, spacing, expand, fill, padding):
		
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
		
		etiqueta_vacia = gtk.Label("\n\n")
		caja.pack_start(etiqueta_vacia, False, False,0)
		etiqueta_vacia.show()
		
		return caja
	
	#~~~~~~~~~~~~~ Cajas de la GUI ~~~~~~~~~~~~~~~~~~~~# 	
	def etiqueta1(self, homogeneous, spacing, expand, fill, padding):

		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
	
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\n<b>Paso 4.\n\nIntroduzca una imagen PNG llamada “syslinux.png” de una\n dimensión no mayor a 1024x768 pixeles, la cuál servirá de\n fondo en el menú de inicio del Medio Vivo.\n</b>")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,10)
		descripcion.show()
		return caja
			
	def etiqueta2(self, homogeneous, spacing, expand, fill, padding):

		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
	
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\n\n<b>Introduzca una imagen PNG llamada “banner-instalador.png”\n de una dimensión exacta de 800x75 pixeles, la cuál será\n el banner del dialogo del instalador del Medio Vivo.\n</b>")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,10)
		descripcion.show()
		return caja
			
	def caja1(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
			
		etiqueta=gtk.Label("Buscar imagen: ")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global texto_sys
		texto_sys = gtk.Entry()
		#texto_sys.connect("activate", hacer)
		caja.pack_start(texto_sys, True, True, 5)
		texto_sys.show()
			
		boton = gtk.Button(" Examinar... ")
		
		#-------------Método para crear el hilo del método buscar_syslinux-------------#					
		def hilo_buscar_syslinux(self):
			hilo=threading.Thread(target = buscar_syslinux, args=(self))
			hilo.start()
					
		#~~~~~~~~~~~~~ Método para realizar la busqueda de la imagen syslinux.png ~~~~~~~~~~~~~~~~~~~~# 
			
		def buscar_syslinux(self):
			gtk.gdk.threads_enter()
			dialog = gtk.FileChooserDialog("Ruta de imagen .png", None, gtk.FILE_CHOOSER_ACTION_OPEN,
											(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
											gtk.STOCK_OK, gtk.RESPONSE_OK))
			filter = gtk.FileFilter()
			filter.set_name("Imagenes")
			filter.add_pattern("syslinux.png")
			dialog.add_filter(filter)
			respuesta = dialog.run()
			filename = dialog.get_filename()
			dialog.destroy()
			gtk.gdk.threads_leave()


			if respuesta == gtk.RESPONSE_OK:
				gtk.gdk.threads_enter()
				texto_sys.set_text(filename)
				ruta = filename
				img = Image.open(ruta)
				b = img.size
				gtk.gdk.threads_leave()
							
				#~ if b <= (1024, 768):
					#~ gtk.gdk.threads_enter()
					#~ os.system('cp '+texto_sys.get_text()+' '+config.ruta)
					#~ gtk.gdk.threads_leave()
				#~ 
					#~ if os.path.exists(config.ruta):
						#~ gtk.gdk.threads_enter()
						#~ message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="Cambios aplicados con éxito en "+config.ruta)
						#~ message.run()
						#~ message.hide()
						#~ gtk.gdk.threads_leave()
				#~ 
					#~ else:
						#~ gtk.gdk.threads_enter()
						#~ md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe crear la carpeta con el nombre del nuevo sabor antes de continuar")
						#~ md.run()
						#~ md.destroy()
						#~ gtk.gdk.threads_leave()
				#~ 
				#~ else:
					#~ gtk.gdk.threads_enter()
					#~ mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="La imagen “syslinux.png” debe tener una dimensión no mayor a 1024x768 pixeles")
					#~ mensaje.run()
					#~ mensaje.destroy()
					#~ gtk.gdk.threads_leave()
				#~ 
					#~ texto_sys.set_text("")
		
		boton.connect("clicked", hilo_buscar_syslinux)
		caja.pack_start(boton, False, False, 5)
		boton.show()
			
		return caja	
			
	def caja2(self, homogeneous, spacing, expand, fill, padding):
			
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(10)
			
		etiqueta=gtk.Label("Buscar imagen: ")
		caja.pack_start(etiqueta, False, False, 5)
		etiqueta.show()
			
		global texto2
		texto2 = gtk.Entry()
		#texto_sys.connect("activate", hacer)
		caja.pack_start(texto2, True, True, 5)
		texto2.show()
			
		boton = gtk.Button(" Examinar... ")
		
		#-------------Método para crear el hilo del método buscar_banner instalador-------------#					
		def hilo_buscar_banner_instalador(self):
			hilo=threading.Thread(target = buscar_banner_instalador, args=(self))
			hilo.start()
						
		#~~~~~~~~~~~~~ Método para realizar la busqueda de la imagen banner-instalador.png ~~~~~~~~~~~~~~~~~~~~# 		
		
		def buscar_banner_instalador(self):
			gtk.gdk.threads_enter()
			dialog = gtk.FileChooserDialog("Ruta de imagen .png", None, gtk.FILE_CHOOSER_ACTION_OPEN,
										(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
										gtk.STOCK_OK, gtk.RESPONSE_OK))
			filter = gtk.FileFilter()
			filter.set_name("Imagenes")
			filter.add_mime_type("Imagenes/png")
			filter.add_pattern("banner-instalador.png")
			dialog.add_filter(filter)
			respuesta = dialog.run()
			filename = dialog.get_filename()
			dialog.destroy()
			gtk.gdk.threads_leave()

			if respuesta == gtk.RESPONSE_OK:
				gtk.gdk.threads_enter()
				texto2.set_text(filename)
				ruta = filename
				img = Image.open(ruta)
				a= img.size
				gtk.gdk.threads_leave()
							#~ 
				#~ if a == (800, 75):
					#~ gtk.gdk.threads_enter()
					#~ os.system('cp '+texto2.get_text()+' '+config.ruta)
					#~ gtk.gdk.threads_leave()
				#~ 
					#~ if os.path.exists(config.ruta):
						#~ gtk.gdk.threads_enter()
						#~ message = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, message_format="Cambios aplicados con éxito en "+config.ruta)
						#~ message.run()
						#~ message.hide()
						#~ gtk.gdk.threads_leave()
				#~ 
					#~ else:
						#~ gtk.gdk.threads_enter()
						#~ md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Debe crear la carpeta con el nombre del nuevo sabor antes de continuar")
						#~ md.run()
						#~ md.destroy()
						#~ gtk.gdk.threads_leave()
				#~ 
				#~ else:
					#~ gtk.gdk.threads_enter()
					#~ mensaje=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="La imagen “banner-instalador.png” debe tener una dimensión exacta de 800x75 pixeles")
					#~ mensaje.run()
					#~ mensaje.destroy()
					#~ gtk.gdk.threads_leave()
				#~ 
					#~ texto2.set_text("")
		
		boton.connect("clicked", hilo_buscar_banner_instalador)
		caja.pack_start(boton, False, False, 5)
		boton.show()
			
		return caja	
		
	def boton_aplicar_cambios(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(15)
		
		global boton_aplicar
		boton_aplicar = gtk.Button("Aplicar Cambios")
		boton_aplicar.connect("clicked", self.hilo_validar)
		caja.pack_start(boton_aplicar, True, False, 10)
		boton_aplicar.show()
			
		return caja
			
	def siguiente(self, data=None):
		paso5.Paso5()
		self.window.hide()
	

if __name__ == "__main__":
	app = Paso4()
	gtk.main()
