from time import sleep
import serial
import time
from pyA20.gpio import gpio
from pyA20.gpio import port
from pyA20.gpio import connector

ares = port.PA2          #Pin for Arduino reset
gpio.init()
gpio.setcfg(ares, gpio.OUTPUT)
gpio.output(ares, 0)


buffer_in = [None] * 5   #Empty buffer for incoming message
buffer_out = [None] * 5  #Empty buffer for outcoming message
bufferSize = 5		 #Frame of 5  bytes
readCounter = 0
isHeader = 0

header = 0x7E		 #First byte in frame
connection = False

ser = serial.Serial(port = "/dev/ttyS1", baudrate=9600)
ser.close()
ser.open()

def acceptmessage_from_UART():
    global buffer_in
    firstTimeHeader = 0
    isHeader = 0
    readCounter = 0
    while (ser.inWaiting()>0):
	c = ord(ser.read(size=1))	#Read 1 byte from serial and convert to integer
	if (c == header):
	    if(firstTimeHeader == 0):
		isHeader = 1
		readCounter = 0
		firstTimeHeader = 1
	buffer_in[readCounter] = c
	readCounter += 1
	if (readCounter >= bufferSize):
	    readCounter = 0
	    if (isHeader):
		checksumValue = buffer_in[4]		#Read the value of checksum from arduino side
		if (verifyChecksum(checksumValue)):     #Recalculate checksum on OrangePi and compare
		    check_incoming_message()
		else:
		    print "Message is corrupted"
		isHeader = 0
		firstTimeHeader = 0

def check_incoming_message():		#Perform a command in accordance with incoming message
    global buffer_in
    global connection
    print "Incoming message: ", buffer_in
    if (buffer_in[1] == 0x50):
	print "Connection with arduino is done"
	connection = True
	send_to_UART(0x51, 0x00, 0x00)  #Prove to arduino that connection is done

    elif (buffer_in[1] == 0x35):
	print "Movement is detected"

    elif (buffer_in[1] == 0x38):
	print "Highlighted "

    else:
	print "Unknown command"
    buffer_in = [None] * 5		#Clear input buffer

def verifyChecksum(originalResult):	#Calculate checksum of incoming message
    result = 0
    sum = 0
    b = 0
    for b in range(bufferSize - 1):
	sum = sum + buffer_in[b]
    result = sum
    if (originalResult == result):	#Compare it with the value from arduino
	return 1
    else:
	return 0

def send_to_UART(code, par1, par2):	#Create outgoing message
    global buffer_out
    buffer_out[0] = header
    buffer_out[1] = code
    buffer_out[2] = par1
    buffer_out[3] = par2
    buffer_out[4] = checksum()
    m = 0
    for m in range(bufferSize):
	ser.write(chr(buffer_out[m]))	#Write 5 bytes (frame) to serial
    print "Outgoing message: ", buffer_out
    buffer_out = [None] * 5		#Clear output buffer

def checksum():				#Calculate checksum for outgoing message
    result_out = 0
    sum_out = 0
    p=0
    for p in range(bufferSize - 1):
	sum_out = sum_out + buffer_out[p]
    result_out = sum_out & 0xFF
    return result_out

def waitforConnection():		#function that is trying to establish the connection with Arduino
    if ser.isOpen():
        if (ser.inWaiting() == 0):                      #If there is no message from Arduino
            while (ser.inWaiting() == 0):               #Wait till the first message
                print "I'm waiting for connection message from arduino"
        else:
            while (connection == False):		#Wait for connection request from arduino
		if (ser.inWaiting() > 0):
		    while (ser.inWaiting() > 0):
			acceptmessage_from_UART()

def connect_to_arduino():
    #Restart arduino
    gpio.output(ares, 1)
    sleep(0.7)
    gpio.output(ares, 0)
    sleep(3)
    #Connect to Arduino
    try:
        if ser.isOpen():
            waitforConnection()
    except:
        while (ser.isOpen == False):
            pass
        waitforConnection()


connect_to_arduino()

#When the connection is done, start main loop
while(1):
    if ser.isOpen():
	if (ser.inWaiting()>0):
	    acceptmessage_from_UART()
    	else:
	    try:
		code1 = input("Type code: ")
		print code1
		param2 = 0
		if (code1 == 0x24 or code1 == 0x30):
		    param2 = input("Type param2: ")
		    print param2
	        send_to_UART(code1, 0x00, param2)
	    except: 
		pass
