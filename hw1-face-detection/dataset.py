import os
import cv2
import numpy as np


def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first
    element is the numpy array of shape (m, n) representing the image.
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    '''
    1.In following two for-loops, load the training images by OpenCV from two folders,
      'face' and 'non-face' respectly.
    2.Let each image and a label meaning the image is face or not (1 or 0) 
      form a tuple and add it into the list of dataset.
    '''
    dataset = []
    subPath = dataPath + '/face'
    for filename in os.listdir(subPath):
        img = cv2.imread(subPath + '/' + filename, cv2.IMREAD_GRAYSCALE)
        dataset.append((img, 1))
    subPath = dataPath + '/non-face'
    for filename in os.listdir(subPath):
        img = cv2.imread(subPath + '/' + filename, cv2.IMREAD_GRAYSCALE)
        dataset.append((img, 0))
    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)
    return dataset
