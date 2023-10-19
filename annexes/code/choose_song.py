import os
import random

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def choose_song(emotion):
    song_names = ["Air_Elements", "Always_Moving_Forward", "Amazing_Future", "Ashes", "Bohemian_Garden", "Flying", "Future_Plans", "Good_Times", "In_Motion", "Infinite_Horizons", "Inner_Light", "Interconnected", "Oceans_of_Sand", "Stay_With_Me", "The_Deepest_Ocean", "Time_Flow", "Time", "Traces"]
    ang = ["Traces","Ashes","Good_Times","Time"]
    fear = ["Bohemian_Garden","Inner_Light","In_Motion","Ocean_of_Sand"]
    happ = ["Amazing_Future","Infinite_Horizons","Stay_With_Me","Always_Moving_Forward"]
    neutral = ["Future_Plans"]
    sad = ["Time_Flow","Flying","Air_Elements","The_Deepest_Ocean"]
    dis = ["Interconnected"]
    song = ''
    if emotion == "ANG" : 
        song = random.choice(ang)
    elif emotion == "FEA":
        song = random.choice(fear)
    elif emotion == "HAP":
        song = random.choice(happ)
    elif emotion == "NEU":
        song = random.choice(neutral)
    elif emotion == "SAD":
        song = random.choice(sad)
    else:
        song = random.choice(dis)
    song_name = song + ".wav"
    with open("../../musiques/music_name.txt", "w") as file:
        file.write(song_name)
