#!/usr/local/bin/python

from PIL import Image
import pytesseract
import argparse
import cv2
import os
import string
import json
import re

argp = argparse.ArgumentParser()
argp.add_argument("-i", "--image", required=True, help="path to image")
argp.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing")
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

reg = "ctf {[a-zA-Z0-9]+}"

alphabet = "abcdefghijklmnopqrstuvwxyz"
otherChars = [" ", "\n"]

length = len(alphabet)
L2I = dict(zip(alphabet,range(length)))
I2L = dict(zip(range(length),alphabet))



def isOneOfTheOtherChars(c):
  return c in otherChars

def skip(c):
  return c in string.punctuation or c in string.digits or isOneOfTheOtherChars(c)

chars = json.dumps(emailContent.encode("utf-8")).lower()

for i in range(length):
  plaintext = ""
  for c in chars:
    if skip(c):
      plaintext += c
    else:
      plaintext += I2L[ (L2I[c]-i) % 26 ]

  if plaintext.find("ctf") != -1:
    print "Caesar Cipher Key is {}".format(i)
    flag = re.findall(reg, plaintext)[0]
    print "Solution is {}".format(flag)
