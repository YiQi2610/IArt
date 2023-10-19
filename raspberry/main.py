#!/usr/bin/python3
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

FICHIER = "../data_to_send/send_temperature.txt" ### Attention il faut changer le cron pour correspondre à ce PATH
f = open(FICHIER,'r')

i=0
k=0
temp1=""
temp2=""
T1=0.0
T2=0.0

j=0
for lines in f.readlines():
    if (j==0):
        for char in lines:
            if (i>=30 and i<=33):
                temp1+=str(char)
            i+=1
    
    if (j==1):
        for char in lines:
            if (k>=30 and k<=33):
                temp2+=str(char)
            k+=1
    j+=1
    
T1=float(temp1)
T2=float(temp2)
print(T2-T1)


print("QQUN PASSE DEVANT LA CAM LA !!!!")
exec(open('codecardio.py').read())
exec(open('capture.py').read())
exec(open('record.py').read())
exec(open('../socket/socket_client.py').read())
