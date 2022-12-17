
## 1. install tesseract for windows : link --> https://github.com/UB-Mannheim/tesseract/wiki
#  2. pip install pytesseract

# The Mannheim University Library (UB Mannheim) uses Tesseract to perform text recognition
# (OCR = optical character recognition)

import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# read an image
img = cv.imread("1.png")
img = cv.resize(img, (900,600))
# pytesseract deals with RGB images so we have to convert to RGB as opencv reads in BGR format
RGBimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)
newImg = RGBimg.copy()
digitImg = RGBimg.copy()
# Now we convert image to text using pytesseract function image_to_string()
textFromImage = pytesseract.image_to_string(RGBimg)
# print(textFromImage)
# in this way you get the raw information from image about text and digits etc. 
# so how can we know where is the location of the each character, so that we can create a box around that 

# so the bounding box information is captured by using image_to_box() function of tesseract library
# first find out the height and width of actual image
imageH, imageW, _ = RGBimg.shape

############## detecting Characters
boxes = pytesseract.image_to_boxes(RGBimg)

# Each character is transform into list and their bounding box information like x, y, w and h is captured
for b in boxes.splitlines():
    b = b.split(" ")
    # print(b)
    # the b[1], 2, 3 and 4 are the x, y, w and h of the each character
    # as it is obtained in the form of string so we need to convert into integers
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    # now draw the rectangle 
    cv.rectangle(RGBimg, (x, imageH-y), (w, imageH-h), (255,0,255), 2)

    # now we have to label thses characters 
    cv.putText(RGBimg, b[0], (x, imageH-y+20), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

############### detecting words
# image_to_data() is the function of pytesseract library which extract the words from image 
boxes = pytesseract.image_to_data(newImg)
print(boxes)

for x, b in enumerate(boxes.splitlines()):
    if x!=0:
        b = b.split()
        # print(b)
        if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            # now draw the rectangle 
            cv.rectangle(newImg, (x, y), (x+w, y+h), (255,0,255), 2)

            # now we have to label thses characters 
            cv.putText(newImg, b[11], (x, y-5), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

############### detecting digits only
# image_to_data() is the function of pytesseract library which extract the words from image 
# so now we have to define some configurations
confg = r'--oem 3 --psm 6 outputbase digits'
boxes = pytesseract.image_to_data(digitImg, config=confg)
print(boxes)

for x, b in enumerate(boxes.splitlines()):
    if x!=0:
        b = b.split()
        # print(b)
        if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            # now draw the rectangle 
            cv.rectangle(digitImg, (x, y), (x+w, y+h), (255,0,255), 2)

            # now we have to label thses characters 
            cv.putText(digitImg, b[11], (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)


# Display image
cv.imshow("image", RGBimg)
cv.imshow("new", newImg)
cv.imshow("digit", digitImg)
cv.waitKey()