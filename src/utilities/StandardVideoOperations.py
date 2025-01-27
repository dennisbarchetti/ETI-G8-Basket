import cv2 as cv
import numpy as np
import imutils
import sys
import imutils
from tkinter import *
"""
from collections import deque
from imutils.video import VideoStream
import time
import argparse
"""

class StandardVideoOperations:  # class for manage the operation on the video

    # instances of the KNN Background Substractor
    KNN_SX = cv.createBackgroundSubtractorKNN(history=200)
    KNN_DX = cv.createBackgroundSubtractorKNN(history=200)

    # when a new instance of StandardVideoOperations is created is initialized with (0, 0) as default values for all ROIs
    def __init__(self):
        self.upper_left_LEFT = (0, 0)
        self.bottom_right_LEFT = (0, 0)
        self.upper_left_RIGHT = (0, 0)
        self.bottom_right_RIGHT = (0, 0)

    # set the values for the left ROI
    def set_left(self, upper_left, bottom_right):
        if (len(upper_left) != 2 or len(bottom_right)) != 2:
            sys.exit("error: upper_left and bottom_right must be arrays with 2 items")
        if not all(isinstance(x, int) for x in upper_left) or not all(isinstance(x, int) for x in bottom_right):
            sys.exit("error: upper_left and bottom_right must contain only integers")
        self.upper_left_LEFT = upper_left
        self.bottom_right_LEFT = bottom_right

    # set the values for the right ROI
    def set_right(self, upper_left, bottom_right):
        if (len(upper_left) != 2 or len(bottom_right)) != 2:
            sys.exit("error: upper_left and bottom_right must be arrays with 2 items")
        if not all(isinstance(x, int) for x in upper_left) or not all(isinstance(x, int) for x in bottom_right):
            sys.exit("error: upper_left and bottom_right must contain only integers")
        self.upper_left_RIGHT = upper_left
        self.bottom_right_RIGHT = bottom_right

    # return a frame cutted cutted as specified in the parameters
    @staticmethod
    def video_cutter(frame, upper_left, bottom_right):
        if(len(upper_left) != 2 or len(bottom_right)) != 2:
            sys.exit("error: upper_left and bottom_right must be arrays with 2 items")
        if not all(isinstance(x, int) for x in upper_left) or not all(isinstance(x, int) for x in bottom_right):
            sys.exit("error: upper_left and bottom_right must contain only integers")
        if not isinstance(frame, np.ndarray):
            sys.exit("error: frame must be of type numpy.ndarray")
        if frame.ndim != 3:
            sys.exit("error: frame should be a matrix of three dimensions")
        rect_frame = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
        return rect_frame



    def cut_frame(self,startingFrame):
        if not isinstance(startingFrame, np.ndarray):
            sys.exit("error: startingFrame must be of type numpy.ndarray")
        if startingFrame.ndim != 3:
            sys.exit("error: startingFrame should be a matrix of three dimensions")
        leftCut = StandardVideoOperations.video_cutter(startingFrame, self.upper_left_LEFT, self.bottom_right_LEFT)
        rightCut = StandardVideoOperations.video_cutter(startingFrame, self.upper_left_RIGHT, self.bottom_right_RIGHT)

        return leftCut,rightCut

    """
    # cut the frame with the ROI values setted with set_left method
    def cut_left(self, startingFrame):
        if not isinstance(startingFrame, np.ndarray):
            sys.exit("error: startingFrame must be of type numpy.ndarray")
        if startingFrame.ndim != 3:
            sys.exit("error: startingFrame should be a matrix of three dimensions")
        leftCut = StandardVideoOperations.video_cutter(startingFrame, self.upper_left_LEFT, self.bottom_right_LEFT)
        return leftCut

    # cut the frame in params with the ROI values setted with set_right method
    def cut_right(self, startingFrame):
        if not isinstance(startingFrame, np.ndarray):
            sys.exit("error: startingFrame must be of type numpy.ndarray")
        if startingFrame.ndim != 3:
            sys.exit("error: startingFrame should be a matrix of three dimensions")
        rightCut = StandardVideoOperations.video_cutter(startingFrame, self.upper_left_RIGHT, self.bottom_right_RIGHT)
        return rightCut
    """

    # draw an empty rectangle with the specified color and position
    @staticmethod
    def draw_rectangle(frameBGR, upperLeft, bottomRight, color_string):
        if not isinstance(frameBGR, np.ndarray):
            sys.exit("error: frameBGR must be of type numpy.ndarray")
        if frameBGR.ndim != 3:
            sys.exit("error: frameBGR mask be a matrix of three dimensions")
        color = (255, 0, 0)
        if color_string == "red":
            color = (0, 0, 255)
        if color_string == "green":
            color = (0, 255, 0)
        return cv.rectangle(frameBGR, upperLeft, bottomRight, color, 1)

    # return the frame applying a mask to isolate the color of the ball
    @staticmethod
    def hsv_thresholding(frames,color):
        if not isinstance(frames[0], np.ndarray) and not isinstance(frames[1], np.ndarray):
            sys.exit("error: frame_hsv must be of type numpy.ndarray")
        if frames[0].ndim != 3 and frames[1].ndim != 3:
            sys.exit("error: frame_hsv should be a matrix of three dimensions")

        frames_hsv_sx = cv.cvtColor(frames[0] , cv.COLOR_BGR2HSV)
        frames_hsv_dx = cv.cvtColor(frames[1], cv.COLOR_BGR2HSV)

        mask0 = cv.inRange(frames_hsv_sx, color[0], color[1])
        mask0 = cv.morphologyEx(mask0, cv.MORPH_OPEN,(5, 5), iterations=1)
        mask0 = cv.dilate(mask0, None, iterations=2)

        mask1 = cv.inRange(frames_hsv_dx, color[0], color[1])
        mask1 = cv.morphologyEx(mask1, cv.MORPH_OPEN, (5, 5), iterations=1)
        mask1 = cv.dilate(mask1, None, iterations=2)

        res_sx = cv.bitwise_and(frames_hsv_sx, frames_hsv_sx, mask=mask0 )
        res_dx= cv.bitwise_and(frames_hsv_dx, frames_hsv_dx, mask=mask1 )


        return res_sx,res_dx

    """"
    @staticmethod
    def get_hsvmask_on_ball(frame_hsv):
        if not isinstance(frame_hsv, np.ndarray):
            sys.exit("error: frame_hsv must be of type numpy.ndarray")
        if frame_hsv.ndim != 3:
            sys.exit("error: frame_hsv should be a matrix of three dimensions")

        lower_red = np.array([160, 75, 85])
        upper_red = np.array([180, 255, 255])
        #lower_red = np.array([ 4, 53, 38])
        #upper_red = np.array([ 350, 54, 40])

        mask = cv.inRange(frame_hsv, lower_red, upper_red)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN,(5, 5), iterations=1)
        mask = cv.dilate(mask, None, iterations=2)


        res = cv.bitwise_and(frame_hsv, frame_hsv, mask=mask )
        return res
    """

    @staticmethod
    def get_knn_on_frame(frames):
        if not isinstance(frames[0], np.ndarray) and not isinstance(frames[1], np.ndarray):
            sys.exit("error: frame_hsv must be of type numpy.ndarray")
        if frames[0].ndim != 3 and frames[1].ndim != 3:
            sys.exit("error: frame_hsv should be a matrix of three dimensions")
        frames_knn_sx = StandardVideoOperations.KNN_SX.apply(frames[0])
        frames_knn_dx = StandardVideoOperations.KNN_DX.apply(frames[1])
        return frames_knn_sx,frames_knn_dx
    # apply the knn method on the left frame

    """"
    @staticmethod
    def get_knn_on_left_frame(frame):
        if not isinstance(frame, np.ndarray):
            sys.exit("error: frame must be of type numpy.ndarray")
        if frame.ndim != 3:
            sys.exit("error: frame mask be a matrix of three dimensions")
        frame_knn = StandardVideoOperations.KNN_SX.apply(frame)
        return frame_knn

    # apply the knn method on the left frame
    @staticmethod
    def get_knn_on_right_frame(frame):
        if not isinstance(frame, np.ndarray):
            sys.exit("error: frame must be of type numpy.ndarray")
        if frame.ndim != 3:
            sys.exit("error: frame mask be a matrix of three dimensions")
        frame_knn = StandardVideoOperations.KNN_DX.apply(frame)
        #history= StandardVideoOperations.KNN_DX.getHistory()
        #print("history",history)
        return frame_knn
    
    # find the circles from counturns
    @staticmethod
    def find_circles(frame_to_scan, frame_to_design):
        if not isinstance(frame_to_scan, np.ndarray):
            sys.exit("error: frame_to_scan must be of type numpy.ndarray")
        if frame_to_scan.ndim != 3:
            sys.exit("error: frame_to_scan mask be a matrix of three dimensions")
        if not isinstance(frame_to_design, np.ndarray):
            sys.exit("error: frame_to_design must be of type numpy.ndarray")
        if frame_to_design.ndim != 3:
            sys.exit("error: frame_to_design mask be a matrix of three dimensions")
        cnts = cv.findContours(frame_to_scan.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            for i in cnts:
                ((x, y), radius) = cv.minEnclosingCircle(i)
                if 10 < radius < 25:
                    cv.circle(frame_to_design, (int(x), int(y)), int(radius), (255, 255, 255), -1)
        return frame_to_design

    # return true if the ball is spotted inside the specified rows and column range
    """
    @staticmethod
    def countWhitePixels(rows, colRange, greyScaleFrame):
        if not all(isinstance(row, int) for row in rows) or not all(isinstance(col, int) for col in colRange):
            sys.exit("error: rows and colRange must contain only integers")
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        for row in rows:
            consecutiveWhitePixels = 0
            consecutiveBlackPixels = 0
            for col in colRange:
                if greyScaleFrame[row, col] < 255:
                    consecutiveBlackPixels += 1
                    if consecutiveBlackPixels == 2:
                        consecutiveWhitePixels = 0
                else:
                    consecutiveBlackPixels = 0
                    consecutiveWhitePixels += 1
                    if 15 < consecutiveWhitePixels:
                        return True
        return False

    # return true if the ball is spotted above the basket in the right frame
    @staticmethod
    def spotBallOnTop_right(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [50, 55, 60]
        return StandardVideoOperations.countWhitePixels(rows, range(90, 150), greyScaleFrame)

    # return true if the ball is spotted in the middle of the basket in the right frame
    @staticmethod
    def spotBallOnMedium_right(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [100, 105, 110]
        return StandardVideoOperations.countWhitePixels(rows, range(90, 150), greyScaleFrame)

    # return true if the ball is spotted below the basket in the right frame
    @staticmethod
    def spotBallOnBottom_right(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [160, 165, 170]
        return StandardVideoOperations.countWhitePixels(rows, range(75, 175), greyScaleFrame)

    # return true if the ball is spotted above the basket in the left frame
    @staticmethod
    def spotBallOnTop_left(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [85, 90, 95]
        return StandardVideoOperations.countWhitePixels(rows, range(80, 140), greyScaleFrame)

    # return true if the ball is spotted in the middle of the basket in the left frame
    @staticmethod
    def spotBallOnMedium_left(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [125, 130, 135]
        return StandardVideoOperations.countWhitePixels(rows, range(80, 140), greyScaleFrame)

    # return true if the ball is spotted below the basket in the left frame
    @staticmethod
    def spotBallOnBottom_left(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [160, 165, 170]
        return StandardVideoOperations.countWhitePixels(rows, range(70, 160), greyScaleFrame)


    @staticmethod
    def change_color_space(frames):
        bwsx = cv.cvtColor(frames[0], cv.COLOR_BGR2GRAY)
        bwdx = cv.cvtColor(frames[1], cv.COLOR_BGR2GRAY)
        return bwsx,bwdx


    @staticmethod
    def cumpute_denseOpticalFlow(prev_gray,gray,masksx,maskdx):
        flowsx = cv.calcOpticalFlowFarneback(prev_gray[0], gray[0], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flowdx = cv.calcOpticalFlowFarneback(prev_gray[1], gray[1], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        # Computes the magnitude and angle of the 2D vectors for each main
        magnitudesx, anglesx = cv.cartToPolar(flowsx[..., 0], flowsx[..., 1])
        magnitudedx, angledx = cv.cartToPolar(flowdx[..., 0], flowdx[..., 1])
        # Sets image hue according to the optical flow direction
        masksx[..., 0] = anglesx * 180 / np.pi / 2
        maskdx[..., 0] = angledx * 180 / np.pi / 2
        # Sets image value according to the optical flow magnitude (normalized)
        masksx[..., 2] = cv.normalize(magnitudesx, None, 0, 255, cv.NORM_MINMAX)
        maskdx[..., 2] = cv.normalize(magnitudedx, None, 0, 255, cv.NORM_MINMAX)
        return masksx,maskdx


    @staticmethod
    def display_color_suggestion():

        root = Tk()
        root.geometry("300x400")
        root.title(" Color Suggestioin ")

        def choose_color(color):
            switcher={
                "red": 'lower_red = [160, 75, 85]\nupper_red = [180, 255, 255]',
                "Red": 'lower_red = [160, 75, 85]\nupper_red = [180, 255, 255]',
                "RED": 'lower_red = [160, 75, 85]\nupper_red = [180, 255, 255]',
                "blue": 'lower_blue = [90, 137, 98]\nupper_blue = [129, 255, 255]',
                "Blue": 'lower_blue = [90, 137, 98]\nupper_blue = [129, 255, 255]',
                "BLUE": 'lower_blue = [90, 137, 98]\nupper_blue = [129, 255, 255]'

                }
            return switcher.get(color,"empty");

        def Take_input():
            INPUT = inputtxt.get("1.0", "end-1c")
            print(INPUT)
            color=choose_color(INPUT)
            Output.insert(END, color)


        l = Label(text="Select a color to filter  ")
        inputtxt = Text(root, height=10,
                        width=25,
                        bg="light yellow")

        Output = Text(root, height=10,
                      width=30,
                      bg="light cyan")

        Display = Button(root, height=2,
                         width=20,
                         text="Show",
                         command=lambda: Take_input())

        l.pack()
        inputtxt.pack()
        Display.pack()
        Output.pack()

        mainloop()

    @staticmethod
    def color_calibration():

            def nothing(x):
                pass  # operatore per quando non succede nulla

            cap = cv.VideoCapture(0)

            cv.namedWindow("Tracking", cv.WINDOW_AUTOSIZE)
            cv.createTrackbar("LH", "Tracking", 0, 255, nothing)
            cv.createTrackbar("LS", "Tracking", 0, 255, nothing)
            cv.createTrackbar("LV", "Tracking", 0, 255, nothing)
            cv.createTrackbar("UH", "Tracking", 255, 255, nothing)
            cv.createTrackbar("US", "Tracking", 255, 255, nothing)
            cv.createTrackbar("UV", "Tracking", 255, 255, nothing)

            while True:
                # frame = cv2.imread('smarties.png')
                _, frame = cap.read()
                hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)  # convert/home/dennis/PycharmProjects/HSV_Object_traking/HSV.pye in un'immagine hsv

                l_h = cv.getTrackbarPos("LH", "Tracking")
                l_s = cv.getTrackbarPos("LS", "Tracking")
                l_v = cv.getTrackbarPos("LV", "Tracking")

                u_h = cv.getTrackbarPos("UH", "Tracking")
                u_s = cv.getTrackbarPos("US", "Tracking")
                u_v = cv.getTrackbarPos("UV", "Tracking")

                l_c = np.array([l_h, l_s, l_v])
                u_c = np.array([u_h, u_s, u_v])

                mask = cv.inRange(hsv, l_c, u_c)  # l_b e u_b sono i lower and upper layer

                res = cv.bitwise_and(frame, frame, mask=mask)

                cv.imshow("frame", frame)
                cv.imshow("mask", mask)
                cv.imshow("result", res)

                key = cv.waitKey(1)
                if key == 13: #enter key
                    cv.destroyAllWindows()
                    return l_c,u_c
                    break
            cap.release()
            cv.destroyAllWindows()

