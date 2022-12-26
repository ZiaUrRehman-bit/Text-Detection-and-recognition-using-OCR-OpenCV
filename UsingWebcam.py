import cv2 as cv
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

output = np.ones((400, 400), "uint8")

cam = cv.VideoCapture(2)

while True:
    Success, frame = cam.read()

    RGBFrame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    copyFrame = RGBFrame.copy()

    frameH, frameW, _ = RGBFrame.shape
    output = np.ones((frameH, frameW), "uint8")*255

    boxes = pytesseract.image_to_boxes(RGBFrame)

    for b in boxes.splitlines():
        b = b.split(" ")

        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv.rectangle(RGBFrame, (x, frameH-y), (w, frameH-h), (255,0,255), 2)

        # now we have to label thses characters 
        cv.putText(RGBFrame, b[0], (x, frameH-y+20), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

    boxes = pytesseract.image_to_data(copyFrame)

    for x, b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            # print(b)
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                # now draw the rectangle 
                cv.rectangle(copyFrame, (x, y), (x+w, y+h), (255,0,255), 2)

                # now we have to label thses characters 
                cv.putText(copyFrame, b[11], (x, y-5), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                cv.putText(output, b[11], (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)


    cv.imshow("webcam", frame)
    cv.imshow("2", copyFrame)
    cv.imshow("3", output)
    k = cv.waitKey(1)

    if k == ord("q"):
        cv.destroyAllWindows()
        break