#-*- coding: UTF-8 -*-

import os
import pygtk
pygtk.require('2.0')
import gtk
import threading
import gobject
from subprocess import Popen, PIPE, STDOUT
import bienvenido

gtk.gdk.threads_init()

usb_1= "usb"
cd_1= "iso"	
i386_1= "i386"
amd64_1= "amd64"




def actualizar_lista(self):
	combo.get_model().clear()
	text = next(os.walk('/usr/share/canaima-semilla/perfiles/'))[1]
	for t in text:
		combo.append_text(t)

class construir_isos():
	
	
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
		boton_cerrar = gtk.Button("Cancelar")
		boton_cerrar.set_size_request(80, 30)
		boton_cerrar.set_sensitive(False)
		
		def clic_boton2(self):
			hilo = threading.Thread(target=cerrar, args=(self))
			hilo.start()
		
		def cerrar(self):			
			gtk.gdk.threads_enter()
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="\tEsta seguro que desea cancerlar \t\n\tla creación de la imagen:\t")
			md.set_title('Cancelar')
			respuesta = md.run()
			md.destroy()
			gtk.gdk.threads_leave()
			if respuesta == gtk.RESPONSE_YES:
				
				x2= Popen(["pkill lb"], shell=True, stdout=PIPE)
				x3= Popen(["pkill live-build"], shell=True, stdout=PIPE)
				x1= Popen(["pkill c-s"], shell=True, stdout=PIPE)
		
		boton_cerrar.connect("clicked", clic_boton2)
		caja.pack_start(boton_cerrar, False, False, 5)
		boton_cerrar.show()
		#----------------------------------------------------------
		
		#-----------------------ayuda--------------------------
		boton_ayuda = gtk.Button("Ayuda")
		def clic_ayuda(self):
			hilo = threading.Thread(target=ayuda_1, args=(self))	
			hilo.start()
		
		def ayuda_1(self, widget=None):								
			x= Popen(["yelp c-s.xml"], shell=True, stdout=PIPE)

					
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
		boton_atras.set_size_request(80, 30)
		
		def paso_sig(self):
			hilo = threading.Thread(target=paso0, args=(self))
			hilo.start()
		
		def paso0(self, data=None):
			gtk.gdk.threads_enter()	
			bienvenido.bienvenido_1()
			self.window.hide()			
			gtk.gdk.threads_leave()
		
		boton_atras.connect("clicked", paso_sig)
		caja.pack_start(boton_atras, False, False, 10)
		boton_atras.show()
		
		#--------------------Sigueinte ventana------------------------	
		boton_siguiente = gtk.Button("Generar")
		
		#Threading revisar
		def clic_boton(self):
			hilo = threading.Thread(target=crear_iso, args=(self))
			hilo.start()
			
		
		##########################################Crear ISO o USB o i386 o amd64 y seleccionar SABOR#####################################################################################################
		def crear_iso(self, data=None):
				def progres(self):
					pbar.pulse()
					return True
				
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
					
				#gtk.gdk.threads_enter()
				#-------------CREAR iso------------------------------------------------------------------------------------------------------
					if check1.get_active() == True:
						# Validar error i386 o amd64
						
						if check3.get_active() ==False and check4.get_active() ==False:
							gtk.gdk.threads_enter()
							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar La Arquitectura i386 o amd64\t\t")
							md.set_title('Error i386 o amd64')
							md.run()
							md.destroy()
							gtk.gdk.threads_leave()
						#----------------------------DEFINIENDO ARQUITECTURA-----------------------------------------------------------------------
						if check3.get_active() ==True:
							#---------------------------------------Validar opciones de la ventana desplegable---------------------------------
							if combo.get_active_text():
								
								
								
								#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ISO 1386 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
								timer_1 = gobject.timeout_add (100, progres,self)
								pbar.set_text("CONSTRUYENDO IMAGEN")
								
								#botones 1 2 3 4 combo
								check1.set_sensitive(False)
								check2.set_sensitive(False)
								check3.set_sensitive(False)
								check4.set_sensitive(False)
								combo.set_sensitive(False)
								boton_siguiente.set_sensitive(False)
								boton_atras.set_sensitive(False)
								boton_cerrar.set_sensitive(True)
								
								#crear Isos
								systema = os.system('c-s construir --medio='+cd_1+' --arquitectura='+i386_1+' --sabor='+combo.get_active_text())
								#~ error=os.system('echo $?')
								#~ error= Popen('echo $?', stdout=PIPE, stderr = STDOUT, shell=True) #shell=True, stdout=PIPE)
								#~ eror = error.stdout.read().split('\n')[0]							
								#~ x= "0"
								#~ y= "1"
								#~ z= "130"
								# if salida correcta
								if systema == 0:
									pbar.set_fraction(1)
									pbar.set_text("FINALIZADO")
									timer_2 = gobject.source_remove(timer_1)
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK, message_format="\tSe ha creado una imagen ISO de canaima-"+combo.get_active_text()+".\n\n\tLa imagen ''canaima-"+combo.get_active_text()+"_i386.iso'' resultante \n\tde los proceso de construcción se encuentra en la \n\tdireccion:\t\n\n\t\t/usr/share/canaima-semilla/semillero/")
									md.set_title('Finalizado')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									pbar.set_text(" ")
									check1.set_sensitive(True)
									check2.set_sensitive(True)
									check3.set_sensitive(True)
									check4.set_sensitive(True)
									combo.set_sensitive(True)
									boton_siguiente.set_sensitive(True)
									boton_atras.set_sensitive(True)
									boton_cerrar.set_sensitive(False)
									x= Popen(["nautilus /usr/share/canaima-semilla/semillero/"], shell=True, stdout=PIPE)
								
								#if salida negativa																									#~ 
								if systema == 256:
									pbar.set_fraction(0.0)
									pbar.set_text("ERROR EN CONSTRUCCIÓN")
									timer_2 = gobject.source_remove(timer_1)
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Ocurrio un error durante la generacion de la imagen. Envie un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo /usr/share/canaima-semilla/semillero/binary.log")
									md.set_title('Error en construcción')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									pbar.set_text(" ")
									
									check1.set_sensitive(True)
									check2.set_sensitive(True)
									check3.set_sensitive(True)
									check4.set_sensitive(True)
									combo.set_sensitive(True)
									boton_siguiente.set_sensitive(True)
									boton_atras.set_sensitive(True)
									boton_cerrar.set_sensitive(False)
									
										#~ 
								#~ #else:
								#if cancelar
								if systema == 36608:
									pbar.set_fraction(0.0)
									pbar.set_text("IMAGEN CANCELADA")
									timer_2 = gobject.source_remove(timer_1)
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="\tLa construcción de la imagen ISO de\n\tcanaima-"+combo.get_active_text()+" ha sido cancelada.\t")
									md.set_title('Imagen cancelada')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									pbar.set_text(" ")
									
									check1.set_sensitive(True)
									check2.set_sensitive(True)
									check3.set_sensitive(True)
									check4.set_sensitive(True)
									combo.set_sensitive(True)
									boton_siguiente.set_sensitive(True)
									boton_atras.set_sensitive(True)
									boton_cerrar.set_sensitive(False)
									
																	
											
								#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ISO 1386 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#						
							else:
								gtk.gdk.threads_enter()
								md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar alguno de los Sabores existentes  \t")
								md.set_title('Sabores')
								md.run()
								md.destroy()
								gtk.gdk.threads_leave()
									
						if check4.get_active() ==True:
							#---------------------------------------Validar opciones de la ventana desplegable-----------------------------------------
							if combo.get_active_text():
								x= Popen(["arch"], shell=True, stdout=PIPE)
								z = x.stdout.read().split('\n')[0]
								y ="i686"	
								if z == y:
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tEl Sistema  operativo de  su computador  no\t\t \n\tpermite crear Imagenes CD/DVD o USB  con  \n\tarquitectura amd64.\t")
									md.set_title('Error amd64')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									check4.set_active(False)
								else:
									#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ISO amd64 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
									
									
									timer_1 = gobject.timeout_add (100, progres,self)
									pbar.set_text("CONSTRUYENDO IMAGEN")
									#boton generar cancelar
									
									check1.set_sensitive(False)
									check2.set_sensitive(False)
									check3.set_sensitive(False)
									check4.set_sensitive(False)
									combo.set_sensitive(False)
									boton_siguiente.set_sensitive(False)
									boton_atras.set_sensitive(False)
									boton_cerrar.set_sensitive(True)
									
									#Crear Isos
									systema = os.system('c-s construir --medio='+cd_1+' --arquitectura='+amd64_1+' --sabor='+combo.get_active_text())	
									#~ error= Popen(["echo $?"], shell=True, stdout=PIPE)
									#~ eror = error.stdout.read().split('\n')[0]
									#~ x= "0"
									#~ y= "1"
									#~ z= "130"
									if systema == 0:
										pbar.set_fraction(1)
										pbar.set_text("FINALIZADO")
										timer_2 = gobject.source_remove(timer_1)
										gtk.gdk.threads_enter()
										md=gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK, message_format="\tSe ha creado una imagen ISO de canaima-"+combo.get_active_text()+".\n\n\tLa imagen ''canaima-"+combo.get_active_text()+"_amd64.iso'' resultante \n\tde los proceso de construcción se encuentra en la \n\tdireccion:\t\n\n\t\t/usr/share/canaima-semilla/semillero/")
										md.set_title('Finalizado')
										md.run()
										md.destroy()
										gtk.gdk.threads_leave()
										pbar.set_text(" ")
										
										check1.set_sensitive(True)
										check2.set_sensitive(True)
										check3.set_sensitive(True)
										check4.set_sensitive(True)
										combo.set_sensitive(True)
										boton_siguiente.set_sensitive(True)
										boton_atras.set_sensitive(True)
										boton_cerrar.set_sensitive(False)
										x= Popen(["nautilus /usr/share/canaima-semilla/semillero/"], shell=True, stdout=PIPE)
																			
									if systema == 256:
										pbar.set_fraction(0.0)
										pbar.set_text("ERROR EN CONSTRUCCIÓN")
										timer_2 = gobject.source_remove(timer_1)
										gtk.gdk.threads_enter()
										md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Ocurrio un error durante la generacion de la imagen. Envie un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo /usr/share/canaima-semilla/semillero/binary.log")
										md.set_title('Error en construcción')
										md.run()
										md.destroy()
										gtk.gdk.threads_leave()
										pbar.set_text(" ")
										
										check1.set_sensitive(True)
										check2.set_sensitive(True)
										check3.set_sensitive(True)
										check4.set_sensitive(True)
										combo.set_sensitive(True)
										boton_siguiente.set_sensitive(True)
										boton_atras.set_sensitive(True)
										boton_cerrar.set_sensitive(False)
																		
									if systema == 36608:
										pbar.set_fraction(0.0)
										pbar.set_text("IMAGEN CANCELADA")
										timer_2 = gobject.source_remove(timer_1)
										gtk.gdk.threads_enter()
										md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="\tLa construcción de la imagen ISO de\n\tcanaima-"+combo.get_active_text()+" ha sido cancelada.\t")
										md.set_title('Imagen cancelada')
										md.run()
										md.destroy()
										gtk.gdk.threads_leave()
										pbar.set_text(" ")
										
										check1.set_sensitive(True)
										check2.set_sensitive(True)
										check3.set_sensitive(True)
										check4.set_sensitive(True)
										combo.set_sensitive(True)
										boton_siguiente.set_sensitive(True)
										boton_atras.set_sensitive(True)
										boton_cerrar.set_sensitive(False)
										
									#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ISO amd64 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
							else:
								gtk.gdk.threads_enter()
								md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar alguno de los Sabores existentes  \t")
								md.set_title('Sabores')
								md.run()
								md.destroy()
								gtk.gdk.threads_leave()
					
					#------ validar error CD o USB---------------------------------------------------------------------------------------------------
					if check1.get_active() == False and check2.get_active() == False:
						
						gtk.gdk.threads_enter()
						md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar el Medio CD/DVD o USB\t\t")
						md.set_title('Error CD/DVD o USB')
						md.run()
						md.destroy()
						gtk.gdk.threads_leave()
					
					#------------------------ CREAR usb-------------------------------------------------------------------------------------------					
					if check2.get_active() == True:
						# validar error i386 o amd64
						if check3.get_active() ==False and check4.get_active() ==False:
							gtk.gdk.threads_enter()
							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar La Arquitectura i386 o amd64\t\t")
							md.set_title('Error i386 o amd64')
							md.run()
							md.destroy()
							gtk.gdk.threads_leave()
						#----------------------------DEFINIENDO ARQUITECTURA-------------------------------------------------------------------------------
						if check3.get_active() ==True:
							#-----------------------------Validar opciones de la ventana desplegable-----------------------------------------------------
							if combo.get_active_text():
								
								
								#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# USB i386 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
								timer_1 = gobject.timeout_add (100, progres,self)
								pbar.set_text("CONSTRUYENDO IMAGEN")
								
								check1.set_sensitive(False)
								check2.set_sensitive(False)
								check3.set_sensitive(False)
								check4.set_sensitive(False)
								combo.set_sensitive(False)
								boton_siguiente.set_sensitive(False)
								boton_atras.set_sensitive(False)
								boton_cerrar.set_sensitive(True)
								
								systema = os.system('c-s construir --medio='+usb_1+' --arquitectura='+i386_1+' --sabor='+combo.get_active_text())
								#~ error= Popen(["echo $?"], shell=True, stdout=PIPE)
								#~ eror = error.stdout.read().split('\n')[0]
								#~ x= "0"
								#~ y= "1"
								#~ z= "130"
								if systema == 0:
									pbar.set_fraction(1)
									pbar.set_text("FINALIZADO")
									timer_2 = gobject.source_remove(timer_1)
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK, message_format="\tSe ha creado una imagen ISO de canaima-"+combo.get_active_text()+".\n\n\tLa imagen ''canaima-"+combo.get_active_text()+"_i386.usb'' resultante \n\tde los proceso de construcción se encuentra en la \n\tdireccion:\t\n\n\t\t/usr/share/canaima-semilla/semillero/")
									md.set_title('Finalizado')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									pbar.set_text(" ")
									
									check1.set_sensitive(True)
									check2.set_sensitive(True)
									check3.set_sensitive(True)
									check4.set_sensitive(True)
									combo.set_sensitive(True)
									boton_siguiente.set_sensitive(True)
									boton_atras.set_sensitive(True)
									boton_cerrar.set_sensitive(False)
									x= Popen(["nautilus /usr/share/canaima-semilla/semillero/"], shell=True, stdout=PIPE)
																	
								if systema == 256:
									pbar.set_fraction(0.0)
									pbar.set_text("ERROR EN CONSTRUCCIÓN")
									timer_2 = gobject.source_remove(timer_1)
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Ocurrio un error durante la generacion de la imagen. Envie un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo /usr/share/canaima-semilla/semillero/binary.log")
									md.set_title('Error en construcción')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									pbar.set_text(" ")
									
									check1.set_sensitive(True)
									check2.set_sensitive(True)
									check3.set_sensitive(True)
									check4.set_sensitive(True)
									combo.set_sensitive(True)
									boton_siguiente.set_sensitive(True)
									boton_atras.set_sensitive(True)
									boton_cerrar.set_sensitive(False)								
									
								if systema == 36608:
									pbar.set_fraction(0.0)
									pbar.set_text("IMAGEN CANCELADA")
									timer_2 = gobject.source_remove(timer_1)
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="\tLa construcción de la imagen ISO de\n\tcanaima-"+combo.get_active_text()+" ha sido cancelada.\t")
									md.set_title('Imagen cancelada')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									pbar.set_text(" ")
									
									check1.set_sensitive(True)
									check2.set_sensitive(True)
									check3.set_sensitive(True)
									check4.set_sensitive(True)
									combo.set_sensitive(True)
									boton_siguiente.set_sensitive(True)
									boton_atras.set_sensitive(True)
									boton_cerrar.set_sensitive(False)
									
								#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# USB i386 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#							
							else:
								gtk.gdk.threads_enter()
								md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar alguno de los Sabores existentes   \t")
								md.set_title('Sabores')
								md.run()
								md.destroy()
								gtk.gdk.threads_leave()
									
						if check4.get_active() ==True:
							#-----------------------------Validar opciones de la ventana desplegable-----------------------------------------------------
							if combo.get_active_text():
								
								x= Popen(["arch"], shell=True, stdout=PIPE)
								z = x.stdout.read().split('\n')[0]
								y ="i686"	
								if z == y:
									gtk.gdk.threads_enter()
									md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tEl Sistema  operativo de  su computador  no\t\t \n\tpermite crear Imagenes CD/DVD o USB  con  \n\tarquitectura amd64.\t")
									md.set_title('Error amd64')
									md.run()
									md.destroy()
									gtk.gdk.threads_leave()
									check4.set_active(False)
								else:
									
	
									#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# USB amd64 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
									timer_1 = gobject.timeout_add (100, progres,self)
									pbar.set_text("CONSTRUYENDO IMAGEN")
									
									check1.set_sensitive(False)
									check2.set_sensitive(False)
									check3.set_sensitive(False)
									check4.set_sensitive(False)
									combo.set_sensitive(False)
									boton_siguiente.set_sensitive(False)
									boton_atras.set_sensitive(False)
									boton_cerrar.set_sensitive(True)
									systema = os.system('c-s construir --medio='+usb_1+' --arquitectura='+amd64_1+' --sabor='+combo.get_active_text())
									#~ error= Popen(["echo $?"], shell=True, stdout=PIPE)
									#~ eror = error.stdout.read().split('\n')[0]
									#~ x= "0"
									#~ y= "1"
									#~ z= "130"
									if sytema == 0:
										pbar.set_fraction(1)
										pbar.set_text("FINALIZADO")
										timer_2 = gobject.source_remove(timer_1)
										gtk.gdk.threads_enter()
										md=gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK, message_format="\tSe ha creado una imagen ISO de canaima-"+combo.get_active_text()+".\n\n\tLa imagen ''canaima-"+combo.get_active_text()+"_amd64.usb'' resultante \n\tde los proceso de construcción se encuentra en la \n\tdireccion:\t\n\n\t\t/usr/share/canaima-semilla/semillero/")
										md.set_title('Finalizado')
										md.run()
										md.destroy()
										gtk.gdk.threads_leave()
										pbar.set_text(" ")
										
										check1.set_sensitive(True)
										check2.set_sensitive(True)
										check3.set_sensitive(True)
										check4.set_sensitive(True)
										combo.set_sensitive(True)
										boton_siguiente.set_sensitive(True)
										boton_atras.set_sensitive(True)
										boton_cerrar.set_sensitive(False)
										x= Popen(["nautilus /usr/share/canaima-semilla/semillero/"], shell=True, stdout=PIPE)
										
																			
									if systema == 256:
										pbar.set_fraction(0.0)
										pbar.set_text("ERROR EN CONSTRUCCIÓN")
										timer_2 = gobject.source_remove(timer_1)
										gtk.gdk.threads_enter()
										md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Ocurrio un error durante la generacion de la imagen. Envie un correo a desarrolladores@canaima.softwarelibre.gob.ve con el contenido del archivo /usr/share/canaima-semilla/semillero/binary.log")
										md.set_title('Error en construcción')
										md.run()
										md.destroy()
										gtk.gdk.threads_leave()
										pbar.set_text(" ")
										
										check1.set_sensitive(True)
										check2.set_sensitive(True)
										check3.set_sensitive(True)
										check4.set_sensitive(True)
										combo.set_sensitive(True)
										boton_siguiente.set_sensitive(True)
										boton_atras.set_sensitive(True)
										boton_cerrar.set_sensitive(False)
																		
									if systema == 36608:
										pbar.set_fraction(0.0)
										pbar.set_text("IMAGEN CANCELADA")
										timer_2 = gobject.source_remove(timer_1)
										gtk.gdk.threads_enter()
										md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format="\tLa construcción de la imagen ISO de\n\tcanaima-"+combo.get_active_text()+" ha sido cancelada.\t")
										md.set_title('Imagen cancelada')
										md.run()
										md.destroy()
										gtk.gdk.threads_leave()
										pbar.set_text(" ")
										
										check1.set_sensitive(True)
										check2.set_sensitive(True)
										check3.set_sensitive(True)
										check4.set_sensitive(True)
										combo.set_sensitive(True)
										boton_siguiente.set_sensitive(True)
										boton_atras.set_sensitive(True)
										boton_cerrar.set_sensitive(False)
										
								#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# USB amd64 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
							else:
								gtk.gdk.threads_enter()
								md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tDebe seleccionar alguno de los Sabores existentes  \t")
								md.set_title('Sabores')
								md.run()
								md.destroy()
								gtk.gdk.threads_leave()
				
				else:
					gtk.gdk.threads_enter()
					md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tNo podrá crear la imagen del Sabor porque\t\n\tno posee una conexión a internet.")
					md.set_title('Error en Conexión')
					md.run()
					md.destroy()
					gtk.gdk.threads_leave()
				
				#gtk.gdk.threads_leave()	
		####################################
		
		
		boton_siguiente.connect("clicked", clic_boton)
		boton_siguiente.set_size_request(85, 30)
		caja.pack_start(boton_siguiente, False, False, 0)
		boton_siguiente.show()
		return caja
	
	def make_box1(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		
		separator = gtk.HSeparator()
		caja.pack_start(separator, False, False,70)
		separator.show()
		
		image = gtk.Image()
		image.set_from_file('/usr/share/icons/canaima-iconos/mimetypes/32/application-x-cue.png')
		caja.pack_start(image, False, False,5)
		image.show()
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("<b>CREAR IMAGEN CD/DVD o USB</b>")
		caja.pack_start(descripcion, False, False,0)
		descripcion.show()
		caja.show()
		return caja
	
	def make_box2(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("Para crear una imagen instalable (ISO o IMG) seleccione los siguientes parámetros:")
		caja.pack_start(descripcion, True, False,0)
		descripcion.show()
		caja.show()
		return caja
	
	def make_box3(self, homogeneous, spacing, expand, fill, padding):
		#----------------------------------------- Check Act PAS--------------------------------------------
		def valor1(self, widget, data=None):
			if check1.get_active() == True:
				check2.set_active(False)
			else:
				check2.set_active(True)
							
		def valor2(self, widget, data=None):
			if check2.get_active() == True:
				check1.set_active(False)
			else:
				check1.set_active(True)
		
		caja = gtk.HBox(homogeneous, spacing)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\t1. Seleccione el Medio que desea crear:")
		caja.pack_start(descripcion, True, False,7)
		descripcion.show()	
		
		global check1
		check1 = gtk.CheckButton("CD/DVD")
		check1.set_active(False)
		check1.connect("toggled", valor1,"uno")
		caja.pack_start(check1, True, True,5)
		check1.show()
		
		global check2
		check2 = gtk.CheckButton("USB")
		check2.set_active(False)
		check2.connect("toggled", valor2,"uno")
		caja.pack_start(check2, True, True,5)
		check2.show()
		return caja
	####################################################################
	
	def make_box4(self, homogeneous, spacing, expand, fill, padding):
		#----------------------------------------- Check Act PAS--------------------------------------------
		def valor3(self, widget, data=None):
			if check3.get_active() == True:
				check4.set_active(False)	
			else:
				check4.set_active(True)
					
		def valor4(self, widget, data=None):
			if check4.get_active() == True:
				check3.set_active(False)
			else:
				check3.set_active(True)
		
		caja = gtk.HBox(homogeneous, spacing)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\n\n2. Seleccione la Arquitectura:\n\n")
		caja.pack_start(descripcion, True, True,5)
		descripcion.show()
		
		#~ separator = gtk.HSeparator()
		#~ caja.pack_start(separator, False, False,10)
		#~ separator.show()
		
		global check3
		check3 = gtk.CheckButton("i386")
		check3.set_active(False)
		check3.connect("toggled", valor3,"uno")
		caja.pack_start(check3, False, True,45)
		check3.show()
		
		global check4
		check4 = gtk.CheckButton("amd64")
		check4.set_active(False)
		check4.connect("toggled", valor4,"uno")
		caja.pack_start(check4, False, True,41)
		check4.show()

		caja.show()
		return caja
		
		
		####################################################################
	def actualizar_lista(self):
		global combo
		combo = gtk.combo_box_new_text()
		combo.get_model().clear()
		text = next(os.walk('/usr/share/canaima-semilla/perfiles/'))[1]
		for t in text:
			combo.append_text(t)
	def make_box5(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\t3. Seleccione alguno de los sabores existentes:")
		caja.pack_start(descripcion, False, False,30)
		descripcion.show()

		
		caja.pack_start(combo, True, False,10)
		combo.show()
	
		caja.show()
		return caja
		
	def make_box6(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("\nUna vez haya seleccionado todos los parámetros haga click en el botón Generar.")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, True,5)
		descripcion.show()

		caja.show()
		return caja
	
	def make_box7(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
		
		global pbar
		pbar = gtk.ProgressBar()
		caja.pack_start(pbar, True, True, 10)
		
		pbar.show()
		caja.show()
		return caja
		
	def make_box10(self, homogeneous, spacing, expand, fill, padding):
		caja = gtk.HBox(homogeneous, spacing)
		caja.set_border_width(5)
		
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("Canaima Semilla puede crear imágenes instalables (ISO o IMG)\n basado en los perfiles de sabores existentes. Puede especificársele\n el tipo de Medio, la arquitectura a construir, y el nombre del sabor.")
		descripcion.set_justify(gtk.JUSTIFY_CENTER)
		caja.pack_start(descripcion, True, False,0)
		descripcion.show()

		caja.show()
		return caja
	
	def close(self):
		md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Al cerrar, todos los procedimientos que esten generando la ISO'S serán eliminados.\n\n\t¿Desea salir de la aplicación?")
		md.set_title('Cerrar')
		respuesta = md.run()
		md.destroy()
		
		if respuesta == gtk.RESPONSE_YES:
			x2= Popen(["pkill lb"], shell=True, stdout=PIPE)
			x3= Popen(["pkill live-build"], shell=True, stdout=PIPE)
			x1= Popen(["pkill c-s"], shell=True, stdout=PIPE)
			self.window.destroy()
			gtk.main_quit()
	
	def on_delete(self, widget, data=None):
		return not self.close()
	
	def __init__(self):
		self.window1 = gtk.Window()
		self.window1.set_border_width(0)
		self.window1.set_title("Crear ISO'S")
		self.window1.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window1.set_size_request(600, 600)
		self.window1.set_resizable(False)
		self.window1.connect("destroy", gtk.main_quit)
		self.window1.connect("delete_event", self.on_delete)
		#self.window1.set_icon_from_file('/usr/share/icons/canaima-iconos/apps/48/c-s.png')

		self.actualizar_lista()
		
		self.vbox = gtk.VBox(False, 10)
		
		self.box2 = self.make_imag1(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box1(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 5)
		self.box2.show()
		
		self.separator = gtk.HSeparator()
		self.vbox.pack_start(self.separator, False, False, 0)
		self.separator.show()
		
		self.box2 = self.make_box10(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 5)
		self.box2.show()
		
		self.box2 = self.make_box2(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 5)
		self.box2.show()
		
		self.box2 = self.make_box3(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box4(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box5(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box6(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.box2 = self.make_box7(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, True, True, 0)
		self.box2.show()
		
		self.separator = gtk.HSeparator()
		self.vbox.pack_start(self.separator, False, False, 0)
		self.separator.show()
		
		self.box2 = self.make_botones(False, 0, False, False,0)
		self.vbox.pack_start(self.box2, False, False, 0)
		self.box2.show()
		
		self.window1.add(self.vbox)
		self.window1.show_all()
#-------------------------------ventana 1---------------------------  
if __name__ == "__main__":
	app = construir_isos()
	gtk.main()
