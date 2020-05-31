import cv2 as cv
import numpy as np
import threading
from utilities.StandardVideoOperations import *


def main_left():
    global svo
    global startingFrame
    global frame_counter
    global top_frameSX
    # global middle_frameSX
    global last_score_frameSX
    global last_score_frameDX
    global leftCut
    global leftResult

    upper_left1 = (80, 85)
    bottom_right1 = (140, 95)

    upper_left2 = (80, 125)
    bottom_right2 = (140, 135)

    upper_left3 = (70, 160)
    bottom_right3 = (160, 170)

    leftCut = svo.cut_left(startingFrame)
    # blurred = cv.GaussianBlur(leftCut, (5, 5), 0)
    # blurred = cv.medianBlur(blurred, 5)
    hsvFrame = cv.cvtColor(leftCut, cv.COLOR_BGR2HSV)
    res = svo.get_hsvmask_on_ball(hsvFrame)
    finalFrame = svo.get_knn_on_left_frame(res)
    leftResult = cv.cvtColor(finalFrame, cv.COLOR_GRAY2BGR)

    if frame_counter > 10:
        if svo.spotBallOnTop_left(finalFrame):
            top_frameSX = frame_counter
            print("top FRAME SX:", top_frameSX)
            leftResult = svo.draw_rectangle(leftResult, upper_left1, bottom_right1, "green")
        else:
            leftResult = svo.draw_rectangle(leftResult, upper_left1, bottom_right1, "red")

        """
        if svo.spotBallOnMedium_left(finalFrame) and 2 < (frame_counter - top_frameSX) < 8:
            middle_frameSX = frame_counter
            print("middle FRAME:", middle_frameSX)
            leftResult = svo.draw_rectangle(leftResult, upper_left2, bottom_right2, "green")
        else:
            leftResult = svo.draw_rectangle(leftResult, upper_left2, bottom_right2, "red")
        """

        if svo.spotBallOnBottom_left(finalFrame) and 3 < (frame_counter - top_frameSX) < 25 and (frame_counter - last_score_frameSX) > 50 and (frame_counter - last_score_frameDX) > 50:
            last_score_frameSX = frame_counter
            print("score SX:", last_score_frameSX)
            leftResult = svo.draw_rectangle(leftResult, upper_left3, bottom_right3, "green")
        else:
            leftResult = svo.draw_rectangle(leftResult, upper_left3, bottom_right3, "red")

        if top_frameSX - last_score_frameSX <  0 and frame_counter - last_score_frameSX == 5:
            print("scoreSX con precauzione top")


def main_right():
    global svo
    global startingFrame
    global frame_counter
    global top_frameDX
    # global middle_frameDX
    global last_score_frameDX
    global last_score_frameSX
    global rightCut
    global rightResult

    upper_left1 = (90, 50)
    bottom_right1 = (150, 60)

    upper_left2 = (90, 100)
    bottom_right2 = (150, 110)

    upper_left3 = (75, 160)
    bottom_right3 = (175, 170)

    rightCut = svo.cut_right(startingFrame)
    # blurred = cv.GaussianBlur(rightCut, (5, 5), 0)
    # blurred = cv.medianBlur(blurred, 5)
    hsvFrame = cv.cvtColor(rightCut, cv.COLOR_BGR2HSV)
    res = svo.get_hsvmask_on_ball(hsvFrame)
    finalFrame = svo.get_knn_on_right_frame(res)
    rightResult = cv.cvtColor(finalFrame, cv.COLOR_GRAY2BGR)

    if frame_counter > 10:
        if svo.spotBallOnTop_right(finalFrame):
            top_frameDX = frame_counter
            print("top FRAME DX:", top_frameDX)
            rightResult = svo.draw_rectangle(rightResult, upper_left1, bottom_right1, "green")
        else:
            rightResult = svo.draw_rectangle(rightResult, upper_left1, bottom_right1, "red")

        """
        if svo.spotBallOnMedium_right(finalFrame)  and 2 < (frame_counter - top_frameDX) < 8:
            middle_frameDX = frame_counter
            print("middle FRAME:", middle_frameDX)
            rightResult = svo.draw_rectangle(returnFrame, upper_left2, bottom_right2, "green")
        else:
            rightResult = svo.draw_rectangle(returnFrame, upper_left2, bottom_right2, "red")
        """
        
        if svo.spotBallOnBottom_right(finalFrame) and 3 < (frame_counter - top_frameDX) < 25 and (frame_counter - last_score_frameDX) > 50 and (frame_counter - last_score_frameSX) > 50:
            last_score_frameDX = frame_counter
            print("score DX:", last_score_frameDX)
            rightResult = svo.draw_rectangle(rightResult, upper_left3, bottom_right3, "green")
        else:
            rightResult = svo.draw_rectangle(rightResult, upper_left3, bottom_right3, "red")

        if top_frameDX - last_score_frameDX <  0 and frame_counter - last_score_frameDX == 5:
            print("scoreDX con precauzione top")


if __name__ == "__main__":

    svo = StandardVideoOperations()
    capture = cv.VideoCapture("/path/video.asf")
    
    # set for 1° quarter
    # svo.set_left((455, 955), (655, 1155))
    # svo.set_right((3145, 895), (3345, 1095))

    # set for 2° quarter
    # svo.set_left((485, 950), (685, 1150))
    # svo.set_right((3185, 900), (3385, 1100))

    # set for 3° 4° quarter
    # svo.set_left((540, 940), (740, 1140))
    # svo.set_right((3225, 900), (3425, 1100))

    if not capture.isOpened:
        print('Unable to open')
        exit(0)

    frame_counter = 0
    top_frameSX = 0
    top_frameDX = 0
    # middle_frameSX = 0
    # middle_frameDX = 0
    last_score_frameSX = 0
    last_score_frameDX = 0

    while True:
        frame_counter += 1
        captureStatus, startingFrame = capture.read()
        if startingFrame is None:
            break

        leftCut = startingFrame.copy()
        rightCut = startingFrame.copy()
        leftResult = startingFrame.copy()
        rightResult = startingFrame.copy()
        
        thread_left = threading.Thread(target=main_left)
        thread_left.start()
        
        thread_right = threading.Thread(target=main_right)
        thread_right.start()
        
        thread_left.join()
        cv.imshow("originalFrameSX", leftCut)
        cv.imshow("returnFrameSX", leftResult)
        
        thread_right.join()
        cv.imshow("originalFrameDX", rightCut)
        cv.imshow("returnFrameDX", rightResult)
        
        key = cv.waitKey(1)
        if key == 27:
            break

    cv.destroyAllWindows()
