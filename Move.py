# importing  Libraries
import cv2
import os
import imutils
import pyttsx3

engine = pyttsx3.init()
list = []
know_dist = 30
know_width = 15


def talk(text):
    engine.say(text)
    engine.runAndWait()


def find_maker(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    return cv2.minAreaRect(c)


def Focal_length(ref_image_width):
    focal_length = (ref_image_width * know_dist) / (know_width)
    return focal_length


def Distance(Focal_length, hand_width_frame):
    distance = (know_width * Focal_length) / (hand_width_frame)
    return distance


counter = 0


def movement(frame, m, w, counter=counter):
    if m < 320:
        direction = "Left"
    else:
        direction = "Right"

    img_name = "opencv_frame_{}.png".format(counter)
    cv2.imwrite(img_name, frame)
    rf_image = cv2.imread(img_name)
    refer_image_width = find_maker(rf_image)
    Frame_Width = w
    ref_image_width = refer_image_width[1][0]

    focal_length = Focal_length(ref_image_width)
    os.remove(img_name)

    if Frame_Width != 0:
        Dis = round(Distance(focal_length, Frame_Width), 2)
        list.append(Dis)
        return (direction, Dis)


# It will give direction of moving objects
def Direction(Dis, label, direction):
    if len(list) > 2:
        j = list[-2]
        k = list[-1]
        if j == k:
            movement = 'Stable'

        elif j < k:
            movement = "Backward"

        elif j > k:
            movement = "Forward"

        else:
            movement = " "

        if Dis < 20:

            if movement == 'Stable':
                talk(f"{label} is Stable at{Dis}inches")
            else:
                if direction == "Right":
                    if movement == "Forward":
                        talk(
                            f"{label}on your{direction} is moving towars you,at a distance{Dis}inches,Please go left")
                elif direction == "Left":
                    if movement == "Forward":
                        talk(
                            f"{label}on your{direction} is moving towars you,at a distance{Dis}inches,Please go Right")
                elif movement == "Backward":
                    talk(f"{label}Moving Backward Direction")
        else:
            talk(f"You are in Safe Zone,{label} in front of you")
