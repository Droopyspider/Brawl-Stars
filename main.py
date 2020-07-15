# [----------------------------]
#           Version: 1.2
#     Made by: u/droopy_spider
#           Free to use
# [----------------------------]
# for py_game surfaces
import pygame, math
# cv2 for video and image manipulation
import cv2
# numpy for array manipulation
import numpy as np
# for file dialogue box
import easygui
# Notice
print("[----------------------------------------------------------]")
print("[----------------------Important Info:---------------------]")
print("[------------------Made by u/droopy_spider-----------------]")
print("[-For best result crop video/image into a 550 x 550 square-]")
print("[------------Credit is not necessary but welcome-----------]")
print("[----------Please report any bugs to me via reddit---------]")
print("[-----------------------Version: 1.2-----------------------]")
print("[----------------------------------------------------------]")
input("Press any key to continue...")
# getting path to video or image
print("Please choose a video or image to convert")
path = easygui.fileopenbox(title="Choose a video or image to convert", multiple=False)
# checking if a valid file_type
supported_extensions = {
    ".mp4": "video",
    ".wav": "video",
    ".avi": "video",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image"
    }
# path is in format dir\dir\file.extension splitting . and checking end directory
path_extension = "." + path.split(".")[1]
# variable for type of file
file_type = ""
# checking for key in dictionary
if not path_extension in supported_extensions:
    print("Unsupported extension please use:")
    for key in supported_extensions:
        print(key)
    exit()
# setting file type
file_type = supported_extensions[path_extension]
# initializing py_game
pygame.init()
pygame.display.set_mode((1, 1))
# creating py_game surface that will be used for drawing
screen = pygame.Surface((1100, 1100))
# asking which theme to use
theme_dictionary = {
    0: "desert",
    1: "mortuary"
    }
theme_colors = {
    0: (247, 164, 114),
    1: (70, 49, 78)
    }
# printing available themes
print("Please choose a theme: ")
for key in theme_dictionary:
    # printing all themes
    print(str(key) + " : " + theme_dictionary[key])
theme = int(input("Your theme: "))
# checking if theme is valid
if not theme in theme_dictionary:
    print("Invalid theme")
    exit()
# loading theme images
theme_images = {
    "desert": 6,
    "mortuary": 7
    }
loaded_theme_images = []
for i in range(theme_images[theme_dictionary[theme]]):
    # loading image
    img = pygame.image.load("./Images/" + str(theme_dictionary[theme]) + "/" + str(i + 1) + ".png").convert_alpha()
    # appending to list
    loaded_theme_images.append(img)
# checking if video or image is loadable
cap = None
try:
    if file_type == "video":
        cap = cv2.VideoCapture(path)
    elif file_type == "image":
        cap = cv2.imread(path)
    else:
        print("Something unexpected occured")
        exit()
except:
    print("Unable to open " + file_type + "...")
    exit()
# everything should be correctly loaded
# save location
save_path = path.split("\\")
save_path = path.replace(save_path[len(save_path) - 1], "")
print("Frame(s) will be saved in image/videos directory:")
print(save_path)
print("Continue?")
if input("(y/n)").lower() != "y":
    print("Exiting...")
    exit()
# good good good
# getting height and width of image/video
width = 0
height = 0
frame_count = 0
if file_type == "video":
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
elif file_type == "image":
    width = cap.shape[0]
    height = cap.shape[1]
# working out frame count
if file_type == "image":
    # frame "count" for images as 1
    frame_count = 1
else:
    # frame for video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# frame saving function
surface = pygame.Surface((1100, 1100))


def draw(frame_array, frame_number):
    # setting background color
    surface.fill(theme_colors[theme])
    # getting 5 x 5 pixels and getting average color
    for y in range(110):
        for x in range(110):
            # color average
            col_average = [0]
            # 5 x 5 starting by multiplying x and y by 10
            start_x = x * 5
            start_y = y * 5
            # looping through twenty five pixels adding colors together
            for y2 in range(5):
                for x2 in range(5):
                    # this gets looped 302,500 times got to be efficient
                    # took out greyscale portion due to it being a massive bottleneck
                    # adding color to average
                    col_average[0] += frame_array[start_y + y2][start_x + x2]
            # dividing variable by 25 to get average
            col_average[0] = int(col_average[0] / 25)
            # seeing what image it is closest to
            # getting total number of images
            total = len(loaded_theme_images)
            # working out size of each section
            size = 255 / total
            # dividing by size rounding down to work out which portion
            which_image = col_average[0] / size
            # adding a small amount to prevent 0 and 255 breaking it
            if which_image < 3:
                which_image += 0.1
            if which_image > 3:
                which_image -= 0.1
            number = math.floor(which_image)
            # blitting
            surface.blit(loaded_theme_images[number], (x * 10, y * 10))
    # saving frame
    pygame.image.save(surface, save_path + str("Frame" + str(frame_number)) + ".png")
    print("Saved Frame")


# looping through frame count
frame_number = 0
while frame_number < frame_count:
    buf = np.empty((1, height, width, 3), np.dtype('uint8'))
    # setting cap if frame count is greater than 1
    if frame_count > 1:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    # reading next frame
    if file_type == "video":
        ret, buf = cap.read()
        buf = cv2.cvtColor(buf, cv2.COLOR_BGR2GRAY)
        draw(buf, frame_number)
    else:
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        draw(cap, frame_number)
    frame_number += 1



