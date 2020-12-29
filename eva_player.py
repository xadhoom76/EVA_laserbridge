#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
# AUTHOR XADHOOM76
# Bolgia Alessandro

#!/usr/bin/python
### CONVERSIONE PER LDV1000 a pioneer o lasermax  raspberry vlc HW
##
## Gestire mute unmute
# finire comandi Sony 
# fare comandi philips
# Argomenti di settaggio a linea di comando

import time
import string
import serial
import sys
import select
import threading
#import parallel

#171 fino a 1206 Presentazione
#fine 31496

import requests
import urllib
import xml.etree.ElementTree as ET
import os

audio = 0

length = float(31496*25)  # Video 


def to_pioneer(ser,data):
	ser.write(data)
def to_sony(ser,data):
	ser.write(data)
# PCB - LETTORE
# PHILIPS 
#FX XX XX	goto Frame #XXXXX & play forward	1    SE LA R in fondo e' STILL
#DX XX XX	goto Frame #XXXXX & halt (first field)	1
#00 00 --	play forward	1
#00 10 --	play reverse	1
#00 20 --	halt (frame)	1
#00 30 --	reserved	
#00 4X XX	slow forward @ XXX speed parameter	1
#00 5X XX	slow reverse @ XXX speed parameter	1
#00 60 --	reserved	
#00 70 --	reserved	
#00 80 --	reserved	
#00 90 --	reserved	
#00 A0 --	scan forward @ 75 times normal speed	2
#00 B0 --	scan reverse @ 75 times normal speed	2
#00 C0 --	reserved	
#00 D0 --	reserved	
#00 EX XX	jump immediately XXX tracks forward	2
#00 FX XX	jump immediately XXX tracks reverse	2
#02 MM NN	Video Audio-I Audio-II CX controls	2
#method for reading incoming bytes on serial

def read_serial_from_philips(ser):
     buf = ''
     inp = ser.read(size=1) #read a byte
#[     inp = ser.readline() #read a byte
        #leggo un byte
     buf = inp #accumalate the response
     data=inp.encode("hex")
#     print data + " : " + inp 

#     if str(inp) <>"":
#	     print inp      

#        print "debug: " + data
#     if ("00" == inp):
#            ser02.setDTR(True)
#	    print "ext"



  
     if ("N" == inp):
	    print "N primo"
   	    vlc.play()
	    ser.write("A")
	    ser.write("1")
            ser.write("\r")
     if ("X" == inp):
	    print "X primo"
   	    vlc.play()
	    ser.write("A")
	    ser.write("0")
            ser.write("\r")
     if ("R" == inp):
	    print "R primo"
   	    vlc.pause()
	    time.sleep(0.05)
	    ser.write("A")
	    ser.write("0")
            ser.write("\r")


     if ("A" == inp ) or ( "B" == inp ):
		buf = ser.read(size=1)
		if buf=="1":
			print "audio on"
			vlc.set_volume(0)
		else:
			print "audio off"
			vlc.set_volume(314)
	        ser.write("A")
                ser.write("0")
                ser.write(chr(0xa))

     if "F" == inp:
	    x=4
	    frame=0
	    while True :
		    buf = ser.read(size=1) #read a byte
#		    if buf<>"":
#			    print buf.encode("hex") + " : " + str(buf) + " : "+ str(x) 
		    
#		    print buf
		#    try:
		    if (x>=0) and (str(buf) <> "R") and (str(buf) <>"") and ( str(buf) <> "N" ) and ( buf<>"P"):
			   # print int(buf)
			    byte = buf.encode("hex")
			    byte = int(byte)
			    byte = ( byte - 30 )*(10**x)
#			    print byte # 8 66 60  | 1 6 6
#			    print str(byte) + " " + str(x)
			    frame = int(frame) + int(byte) 
			    x=x-1
#			    print "--Seek frame--- " + str(frame)


		    elif str(buf) == "R":
                        time.sleep(0.02)
 		        vlc.seek(frame)
		        vlc.pause()
			vlc.set_volume(0)
                        time.sleep(0.50)
   		        ser.write("A")
		        ser.write("0")
		        ser.write("\r")
