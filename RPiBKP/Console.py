import serial
import RPi.GPIO as GPIO
import os, time
import binascii
from curses import ascii

GPIO.setmode(GPIO.BOARD)


# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)
port.reset_input_buffer()
port.reset_output_buffer()



def msgDel(n):
	port.write('AT+CMGD=' + str(n) + '\r\n')
	portRead()

def msgRead(n):
	
	port.write('AT+CMGF=1\r\n')  # Set SMS mode [0,1]  [PDU, TEXT]
	portRead()
	port.write('AT+CPMS="SM"\r\n')
	portRead()
	port.write('AT+CMGR=' + str(n) + '\r\n')  # 1 is user input *VAR*
	time.sleep(0.5)
	msg = portRead()
	time.sleep(0.5)
	if 'heysexywhereareyou?' in msg:
		port.write('AT+CGNSPWR=1\r\n')
                portRead()
		time.sleep(20)
                port.write('AT+CGNSINF\r\n')
                msg = portRead()
                print msg.split(',')[3]  # lat
                print '\n'
                print msg.split(',')[4]  # long
		time.sleep(2)
		port.write('AT+CGNSPWR=0\r\n')
                portRead()
	#if 'AT+' in msg:
	#	print 'THERE IS'


def msgSend(lat, lon):
	port.write('AT+CSCA="+3097100000"\r\n')  # SMS Center (Cosmote) *VAR*
        portRead()
        port.write('AT+CMGF=1\r\n')
        portRead()
        port.write('AT+CMGS="+306983413353"\r\n')  # Target Number
        portRead()
        port.write('Coords' + lat + '\t' + lon)
        port.write('\x1A\r\n')  # \x1A is CTRL+Z  ** \r\n is required **
        time.sleep(5)
	portRead()

def msgStore():
	port.write('AT+CMGF=1\r\n')
	portRead()
	port.write('AT+CPMS="SM", "SM"\r\n')
	portRead()
	port.write('AT+CSCA="+3097100000"\r\n')
	portRead()
	port.write('AT+CMGW="+306983413353",145,"STO UNSENT"\r\n')
	portRead()
	time.sleep(1)
	portRead()
	port.write('atcheck')
	port.write('\x1A\r\n')
	time.sleep(1)
	portRead()

def portRead():
	rc = ''
	time.sleep(0.5)
	while port.inWaiting() > 0:
        	rc += port.read(1)
	print rc
	return rc

while 1 :
	cmd = raw_input(">> ")
	
	if cmd == 'exit':
		port.close()
		exit()
	elif cmd == 'SMS':
		msgSend()
	elif cmd == 'STOR':
		msgStore()
	elif 'LOOK' in cmd:
		num = int(''.join(filter(str.isdigit, cmd)))  # Extract number
		msgRead(num)
	elif 'DEL' in cmd:
		num = int(''.join(filter(str.isdigit, cmd)))
		msgDel(num)
	elif cmd == 'GPON':
		port.write('AT+CGNSPWR=1\r\n')
		portRead()
	elif cmd == 'GPOFF':
		port.write('AT+CGNSPWR=0\r\n')
		portRead()
	elif cmd == 'LOC':
		port.write('AT+CGNSINF\r\n')
		msg = portRead()
		print msg.split(',')[3]  # lat
		print '\n'
		print msg.split(',')[4]  # long
	elif cmd == 'PWROFF':
		port.write('AT+CPOWD=1\r\n')
		portRead()
	else:
		port.write(cmd + '\r\n')
		rcv = ''

		time.sleep(0.5)

		while port.inWaiting() > 0:
			rcv += port.read(1)

		print rcv
		if rcv != '':
			print ">>" + rcv

		port.reset_input_buffer()
		port.reset_output_buffer()
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
#port.write(cmd+'\r\n')
#rcv = port.read(10)
#time.sleep(.2)
#print rcv
#time.sleep(1)
#port.close()

