from __future__ import print_function
from PIL import Image
import webcolors
from PIL import Image
from colorthief import ColorThief
from rembg import remove
import os
import colorsys

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Find the nearest color name from rgb code
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name
 
# To remove background of image
# Detect dominant color and find the nearest color name
def get_dominant_color(input_path):
    output_path = "../../images/backgroundremoved.png"
    
    # Remove background of image
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)

    # get the dominant color rgb code
    color_thief = ColorThief(output_path)  
    dominant_color = color_thief.get_color(quality=1)
    #print(dominant_color)
    
    # Get the nearest color name from rgb code
    requested_colour = dominant_color
    lst = list(colorsys.rgb_to_hls(requested_colour[0], requested_colour[1], requested_colour[2]))
    lst[1] = min(lst[1] + 100, 255)
    requested_colour_light = colorsys.hls_to_rgb(lst[0], lst[1], lst[2])
    closest_name = get_colour_name(requested_colour_light)

    hsv_col = colorsys.rgb_to_hsv(requested_colour[0],requested_colour[1],requested_colour[2])

    #print("Closest colour name:", closest_name)
    return closest_name, hsv_col