#			print "exit" STILL
			break 
		    elif str(buf) == "N":
 		        vlc.seek(frame)
                        time.sleep(0.02)
		        vlc.play()
			vlc.set_volume(314)
                        time.sleep(0.55) # IMPORTANTE
   		        ser.write("A")
		        ser.write("1")
		        ser.write("\r")
#                        time.sleep(0.01) # IMPORTANTE

			break
	#	    except:
	#		print "eccezione"
	#		sys.exit(0)




# FIXME
#00 00 00 08 00 00
#	    ser.write(chr(0x00))
#	    ser.write(chr(0x00))
#	    ser.write(chr(0x00))
#	    ser.write(chr(0x08))
#	    ser.write(chr(0x00))
#	    ser.write(chr(0x00))

#	    ser.write("A0")
#	    ser.write(chr(0x05))
#	    ser.write(chr(0x00))
#	    ser.write(chr(0x00))
#	    ser.write(chr(0x0))

#	    ser.write(chr(0xa))


#--Seek frame--- 166
#0d : 
#41 : A
#30 : 0
#0d : 
#42 : B
#30 : 0
#0d : 
#4e : N
#0d : 



def read_serial_from_pioneer(pcb,audio):
        buf = ''
        num=''

#    while True:
        inp = pcb.readline().strip() #read fino a CR
	command = inp[-2:]
	addr=inp[:len(inp)-2]
	inp=command
        if "CL" == inp: ## CLEAR
	    pcb.write("R\r")
#	    print inp
	    buf=1 
            print "risponde ok "
        if "R" == inp: ## Messaggio di completamento comando
#  	    print inp
	    pcb.write("R\r") 
        if "1XXXX" == inp: ## Messaggio di completamento comando
#80 00 11 00 20
	    print inp
#	    print " fine status"
        if "10000" == inp: ## Messaggio di completamento comando
	    print inp
	   # sony.write(chr(0x80)) 
	   # sony.write(chr(0x00)) 
	   # sony.write(chr(0x11)) 
	   # sony.write(chr(0x00)) 
	   # sony.write(chr(0x20)) 
#	    print " fine status"
	if "OP" == inp:
	    print inp
	    pcb.write("R\r") 
	    buf=1 # DOOR OPEN
        if "CO" == inp: 
	    print inp
	    pcb.write("R\r") 
            buf=1 # DOOR CLOSE
        if "RJ" == inp: 
	    print inp
	    pcb.write("R\r") 
            buf=1 # REJECT
        if "SA" == inp: 
	    print inp
	    pcb.write("R\r") 
            buf=1 # START
        if "SE" in inp: ## Address Search

