#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
from PCQueue import PCQueue

def extractFrames(fileName, outputBuffer, maxFramesToLoad=9999):
    # Initialize frame count
    count = 0
    # open video file
    vidcap = cv2.VideoCapture(fileName)
    # read first image
    success,image = vidcap.read()
    print(f'Reading frame {count} {success}')
    while success:
        # add the frame to the buffer
        outputBuffer.put(image)
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1
    outputBuffer.put('$')
    print('Frame extraction complete')

def convertToGray(original, converted):
    count = 0
    while True:
        print(f'Converting frame {count}')

        inputFrame = original.get()

        if inputFrame == '$':
            break

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        converted.put(grayscaleFrame)

        count += 1

    converted.put('$')

def displayFrames(inputBuffer):
    # initialize frame count
    count = 0
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = inputBuffer.get()
        if frame == '$':
            break
        print(f'Displaying frame {count}')
        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        count += 1

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()


filename = 'clip.mp4'
# shared queue
start = PCQueue()
converted = PCQueue()
# extract the frames
extract = threading.Thread(target = extractFrames, args = (filename,start, 72))
convert = threading.Thread(target = convertToGray, args = (start,converted))
display = threading.Thread(target = displayFrames, args = (converted,))
# display the frames
extract.start()
convert.start()
display.start()
