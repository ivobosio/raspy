import rrdtool
import time
import datetime
import rrdtool
import RPi.GPIO as GPIO
import subprocess
import os
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
time.sleep(7)

database_file = "/opt/dallas/database.rrd"
MIN_TEMP = -100
MAX_TEMP = 50
TEMP_ALL = -6
porta = 0
# Setup pin23 for input
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
# Setup pin17 for output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def read_temp_1():
# open/read/close the file with the temperature; the output is like
# in the example above.
tfile = open("/sys/bus/w1/devices/28-000004b5bf2e/w1_slave")
text = tfile.read()
tfile.close()

# split the two lines
lines = text.split("\n")

# make sure the crc is valid
if lines[0].find("YES") > 0:
    # get the 9th (10th) chunk of text and lose the t= bit
    temp = float((lines[1].split(" ")[9])[2:])
# add a decimal point
    temp /= 1000
    return temp
#return MIN_TEMP-1

temp1 = read_temp_1()

def read_temp_2():
# open/read/close the file with the temperature; the output is like
# in the example above.
tfile = open("/sys/bus/w1/devices/28-000004b61d91/w1_slave")
text = tfile.read()
tfile.close()

# split the two lines
lines = text.split("\n")

# make sure the crc is valid
if lines[0].find("YES") > 0:
    # get the 9th (10th) chunk of text and lose the t= bit
temp = float((lines[1].split(" ")[9])[2:])
    # add a decimal point
    temp /= 1000
    return temp
# return MIN_TEMP-1

temp2 = read_temp_2()

#Attiva led
GPIO.output(17, True)
#Controlla porta
if GPIO.input(23) == True:
    porta = 44
    print"porta chiusa"
elif GPIO.input(23) == False:
print"porta aperta"
porta = 40
temp3 = temp2

print(temp1)
print(temp2)
print(temp3)
#scrivi su database
if temp1 >= MIN_TEMP and temp1 <= MAX_TEMP and temp2 >= MIN_TEMP and temp2 <= MAX_TEMP and temp3 >= MIN_TEMP and temp3 <= MAX_TEMP:
rrdtool.update(database_file, "N:%f:%f:%f:%f" % (temp1, temp2, temp3, porta) )
#allarme temperatura
if temp1 >= TEMP_ALL:
os.system('echo "Allarme" | mail -s "Allarme Temperatura Alta Cella 1" masc.seneca@gmail.com')

exit(0)