#	    print inp	
#	    vlc.seek(int(5))

	    time.sleep(0.02)  # RITARDO DEL PLAY, USCITA FILMATO

	    vlc.seek(int(addr))
	    vlc.play_pause()
	    time.sleep(dsearch)
	    pcb.write("R\r") 
        if "PL" == inp: 
	    vlc.play()
	    time.sleep(0.3) #### IMPORTANTE PER NON VEDERE FRAME PRECEDENTI
	    pcb.write("R\r") 
	    buf=1 #PLAY  address play
        if "PA" == inp: 
	    pcb.write("R\n") 
	    vlc.play_pause()
	    print inp
	    buf=1 #PAUSE
        if "ST" == inp: 
	    pcb.write("R\n") 
	    print inp
	    buf=1 #STILL
        if "SF" == inp: 
	    pcb.write("R\n") 
	    print inp
	    buf=1 #STEP FWD
        if "SR" == inp: 
	    pcb.write("R\n") 
	    print inp
	    buf=1 #STEP REV
        if "NF" == inp: ## Scan FWD
	    pcb.write("R\n") 
	    print inp
	    buf=1 
        if "NR" == inp: ## Scan REV
	    pcb.write("R\n") 
	    print inp
	    buf=1 
        if "MF" == inp: ## Address Multi speed fwd
	    pcb.write("R\n") 
	    print inp
	    buf=1 
        if "MR" == inp: ## Address Multi speed rev
	    pcb.write("R\n") 
	    print inp
	    buf=1 #
        if "SP" == inp: ## Integer SPEED SET
	    pcb.write("R\n") 
	    print inp
	    buf=1 
        if "JF" == inp: ## Integer Multi track Jump Fwd
	    pcb.write("R\n") 
	    print inp
	    buf=1 
        if "JR" == inp: ## Integer Multi track Jump rev
	    print inp
	    buf=1 
        if "SM" == inp: ## Address Stop Marker
	    print inp
	    buf=1 
        if "FR" == inp: ## FRAME SET
	    print inp
	    buf=1 
        if "TM" == inp: ## Time set
	    print inp
	    buf=1 
        if "CH" == inp: ## Chapter Set
	    print inp
	    buf=1 
        if "LO" == inp: ## Lead-Out symbol
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "AD" == inp: ## integer Audio control
	 #   print inp
	    global flag_audio
	    if flag_audio==1:
		 #   print " mute "	      
		    vlc.set_volume(0)
		    flag_audio=0
	    else:
		 #   print " unmute "
		    vlc.set_volume(100)
	            flag_audio=1
	    pcb.write("R\r")
	    
        if "VD" == inp: ## integer Video control
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "KL" == inp: ## integer KEYLOCK
	    print inp
	    time.sleep(0.5)
	    pcb.write("R\r")
	    buf=1 
        if "DS" == inp: ## integer Display Control
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "CS" == inp: ## Clear Screen
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "PR" == inp: ## integer Print character
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?F" == inp: ## Frame number request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?T" == inp: ## Time Code Request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?C" == inp: ## Chapter number request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?P" == inp: ## Player active mode request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?D" == inp: ## Disc Status request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?X" == inp: ## LPD model request
	    print inp
	    time.sleep(0.5)
            pcb.write("P151601\r")
	    
	    buf=1 
        if "?U" == inp: ## PIONEER USER CODE REQUEST
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?Y" == inp: ## STANDARD USER CODE REQUEST
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?S" == inp: ## TELEVISION SYSTEM REQUEST
	    print inp
	    buf=1 
        if "CM" == inp: ## integer Communicacation control
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "?M" == inp: ## CCR MODE REQUEST
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "RA" == inp: ## Integer RA registeer A set ( DISPLAY )
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "RB" == inp: ## Integer RB register B set ( squelch )
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "RC" == inp: ## Integer RC register C set ( Misc )
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "RD" == inp: ## Integer RD register D set ( rs-232 )
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "$A" == inp: ## Register A request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "$B" == inp: ## Register B request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "$C" == inp: ## Register B request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "$D" == inp: ## Register D request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "#I" == inp: ## Input Unit request
	    print inp
	    pcb.write("R\r")
	    buf=1 
        if "E" in inp: ## Errore e segue il codice di errore
#	    print inp
#	    print addr
	    pcb.write("R\r")
	    print " ERROR "
# DA SISTEMARE	    sony.write(chr(0x02)) 
	    #sony.write(chr(0x02)) 
	else:
	    "Non riconosciuto pioneer"
	    buf=num

	    if inp<>"":
		    print inp

    #print " FINE PIONEER"
#    return buf

#method for reading incoming bytes on serial
def read_serial_from_sony(ser):
     buf = ''
#    print "Reading from " + ser.port
 #   while True:
     inp = ser.read(size=1) #read a byte
	#leggo un byte
#	print inp	
#        print inp.encode("hex") #gives me the correct bytes, each on a newline
#        print inp.decode("hex") #gives me the correct bytes, each on a newline
     buf = buf + inp #accumalate the response
     if "01" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # Completato, corrisponde al R del pioneer
#	    print "0x01"
     if "02" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
 #           pio.write("ER\n")# ERRORE RS232 # ERROR
