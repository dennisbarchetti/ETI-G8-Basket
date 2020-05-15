import cv2 as cv
import numpy as np
import imutils


class StandardVideoOperations:
    KNN = cv.createBackgroundSubtractorKNN()

    @staticmethod
    def video_cutter(frame_hsv, upper_left, bottom_right):
        rect_frame = frame_hsv[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
        return rect_frame
    
    @staticmethod
    def cut_left(startingFrame):
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
        # 3° 4° quarto
        upper_left = (540, 940)
        bottom_right = (740, 1140)
        leftCut = StandardVideoOperations.video_cutter(startingFrame, upper_left, bottom_right)
        return leftCut

    @staticmethod
    def cut_right(startingFrame):
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
        # 3° 4° quarto
        upper_left = (3225, 900)
        bottom_right = (3425, 1100)
        rightCut = StandardVideoOperations.video_cutter(startingFrame, upper_left, bottom_right)
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
        lower_red = np.array([160, 75, 85])
        upper_red = np.array([180, 255, 255])
        mask = cv.inRange(frame_hsv, lower_red, upper_red)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN,(5, 5), iterations=1)
        mask = cv.dilate(mask, None, iterations=2)
        res = cv.bitwise_and(frame_hsv, frame_hsv, mask=mask)
        return res

    @staticmethod
    def get_knn_on_mask(mask):
        frame_knn = StandardVideoOperations.KNN.apply(mask)
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
        rows = [50, 55, 60]
        return StandardVideoOperations.countWhitePixels(rows, range(90, 150), greyScaleFrame)

    @staticmethod
    def spotBallOnMedium_right(greyScaleFrame):
        rows = [100, 105, 110]
        return StandardVideoOperations.countWhitePixels(rows, range(90, 150), greyScaleFrame)

    @staticmethod
    def spotBallOnBottom_right(greyScaleFrame):
        rows = [160, 165, 170]
        return StandardVideoOperations.countWhitePixels(rows, range(75, 175), greyScaleFrame)

    @staticmethod
    def spotBallOnTop_left(greyScaleFrame):
        rows = [85, 90, 95]
        return StandardVideoOperations.countWhitePixels(rows, range(80, 140), greyScaleFrame)

    @staticmethod
    def spotBallOnMedium_left(greyScaleFrame):
        rows = [125, 130, 135]
        return StandardVideoOperations.countWhitePixels(rows, range(80, 140), greyScaleFrame)

    @staticmethod
    def spotBallOnBottom_left(greyScaleFrame):
        rows = [160, 165, 170]
        return StandardVideoOperations.countWhitePixels(rows, range(70, 160), greyScaleFrame)


svo = StandardVideoOperations()
capture = cv.VideoCapture("/path/tempo.asf")

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
    finalFrame = svo.get_knn_on_mask(res)
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
