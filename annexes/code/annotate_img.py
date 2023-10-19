from PIL import Image, ImageOps, ImageDraw, ImageFont
import os

def annotate_img(path, emotion, bpm, color, temp):
    img = Image.open(path)
    width = (199,0)
    black_border_img = ImageOps.expand(img,border=width)
    li = path.split(".")

    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')
    font = ImageFont.truetype(os.path.join(font_path, 'agane.ttf'), 32)

    annotated_img = ImageDraw.Draw(black_border_img)
    annotated_img.text((30,150), emotion, (255,255,255), font=font)
    annotated_img.text((30,203), bpm + " bpm", (255,255,255), font=font)
    annotated_img.text((30,256), color, (255,255,255), font=font)
    annotated_img.text((30,309), temp + "°C", (255,255,255), font=font)
    black_border_img.save(".".join(li[:-1]) + "_annotated." + li[-1])

annotate_img("../../images/test_prof2.jpg", "angry", "110", "red", "36.5")