#	    print "0x02"
     if "03" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # Aperto ( non e' un comando solo stato )
	    print "0x03"
     if "05" == inp.encode("hex"): 
	    print "0x05"
            buf=1 # Target frame non trovato
     if "06" == inp.encode("hex"): 
	    print "0x06"

            buf=1 # Target frame illegale
     if "07" == inp.encode("hex"): 
	    print "0x07"
            buf=1 # Mark return - Mark set position found
     if "0A" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # OK
     if "0B" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # No OK
     if "24" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("1AD\n") # Audio Mute ON
#	    read_serial_from_pioneer(pio,ser)
     if "25" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
 #           pio.write("0AD\n") # Audio Mute OFF
#	    read_serial_from_pioneer(pio,ser)
     if "26" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # Video Off
     if "27" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # Video On
     if "28" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # PCS ENABLE
     if "29" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # PCS DISABLE
     if "2a" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("RJ\n") # EJECT
#	    read_serial_from_pioneer(pio,ser)
     if "2b" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
 #           pio.write("SF\n") # FWD STEP and STILL
#	    read_serial_from_pioneer(pio,ser)
     if "2c" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("SR\n") # RW STEP and STILL
#	    read_serial_from_pioneer(pio,ser)
     if "2d" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
 #           pio.write("JF\n") # FWD RELATIVE SEARCH
#	    read_serial_from_pioneer(pio,ser)
     if "2e" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
 #           pio.write("JR\n") # REW RELATIVE SEARCH
#	    read_serial_from_pioneer(pio,ser)
     if "30" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=0 # FW STEP and STILL
     if "31" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # FW STEP and STILL
     if "32" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=2 # FW STEP and STILL
     if "33" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=3 # FW STEP and STILL
     if "34" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=4 # FW STEP and STILL
     if "35" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=5 # FW STEP and STILL
     if "36" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=6 # FW STEP and STILL
     if "37" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=7 # FW STEP and STILL
     if "38" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=8 # FW STEP and STILL
     if "39" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=9 # FW STEP and STILL
     if "3a" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
	    vlc.play()
            ser.write(chr(0x0a)) ## DO OK AD OGNI BYTE RICEVUTO
            buf=1 # PLAY
     if "3b" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("02MF\n") # FAST PLAY
     if "3c" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 #SLOW PLAY
     if "3d" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # VARIABLE SPEED PLAY
     if "3e" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("NF\r") # SCAN FWD
#	    read_serial_from_pioneer(pio,ser)
     if "3f" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
	    vlc.pause()
 #            print " PIONEER STOP "
#	    pio.write("ST\r") # STOP
#	    read_serial_from_pioneer(pio,ser)
#            ser.write(chr(0x0A))
     if "40" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("\r") # ENTER - Terminate a command
# 	    read_serial_from_pioneer(pio,ser)
     if "41" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("CL\r") # CLEAR NUMERI ENTRY
# 	    read_serial_from_pioneer(pio,ser)
     if "42" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # GO to beginning of program area
     if "43" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
	    ser.write(chr(0x0a))
### VAI AL FRAME XXXXX
#	    pio.readline()
	    pio_frame=''
	    x=1
	    while True :
		frame=ser.read(size=1)
		if frame <> '':
			if frame.encode("hex") == "40":
				break 
		#	print frame
		        #print ( "ciclo" + chr(x+48))
				
	        	num=frame.encode("hex")
		#	print num
	    	
			ser.write(chr(0x0A)) ## DO OK AD OGNI BYTE RICEVUTO
		 	num=string.atoi(num)
#			print num
			num=num+18 # I NUMERI PARTONO DA 0x30
# DEVO CONVERTIRE I BYTE IN NUMERI ASCII
			pio_frame = pio_frame + chr(num)
		#	print "er02"
			#pio_frame=pio_frame + (num-30)*10^x	    
		 #       print pio_frame
            #print ("EXIT")
#            frame=ser.read(size=1) # leggo enter 0x40 # FINE ENCODING del frame
#	    print frame.encode("hex")
	    ser.write(chr(0x0a)) # OK letto
