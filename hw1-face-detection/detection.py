import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    '''
    1.Load the name of image and the information of its divided areas 
      (left-top point (x,y), range) from 'detectData.txt'.
    2.Load image twice by grayscale and default mode.
    3.For each divided area, save it as a new smaller image, 
      and then turn it into 19 x 19
    4.Detect smaller image from 3. by the classifier, if it is classified as a face, 
      add a green rectangular frame onto the original image;
      if not, add a red rectangular frame.
    '''
    file = open(dataPath, "r")
    subPath = 'data/detect/'
    num_testZone = 0
    dic = {}
    fileNames = []
    for line in file:
        len = 0
        idx = 0
        if num_testZone == 0:
            for ch in line:
                if ch == ' ':
                    fileName = line[idx - len: idx]
                    fileNames.append(fileName)
                    dic[fileName] = []
                    len = 0
                elif line[idx] == line[-1]:
                    num_testZone = int(line[idx - len: idx])
                else:
                    len += 1
                idx += 1
        else:
            range = []
            for ch in line:
                if ch == ' ':
                    range.append(int(line[idx - len: idx]))
                    len = 0
                elif line[idx] == line[-1]:
                    range.append(int(line[idx - len: idx]))
                else:
                    len += 1
                idx += 1
            num_testZone -= 1
            dic[fileName].append(tuple(range))
    file.close()
    for fileName in fileNames:
        img = cv2.imread(subPath + fileName, cv2.IMREAD_GRAYSCALE)
        img_colorful = cv2.imread(subPath + fileName)
        for zone in dic[fileName]:
            copy_img = img[zone[1]:zone[1] +
                           zone[3], zone[0]:zone[0] + zone[2]]
            res_img = cv2.resize(copy_img, (19, 19))
            if clf.classify(res_img) == 1:
                BGR_form = (0, 255, 0)
            else:
                BGR_form = (0, 0, 255)
            cv2.rectangle(
                img_colorful, (zone[0], zone[1]), (zone[0] + zone[2], zone[1] + zone[3]),
                 BGR_form, 3)
        cv2.imshow(fileName, img_colorful)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)
