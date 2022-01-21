#!/usr/bin/python
#coding: utf8

"""
Imports
"""
import time
from math import cos,sin
import serial

"""
Imports de Teclado
"""
import os
import sys, tty, termios
from select import select

# To import the function "envia" from the file "test_NeatoCommands.py"
from test_NeatoCommands import envia

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:

        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:

        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	print ch
    return ch



# Llamada a la funcion main
if __name__ == '__main__':

	global ser
	# Open the Serial Port.
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.05)

	envia(ser,'TestMode On', 0.2)

	envia(ser, 'Clean', 0.2)

	envia(ser,'PlaySound 1', 0.3)

	envia(ser,'SetMotor RWheelEnable LWheelEnable', 0.2)

	# Parametros Robot.
	S = 121.5		# en mm
	distancia_L = 0	# en mm
	distancia_R = 0	# en mm
	speed = 0 		# en mm/s
	tita_dot = 0
	tiempo = 20
	direccion = 0
	CI = [0,0,0] #[x, y, tita], estas condiciones iniciales variaran en clase 
	delta_d = 0
	delta_t = 0
	L_k = 0
	R_k = 0

	print "########################"
	print "Speed = " + str(speed)
	print "Tita_dot = " + str(tita_dot)

	if direccion == 0:
		print "Direction: fordward."
	else:
		print "Direction: backward."

	print "q to exit."
	print "########################"

	# Tecla a leer.
	tecla = ''
	comando = ''

	while tecla != "q":

		aux = envia(ser, 'GetMotors LeftWheel RightWheel')
		
		lines = aux.split("\n")
		lines = list(map(lambda v: v.split(','), lines))

		L_k1 = float(lines[4][1])
		R_k1 = float(lines[8][1])

		dL = L_k1 - L_k
		dR = R_k1 - R_k

		L_k = L_k1
		R_k = R_k1

        #ODOMETRIA

		delta_d = (R_k + L_k) / 2
		delta_t = (R_k - L_k) / (2*S)
        
        #POSE_INTEGRATION
        
		CI = [CI[0] + delta_d * cos(CI[2]), CI[1] * delta_d * sin(CI[2]), CI[2] + delta_t]

		print "X: "+ str(CI[0])
		print "Y: "+ str(CI[1])
		print "tita: " + str(CI[2])

		# Leemos la tecla.
		print "Write command: "
		tecla = getch()

		if tecla == '8' or tecla == '2':

			if tecla == '8':
				speed = speed + 50
			else:
				speed = speed - 50

			if speed >= 0:
				direccion = 0
			else:
				direccion = 1

			if speed == 0:

				envia(ser,'SetMotor LWheelDisable RWheelDisable', 0.2)
				envia(ser,'SetMotor RWheelEnable LWheelEnable', 0.2)

			else:
				distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion) #A rellenar la fórmula 
				distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion) #A rellenar la fórmula 

				comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(speed * pow(-1, direccion))
				envia(ser,comando, 0.2)

		elif tecla == '4' or tecla == '6':

			if tecla == '4':
				tita_dot = tita_dot + (3.1415/10)
			else:
				tita_dot = tita_dot - (3.1415/10)

			distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
			distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)

			comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(speed * pow(-1, direccion))
			envia(ser,comando, 0.2)

		elif tecla == '5':

			direccion = 0
			speed = 0
			tita_dot = 0
			distancia_L = 0
			distancia_R = 0

			envia(ser,'SetMotor LWheelDisable RWheelDisable', 0.2)
			envia(ser,'SetMotor RWheelEnable LWheelEnable', 0.2)
		
		elif tecla == '1' or tecla == '3':

			if tecla == '1':
				distancia_R = 1000 * tiempo
				
				distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
				distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)
			
				distancia_L = -distancia_R
				
				if speed == 0:
					speed = 50

				comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(speed * pow(-1, direccion))
				envia(ser,comando, 0.2)
				
			else:
				distancia_R = -1000 * tiempo
				
				distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
				distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)
			
				distancia_R = -distancia_L
				
				if speed == 0:
					speed = 50

				comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(speed * pow(-1, direccion))
				envia(ser,comando, 0.2)

		if tecla == '8' or tecla == '2' or tecla == '6' or tecla == '4' or tecla == '5' or tecla == '1' or tecla == '3':


			#print "\n########################"
			#print 'Comando enviado: ' + comando
			print "########################"
			print "########################"
			print "Speed = " + str(speed)
			print "Tita_dot = " + str(tita_dot)

			if direccion == 0:
				print "Direction: fordward."
			else:
				print "Direction: backward."
			print "########################"