#	    print "----FRAME: "
#	    print pio_frame+"SE\r"
            vlc.seek(int(pio_frame))
	    vlc.play_pause()
#	    pio.write(pio_frame+"SE\r") # INVIO IL COMANDO DI VAI AL FRAME XXXXXSE
#            pio.write("SE\r") # SEARCH ## INVERTIRE IL COMANDO PER IL PIONEER
	    ser.write(chr(0x01)) # FRAME TROVATO
	    #LEGGERe 5 BYTE ed inviare a Pioneer

     if "44" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # REPEAT
     if "46" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            ser.write(chr(0x0A))
#            pio.write("1AD\r") # AUDIO CHANNEL 1 ON
     if "47" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            print " attivo audio pioneer"
            ser.write(chr(0x0A))
#	    pio.write("0AD\r") # AUDIO CHANNEL 1 OFF
#	    pio.write("PL\r") # AUDIO CHANNEL 1 OFF
     if "48" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("1AD\r") # AUDIO CHANNEL 1 ON
            ser.write(chr(0x0A))
            #pio.write("PL\r") # AUDIO CHANNEL 1 ON
     if "49" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("0AD\r") # AUDIO CHANNEL 2 OFF
            ser.write(chr(0x0A))
     if "4a" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # REW PLAY
     if "4b" == inp.encode("hex"): 
            #pio.write("02MR\r") # REW FAST
            print inp.encode("hex") #gives me the correct bytes, each on a newline
# 	    read_serial_from_pioneer(pio,ser)
     if "4c" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # REW SLOW
 	    #read_serial_from_pioneer(pio,ser)
     if "4d" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # REV STEP
     if "4e" == inp.encode("hex"): 
#            pio.write("NR\r") # # REV SCAN
            print inp.encode("hex") #gives me the correct bytes, each on a newline
# 	    read_serial_from_pioneer(pio,ser)
     if "4f" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
#            pio.write("ST\r") # STILL
# 	    read_serial_from_pioneer(pio,ser)
     if "50" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # INDEX ON 
     if "51" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            ser.write(chr(0x0A))
#	    buf=1 # INDEX OFF
     if "55" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            #pio.write("FR\r") # FRAME MODE
# 	    read_serial_from_pioneer(pio,ser)
     if "56" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            #pio.write("CL\r") # CLEAR ALL
 #	    read_serial_from_pioneer(pio,ser)
     if "5a" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # MEMORY set
     if "5b" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # MEMORY SEARCH
     if "60" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            #pio.write("?F\r") # INQUIRY FOR CURRENT ADDRESS
	    #result=pio.readline()
         
	 ## 02047 cr
	    x=5
	    #for x>=1:
	#	byte=hex(ord(result[x]))
	 #       print result[x] # CODIFICARE PIONNER 
### frame 
	  #      ser.write(byte)
	#	x=x-1
     if "61" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
        #    pio.write("PL\r") # CONTINUE
 	#    read_serial_from_pioneer(pio,ser)
     if "62" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
        #    pio.write("PL\r") # MOTOR ON
 	#    read_serial_from_pioneer(pio,ser)
     if "63" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
        #    pio.write("PA\r") # MOTOR OFF
 	#    read_serial_from_pioneer(pio,ser)
     if "67" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
        #    pio.write("?D\r") # INQUIRY STATUS ( 5 bytes return )
	#    ser.write(chr(0x80)) 
	#    ser.write(chr(0x00)) 
	#    ser.write(chr(0x11)) 
	#    ser.write(chr(0x00)) 
	#    ser.write(chr(0x20)) 
     if "69" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
        #    pio.write("CH\r") # set CHAPTER MODE
 	#    read_serial_from_pioneer(pio,ser)
     if "6e" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # CX ON
     if "6f" == inp.encode("hex"): 
            buf=1 # CX OFF
            print inp.encode("hex") #gives me the correct bytes, each on a newline
     if "71" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # NON CF PLAY
     if "72" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # INQUIRY RON VERSION
     if "73" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # MARK SET
     if "74" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # EJECT ENABLE
     if "75" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # EJECT DISABLE
     if "76" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
         #   pio.write("?C\r") # INQUIRY CHAPTER
 	 #   read_serial_from_pioneer(pio,ser)
     if "79" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # USER INQUIRY
     if "80" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # USER INDEX CONTROL
     if "81" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # USER INDEX ON
     if "82" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # USER INDEX OFF
     if "8f" == inp.encode("hex"): 
            print inp.encode("hex") #gives me the correct bytes, each on a newline
            buf=1 # DEVICE TYPE INQUIRY
     else:
	    if inp<>"":
		    print inp.encode("hex")
		    print inp
	#	    print inp.decode("hex")
		    print " NON RICONOOSCIUTO"
