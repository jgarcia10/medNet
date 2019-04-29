from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse
from django.http import Http404
import simplejson as json
import time
import socket
import threading


global LISTA_ACTIVIDADES, LISTA_LINKS, actividadActual
LISTA_ACTIVIDADES = ['Comiendo', 'Rumiando', 'Tomando Agua', 'Durmiendo', 'Caminando', 'Nada']
LISTA_LINKS = ['comiendo.png', 'rumia.png', 'agua.png', 'durmiendo.png', 'caminando.png', 'nada.png']
actividadActual = 5

global tiempoInicio
tiempoInicio = time.time()

global cosa, PosX, PosY, PosZ, Acc_x, Acc_y, Acc_z

cosa = []
PosX = []
PosY = []
PosZ = []
Acc_x = 0
Acc_y = 0
Acc_z = 0

def ThreadActualizarSocket():
	global cosa, PosX, PosY, PosZ, Acc_x, Acc_y, Acc_z
	
	s = socket.socket()
	s.bind(("192.168.137.1", 9001))
	s.listen(10)
	print("Binding completed")

	c, adrr = s.accept()
	print("Incoming connection from:"+str(adrr))


	while True:
		data = c.recv(1024)
		if data:

			mensajeRecibido = data.decode()
			reciveArray = mensajeRecibido.split("\r\n")
			for i in range(0,len(reciveArray)): cosa.append(reciveArray[i].split("#"))
			if len(cosa) > 4:
				for i in range(0,len(cosa)):
					if len(cosa[i]) == 4:
						PosX.append(cosa[i][1])
						PosY.append(cosa[i][2])
						PosZ.append(cosa[i][3])
			
		else: break

	c.close()

threading.Thread(target=ThreadActualizarSocket).start()


def index(request):
	global LISTA_ACTIVIDADES

	return render(request, 'index.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS), 'ACTUAL':actividadActual})


def actualizar_estado(request):

	global actividadActual

	actividadActual = int(request.POST['estado'])

	return HttpResponse(str(actividadActual))

def server(request):

	global actividadActual, LISTA_ACTIVIDADES, LISTA_LINKS

	return render(request, 'server.html', {'Actividad':LISTA_ACTIVIDADES[actividadActual], 'Imagen': LISTA_LINKS[actividadActual]})

def actualizarServer(request):

	global actividadActual, LISTA_ACTIVIDADES, LISTA_LINKS, tiempoInicio, Acc_x, Acc_y, Acc_z

	respuesta = {}

	respuesta['texto'] = LISTA_ACTIVIDADES[actividadActual]
	respuesta['imagen'] = LISTA_LINKS[actividadActual]
	respuesta['Acc_x'] = Acc_x
	respuesta['Acc_y'] = Acc_y
	respuesta['Acc_z'] = Acc_z
	respuesta['tiempo'] = time.time()-tiempoInicio

	return HttpResponse(json.dumps(respuesta))