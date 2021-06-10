# importing  Libraries
import cv2
import time
import pyttsx3



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # for female voice

def talk(text):
    engine.say(text)
    engine.runAndWait()

def line_dis(image, m, n,label, distance,command):
    Line_Position2 = int(image.shape[1] * (50 / 100))
    cv2.line(image, pt1=(Line_Position2, 0), pt2=(Line_Position2, image.shape[0]), color=(255, 0, 0),
             thickness=2, lineType=8, shift=0)

    bounding_mid = (int(m), int(n))
    if (bounding_mid):
        distance_from_line = Line_Position2 - bounding_mid[0]
        if label==command:
            if (m > 320):
                while (distance_from_line) <= 0:
                    talk("Turn Left")
                    if (distance_from_line) >= -20:
                        step = (distance / 9)
                        step = round(step, 0)
                        talk(f"{label} at a distance{distance},Please go {step} steps Forward")
                        time.sleep(5)
                    break


            else:
                while (distance_from_line) >= 0:
                    talk("Turn Right")
                    if (distance_from_line) <= 20:
                        step = (distance / 9)
                        step=round(step,0)
                        talk(f"{label} at a distance{distance},Please go {step} steps Forward")
                        time.sleep(5)
                    break