#    return buf   






class vlc_http:

	SEEK_CUR = 0
	SEEK_BEGIN = 0
	
	port = 8080		# Port on which player interface exists
	sec_percentage = 0 	# Each second represents how much percentage of the media

	def __init__(self, port=8080):
		self.port = port

		# Check if VLC localhost page is accessible or not
		try:
			page = requests.get('http://localhost:'+str(self.port))
		except:
			raise Exception("There was a problem connecting with VLC localhost control. \
					Make sure that VLC is running and port address is correct.")
		self.set_sec_percentage()

	def get_attributes( self ):
		""" It parses the VLC status xml file and returns a dictionary of attributes. """
		page = requests.get('http://:213@localhost:'+str(self.port)+'/requests/status.xml')
		
		attributes = {}
		et = ET.fromstring( page.text )
		for ele in et:
			if len(ele) == 0:
				attributes[ ele.tag ] = ele.text
			else:
				attributes[ ele.tag ] = {}
				for subele in ele:
					if subele.tag == "category":
						subattr = attributes[ ele.tag ][ subele.get("name") ] = {}
						for _subele in subele:
							subattr[ _subele.get("name")] = _subele.text
					else:
						attributes[ ele.tag ][ subele.tag ] = subele.text
		return attributes

	def set_sec_percentage(self):
		""" Calculates and sets how much percentage of media each second represents for the seek() function. """
		attributes = self.get_attributes()
        
        try:
		    media_length = int(attributes["length"])
		    self.sec_percentage = float(100 / length)
		    print "sec_percentage" + str(self.sec_percentage)
	except:
		    pass

	def send_command(self, command, val=None):
		""" Send commands to VLC http interface - seek, volume, pause/play etc .""" 
		
		if (val == None ):
			requests.get('http://:213@localhost:'+str(self.port)+'/requests/status.xml?command=' + command  )
		else:
			requests.get('http://:213@localhost:'+str(self.port)+'/requests/status.xml?command=' + command + '&val=' + urllib.quote_plus(str(val))  )

	def current_pos(self, flag=SEEK_BEGIN):
		""" Seek the media to value given in seconds. By default, it seeks from current media position.
Additionaly, flag SEEK_BEGIN can be passed to seek from beginning position."""
		attributes = self.get_attributes()
		c_position= float(attributes["position"])*float(length)*1000
		print "FRAME: "+str(c_position)+"\n"


	def seek(self, val, flag=SEEK_BEGIN):
		""" Seek the media to value given in seconds. By default, it seeks from current media position.
Additionaly, flag SEEK_BEGIN can be passed to seek from beginning position."""
		attributes = self.get_attributes()
	
		if( not("length" in attributes) ):
			raise Exception("No media being played for seek command to work.")

		elif( flag == self.SEEK_BEGIN ):
			seek_offset = 0;

		else:
			raise Exception("Unknown flag passed.")
		seek_offset = -0.5;

		seek_val_sec = float(float(seek_offset + val)*25 )
		
		seek_percentage = float( seek_val_sec )/ float(length ) 
		
		seek_percentage = seek_percentage * 100

		seek_percentage=round(seek_percentage,3)


