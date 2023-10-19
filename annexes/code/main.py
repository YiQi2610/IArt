#!/usr/bin/python3
from detectColor import get_dominant_color
from get_emotion import get_emotion
from get_heartrate import get_heartrate
from get_temperature import get_temperature
from generate_img import generate_img
from choose_song import choose_song
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

IMG_PATH = "../../data_received/send_image.png"
SOUND_PATH = "../../data_received/send_audio.wav"
HEARTRATE_PATH = "../../data_received/send_heartrate.txt"
TEMPARATURE_PATH = "../../data_received/send_temperature.txt"
IMG_EXPORT_PATH = "../../generated_image/generated_image.jpg"


def exec():
    main_emotion = get_emotion(SOUND_PATH)
    print("Emotion GET : " + main_emotion)
    main_color, hsv_color = get_dominant_color(IMG_PATH)
    print("Dominant color GET : " + main_color)
    heartrate = get_heartrate(HEARTRATE_PATH)
    print("Heartrate GET : " + heartrate)
    temperature = get_temperature(TEMPARATURE_PATH)
    print("Temperature GET : " + str(temperature))

    choose_song(main_emotion)
    generate_img(main_color, main_emotion, heartrate, temperature, IMG_EXPORT_PATH)
    #annotate_img(IMG_EXPORT_PATH)


if __name__ == '__main__':
    exec()
