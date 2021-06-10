# importing  Libraries

from imutils.video import VideoStream
from Move import *
from Assist import *
import speech_recognition as sr
import datetime
import numpy as np

class visuals:
    ### Lists ###

    boxes = []
    confidences = []
    class_ids = []
    listener = sr.Recognizer()
    def __init__(self, boxes=boxes, confidences=confidences, class_ids=class_ids,listener=listener):
        self.boxes = boxes
        self.confidences = confidences
        self.class_ids = class_ids
        self.listener = listener

    def take_command(self):
        with sr.Microphone() as source:
            print('listening....!')
            sr.pause_threshold = 1
            voice = self.listener.listen(source)
            try:
                command = self.listener.recognize_google(voice)
                command = command.lower()
                print(command)
                return command
            except:
                return None

    def Object(self, layerOutput, classes, W, H):

        for output in layerOutput:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    self.boxes.append([x, y, int(width), int(height)])
                    self.confidences.append((float(confidence)))
                    self.class_ids.append(class_id)

        index = cv2.dnn.NMSBoxes(self.boxes, self.confidences, 0.5, 0.3)
        if len(index) > 0:
            # loop over the indexes we are keeping
            for i in index.flatten():
                # extract the bounding box coordinates
                (x, y) = (self.boxes[i][0], self.boxes[i][1])
                (w, h) = (self.boxes[i][2], self.boxes[i][3])
                label = str(classes[self.class_ids[i]])
                confidence = str(round(self.confidences[i], 2))
                #Find centre of image
                m = int(x + w / 2)
                n = int(y + h / 2)
                return (label, m, n, w)


def main():
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
    with open("coco.names", "r") as f:
        classes = f.read().splitlines()

    vs = VideoStream(0).start()
    visual = visuals()
    #Take command
    talk("How can I Help You")
    voice = visual.take_command()

    while True:
        frame = vs.read()
        H, W = frame.shape[:2]
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        layerOutput = net.forward(ln)
        # output_name = net.getUnconnectedOutLayersNames()
        # layerOutput = net.forward(output_name)
        Object = visual.Object(layerOutput, classes, W, H)
        label = Object[0]
        m = int(Object[1])
        n = int(Object[2])
        w = int(Object[3])

        Position = movement(frame,m, w)
        direction=Position[0]
        distance=Position[1]


        if voice is None:
            Direction(distance, label, direction)

        elif voice in classes:
            line_dis(frame, m, n,label,distance,voice)

        elif 'time' in voice:
            time = datetime.datetime.now().strftime('%I:%M:%S %p')
            talk('time is' + time)

        elif 'stop' in voice:
            talk('OK')
            break
        else:
            talk('Please say the command again')

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
