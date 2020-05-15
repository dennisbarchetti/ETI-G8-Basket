import cv2 as cv
import numpy as np
import imutils
import sys


class StandardVideoOperations:

    KNN = cv.createBackgroundSubtractorKNN()

    def set_left(self, upper_left, bottom_right):
        if (len(upper_left) != 2 or len(bottom_right)) != 2:
            sys.exit("error: upper_left and bottom_right must be arrays with 2 items")
        if not all(isinstance(x, int) for x in upper_left) or not all(isinstance(x, int) for x in bottom_right):
            sys.exit("error: upper_left and bottom_right must contain only integers")
        self.upper_left_LEFT = upper_left
        self.bottom_right_LEFT = bottom_right

    def set_right(self, upper_left, bottom_right):
        if (len(upper_left) != 2 or len(bottom_right)) != 2:
            sys.exit("error: upper_left and bottom_right must be arrays with 2 items")
        if not all(isinstance(x, int) for x in upper_left) or not all(isinstance(x, int) for x in bottom_right):
            sys.exit("error: upper_left and bottom_right must contain only integers")
        self.upper_left_RIGHT = upper_left
        self.bottom_right_RIGHT = bottom_right

    @staticmethod
    def video_cutter(frame_hsv, upper_left, bottom_right):
        if(len(upper_left) != 2 or len(bottom_right)) != 2:
            sys.exit("error: upper_left and bottom_right must be arrays with 2 items")
        if not all(isinstance(x, int) for x in upper_left) or not all(isinstance(x, int) for x in bottom_right):
            sys.exit("error: upper_left and bottom_right must contain only integers")
        if not isinstance(frame_hsv, np.ndarray):
            sys.exit("error: frame_hsv must be of type numpy.ndarray")
        if frame_hsv.ndim != 3:
            sys.exit("error: frame_hsv should be a matrix of three dimensions")
        rect_frame = frame_hsv[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
        return rect_frame

    def cut_left(self, startingFrame):
        """
        # 1° quarto
        upper_left = (455, 955)
        bottom_right = (655, 1155)
        """
        """
        # 2° quarto
        upper_left = (485, 950)
        bottom_right = (685, 1150)
        """
        """
        # 3° 4° quarto
        upper_left = (540, 940)
        bottom_right = (740, 1140)
        """
        if not isinstance(startingFrame, np.ndarray):
            sys.exit("error: startingFrame must be of type numpy.ndarray")
        if startingFrame.ndim != 3:
            sys.exit("error: startingFrame should be a matrix of three dimensions")
        leftCut = StandardVideoOperations.video_cutter(startingFrame, self.upper_left_LEFT, self.bottom_right_LEFT)
        return leftCut

    def cut_right(self, startingFrame):
        """
        # 1° quarto
        upper_left = (3145, 895)
        bottom_right = (3345, 1095)
        """
        """
        # 2° quarto
        upper_left = (3185, 910)
        bottom_right = (3385, 1110)
        """
        """
        # 3° 4° quarto
        upper_left = (3225, 900)
        bottom_right = (3425, 1100)
        """
        if not isinstance(startingFrame, np.ndarray):
            sys.exit("error: startingFrame must be of type numpy.ndarray")
        if startingFrame.ndim != 3:
            sys.exit("error: startingFrame should be a matrix of three dimensions")
        rightCut = StandardVideoOperations.video_cutter(startingFrame, self.upper_left_RIGHT, self.bottom_right_RIGHT)
        return rightCut
    
    @staticmethod
    def draw_rectangle(frameBGR, upperLeft, bottomRight, color_string):
        color = (255, 0, 0)
        if color_string == "red":
            color = (0, 0, 255)
        if color_string == "green":
            color = (0, 255, 0)
        return cv.rectangle(frameBGR, upperLeft, bottomRight, color, 1)

    @staticmethod
    def get_hsvmask_on_ball(frame_hsv):
        if not isinstance(frame_hsv, np.ndarray):
            sys.exit("error: frame_hsv must be of type numpy.ndarray")
        if frame_hsv.ndim != 3:
            sys.exit("error: frame_hsv should be a matrix of three dimensions")
        lower_red = np.array([160, 75, 85])
        upper_red = np.array([180, 255, 255])
        mask = cv.inRange(frame_hsv, lower_red, upper_red)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN,(5, 5), iterations=1)
        mask = cv.dilate(mask, None, iterations=2)
        res = cv.bitwise_and(frame_hsv, frame_hsv, mask=mask)
        return res

    @staticmethod
    def get_knn_on_frame(frame):
        if not isinstance(frame, np.ndarray):
            sys.exit("error: mask must be of type numpy.ndarray")
        if frame.ndim != 3:
            sys.exit("error: mask mask be a matrix of two dimensions")
        frame_knn = StandardVideoOperations.KNN.apply(frame)
        return frame_knn

    @staticmethod
    def find_circles(frame_to_scan, frame_to_design):
        cnts = cv.findContours(frame_to_scan.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            for i in cnts:
                ((x, y), radius) = cv.minEnclosingCircle(i)
                if 10 < radius < 25:
                    cv.circle(frame_to_design, (int(x), int(y)), int(radius), (255, 255, 255), -1)
        return frame_to_design

    # qualcosa su opticalflow nel relativo file

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

    @staticmethod
    def spotBallOnTop_right(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [50, 55, 60]
        return StandardVideoOperations.countWhitePixels(rows, range(90, 150), greyScaleFrame)

    @staticmethod
    def spotBallOnMedium_right(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [100, 105, 110]
        return StandardVideoOperations.countWhitePixels(rows, range(90, 150), greyScaleFrame)

    @staticmethod
    def spotBallOnBottom_right(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [160, 165, 170]
        return StandardVideoOperations.countWhitePixels(rows, range(75, 175), greyScaleFrame)

    @staticmethod
    def spotBallOnTop_left(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [85, 90, 95]
        return StandardVideoOperations.countWhitePixels(rows, range(80, 140), greyScaleFrame)

    @staticmethod
    def spotBallOnMedium_left(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [125, 130, 135]
        return StandardVideoOperations.countWhitePixels(rows, range(80, 140), greyScaleFrame)

    @staticmethod
    def spotBallOnBottom_left(greyScaleFrame):
        if greyScaleFrame.ndim != 2:
            sys.exit("error: greyScaleFrame must be a matrix of two dimensions")
        rows = [160, 165, 170]
        return StandardVideoOperations.countWhitePixels(rows, range(70, 160), greyScaleFrame)


svo = StandardVideoOperations()
capture = cv.VideoCapture("/path/tempo.asf")
# 1° quarto
# svo.set_left((455, 955), (655, 1155))
# svo.set_right((3145, 895), (3345, 1095))
# 2° quarto
# svo.set_left((485, 950), (685, 1150))
# svo.set_right((3185, 910), (3385, 1110))      # provare ad alzare la RoI nella parte dx a 900 per il secondo quarto per vedere se non vengono segnati più errori dovuti al monitor 
# 3° 4° quarto
svo.set_left((540, 940), (740, 1140))
svo.set_right((3225, 900), (3425, 1100))

if not capture.isOpened:
    print('Unable to open')
    exit(0)
top_frame = middle_frame = bottom_frame = frame_counter = last_score_frame = 0

upper_left1 = (80, 85)
bottom_right1 = (140, 95)

upper_left2 = (80, 125)
bottom_right2 = (140, 135)

upper_left3 = (70, 160)
bottom_right3 = (160, 170)

while True:
    frame_counter += 1
    captureStatus, startingFrame = capture.read()
    if startingFrame is None:
        break

    leftCut = svo.cut_left(startingFrame)
    # blurred = cv.GaussianBlur(leftCut, (5, 5), 0)
    # blurred = cv.medianBlur(blurred, 5)
    hsvFrame = cv.cvtColor(leftCut, cv.COLOR_BGR2HSV)
    res = svo.get_hsvmask_on_ball(hsvFrame)
    finalFrame = svo.get_knn_on_frame(res)
    returnFrame = cv.cvtColor(finalFrame, cv.COLOR_GRAY2BGR)

    if frame_counter > 10:
        if svo.spotBallOnTop_left(finalFrame):
            top_frame = frame_counter
            print("top FRAME:", frame_counter)
            returnFrame = svo.draw_rectangle(returnFrame, upper_left1, bottom_right1, "green")
        else:
            returnFrame = svo.draw_rectangle(returnFrame, upper_left1, bottom_right1, "red")
        """
        if svo.spotBallOnMedium_left(finalFrame) and 2 < (frame_counter - top_frame) < 8:
            middle_frame = frame_counter
            print("middle FRAME:", frame_counter)
            returnFrame = svo.draw_rectangle(returnFrame, upper_left2, bottom_right2, "green")
        else:
            returnFrame = svo.draw_rectangle(returnFrame, upper_left2, bottom_right2, "red")
        """
        if svo.spotBallOnBottom_left(finalFrame) and 3 < (frame_counter - top_frame) < 25 and (frame_counter - last_score_frame) > 25:
            print("bottom FRAME:", frame_counter)
            print("score")
            last_score_frame = frame_counter
            bottom_frame = frame_counter
            returnFrame = svo.draw_rectangle(returnFrame, upper_left3, bottom_right3, "green")
        else:
            returnFrame = svo.draw_rectangle(returnFrame, upper_left3, bottom_right3, "red")

        if top_frame - last_score_frame <  0 and frame_counter - last_score_frame == 5:
            print("score con precauzione top")


    cv.imshow("returnFrame", returnFrame)
    cv.imshow("originalFrame", leftCut)

    key = cv.waitKey(1)
    if key == 27:
        break

cv.destroyAllWindows()
