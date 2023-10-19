#!/usr/bin/python3
import socket
import zipfile
import os
#from playsound import playsound

os.chdir(os.path.dirname(os.path.realpath(__file__)))

IMG_PATH = "send_image.png"
SOUND_PATH = "send_audio.wav"
HEARTRATE_PATH = "send_heartrate.txt"
TEMPARATURE_PATH = "send_temperature.txt"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IP, SOCK_STREAM = TCP
client.connect(('gpu2.enst.fr', 8888))
print("Client connected")

zip_name = 'files.zip'

os.chdir("../data_to_send")

with zipfile.ZipFile(zip_name, 'w') as file:
    file.write(IMG_PATH)
    file.write(SOUND_PATH)
    file.write(HEARTRATE_PATH)
    file.write(TEMPARATURE_PATH)

print("zip done")

file_size = os.path.getsize(zip_name)
print("File Size is :", file_size, "bytes")
file_size_in_bytes = file_size.to_bytes(8, 'big')
    
print("Sending the file size")
client.send(file_size_in_bytes)
msg = client.recv(1024).decode("utf-8")                    
print(f"[SERVER]: {msg}")

f = open(zip_name, 'rb')
l = f.read()
client.sendall(l)

print("Sent to server")
os.remove(zip_name)

msg = client.recv(1024)
while(msg.decode("utf-8")!="OK"):
   msg = client.recv(1024) 

print("Get image from server")
os.system("scp ktung-22@gpu2.enst.fr:~/pact22/rapport/generated_image/generated_image.jpg ../generated_image")
print("Get music file from server")
os.system("scp ktung-22@gpu2.enst.fr:~/pact22/rapport/musiques/music_name.txt ../musiques")

print("Image received") 
f.close()
client.close()
### Play song after reading it's name in music_name.txt (os.system ...)

#os.system("DISPLAY=:0 feh -qrYzF --zoom 200  ../generated_image/generated_image.jpg &")
with open("../musiques/music_name.txt", 'r') as f:
    music_file = f.readline()
#playsound("../musiques/music_file.mp3")
print(music_file)
os.system("aplay ../musiques/"+music_file+" &")

os.system("DISPLAY=:0 feh -qrYzF --zoom 250 ../generated_image/generated_image.jpg")
