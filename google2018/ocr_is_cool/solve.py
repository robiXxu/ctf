#!/usr/local/bin/python

from PIL import Image
import pytesseract
import argparse
import cv2
import os


argp = argparse.ArgumentParser()
argp.add_argument("-i", "--image", required=True, help="path to image to be processed")
argp.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing done ")
args = vars(argp.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
if args["preprocess"] == "thresh":
  gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
  gray = cv2.medianBlur(gray, 3)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
startIndex = text.index("@ = Snoozed tome")
endIndex = text.index("No recect")
emailContent = text[startIndex:endIndex]
emailContent = emailContent.replace("@ = Snoozed tome", "").replace("> Sent", "")
print emailContent


# cv2.imshow("gray", gray)
# cv2.imshow("original", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()