#          	print str(seek_percentage) + "%"



		self.send_command("seek", str(seek_percentage) + "%")


	def set_volume(self, val):
		""" Sets the volume of VLC. The interface expects value between 0 and 512 while in the UI it is 0% to 200%. So a factor of 2.56 is used
to convert 0% to 200% to a scale of 0 to 512."""

		self.send_command("volume", val)

	def play_file(self, infile):
		""" Send the input file to be played. The in_file must be a valid playable resource."""

		if( not( os.path.isfile(infile) ) ):
			raise Exception("FileNotFound: The file " + infile + " does not exist.")
		else:
			self.send_command("in_file", "file://" + os.path.abspath(infile) )

# No-argument commands. 

	def play_pause(self):
		"""Toggle between play and pause."""

		self.send_command("pl_pause")
	def pause(self):
		"""Toggle between play and pause."""

		self.send_command("pl_pause")
	def mute(self):
		self.send_command("no-audio")
	
	def unmute(self):
		self.send_command("volume=1000")

	def play(self):
		self.send_command("pl_play")

	def stop(self):
		"""Stops the player."""

		self.send_command("pl_stop")

	def fullscreen(self):
		""" Toggle fullscreen."""

		self.send_command("pl_stop")

	def next(self):
		""" Next media on the playlist. """

		self.send_command("pl_next")

	def previous(self):
		""" Previous media on the playlist. """

		self.send_command("pl_previous")




if len(sys.argv) > 1:
	spiazzamento_frame= float(sys.argv[1])
	dsearch=float(sys.argv[2])
	dloop=float(sys.argv[3])
	dritardo=float(sys.argv[4])
	s_timeout=float(sys.argv[5])
	dcomando=float(sys.argv[6])
else:
	spiazzamento_frame=0
	dsearch=0.025
	dloop=0.01
	dritardo=0
	s_timeout=0
	dcomando=0.18

global flag_audio
flag_audio=0


print "spiazzamento " + str(spiazzamento_frame)
print "dealy search " + str(dsearch)
print "delay loop " + str(dloop)
print "delay ritardo " + str(dritardo)
print "serail timeout " + str(s_timeout)
print "delay comando " + str(dcomando)





ser01 = serial.Serial()
#port=device_serial01, baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE,bytesize=8)
ser02 = serial.Serial()
#port=device_serial02, baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE,bytesize=8)


#PORTA SERIALE COLLEGATA AL LETTORE
ser01.port = "/dev/ttyS0"
#ser01.port = "/dev/ttyUSB0"
ser01.baudrate = 4800
ser01.bytesize = serial.EIGHTBITS #number of bits per bytes
ser01.parity = serial.PARITY_NONE #set parity check: no parity
ser01.stopbits = serial.STOPBITS_ONE #number of stop bits
ser01.timeout = 0.05            #non-block read
ser01.xonxoff = False     #disable software flow control

# PORTA SERIALE COLLEGATA ALLA BOARD
ser02.port = "/dev/ttyUSB0"
#ser02.port = "/dev/ttyAMA0"
#ser02.port = "/dev/ttyUSB1"
ser02.baudrate = 9600
ser02.bytesize = serial.EIGHTBITS #number of bits per bytes
ser02.parity = serial.PARITY_NONE #set parity check: no parity
ser02.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser02.timeout = 0.001           #non-block read
ser02.timeout = s_timeout          #non-block read
#ser02.xonxoff = True     #disable software flow control
#ser02.rtscts = True     #disable software flow control
#ser02.dsrtdr = True     #disable software flow control


time.sleep(4)

vlc = vlc_http()



try: 

    ser02.open()

except Exception, e:

    print "error open serial port: " + str(e)

    exit()

if  ser02.isOpen():

    try:
	print "OK START"
        print "leggo risposte dal pioneer"
        print "Reading from " + ser02.port

	timeout = 0.1
        time.sleep(0.1)
        ser02.write("A")
        ser02.write("0")
        ser02.write("\r")
        ser02.write(chr(0xa))


    	while (True ):


		readlines,_,_ = select.select([ser02], [], [], timeout)
		read_serial_from_philips(ser02)

    except Exception, e:
	print " ECCEZIONE"
	print 	str(e)
	exit()



