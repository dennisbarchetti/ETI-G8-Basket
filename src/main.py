import cv2 as cv
import numpy as np
import threading
from utilities.StandardVideoOperations import *
from timepy import Timer



def main_left(KNNSX):
    global svo
    global startingFrame
    global leftCut
    global leftResult
    global frame_counter
    global top_frameSX
    #global finalFrame_sx
    # global middle_frameSX
    global last_score_frameSX
    global last_score_frameDX
    global score_SX

    # posizioni dei vari rettangoli che vengono utilizzati nell’analisi
    upper_left1 = (80, 85)
    bottom_right1 = (140, 95)

    # upper_left2 = (80, 125)
    # bottom_right2 = (140, 135)

    upper_left3 = (70, 160)
    bottom_right3 = (160, 170)

    #leftCut= left_cut
    #leftCut = svo.cut_left(startingFrame)  # ritaglio della RoI
    # filtri mediani non utilizzati perché portavano ad errori
    # blurred = cv.GaussianBlur(leftCut, (5, 5), 0)
    # blurred = cv.medianBlur(blurred, 5)
    #hsvFrame = cv.cvtColor(leftCut, cv.COLOR_BGR2HSV)  # conversione in HSV per poter sogliare meglio sulla base del colore della palla
    #res = svo.get_hsvmask_on_ball(hsvFrame)  # esecuzione della sogliatura del colore con valori trovati usando l'euristica
    #finalFrame = svo.get_knn_on_left_frame(res)  # utilizzo della background subtraction KNN per la parte sinistra
    finalFrame = KNNSX
    leftResult = cv.cvtColor(finalFrame, cv.COLOR_GRAY2BGR)  # conversione in BGR per disegnare i rettangoli colorati in base al rilevamento della palla

    if frame_counter > 10:  # per evitare problemi dovuti alla background subtraction sinistra nei primi frame
        if svo.spotBallOnTop_left(finalFrame):  # ricerchiamo la presenza della palla nel rettangolo sopra il canestro
            top_frameSX = frame_counter  # se e' presente salviamo il numero del frame
            print("Top SX, frame:", top_frameSX) # segnaliamo in output il numero del frame in cui la palla e' stata rilevata
            leftResult = svo.draw_rectangle(leftResult, upper_left1, bottom_right1, "green")  # coloriamo il rettangolo di verde
        else:
            leftResult = svo.draw_rectangle(leftResult, upper_left1, bottom_right1, "red")  # altrimenti lasciamo il rettangolo colorato di rosso

        """
        # il rettangolo centrale a livello della retina e' stato provato ma con risultati peggiori in quanto non veniva sempre segnalata la presenza della palla
        # e l'attivazione era dovuta principalmente al movimento retina o a causa del  monitor dietro il canestro (che spesso influisce e causa problemi anche sul rilevamento della palla nel rettangolo sotto il canestro)
        if svo.spotBallOnMedium_left(finalFrame) and 2 < (frame_counter - top_frameSX) < 15:  # ricerchiamo la presenza della palla nel rettangolo a livello della retina
            middle_frameSX = frame_counter  # se e' presente dopo essere stata rilevata nel rettangolo sopra tra 2 e 15 frame prima salviamo il numero del frame
            print("Middle SX, frame:", middle_frameSX)  # segnaliamo in output il numero del frame in cui la palla e' stata rilevata
            leftResult = svo.draw_rectangle(leftResult, upper_left2, bottom_right2, "green")  # coloriamo il rettangolo di verde
        else:
            leftResult = svo.draw_rectangle(leftResult, upper_left2, bottom_right2, "red")  # altrimenti lasciamo il rettangolo colorato di rosso
        """

        if svo.spotBallOnBottom_left(finalFrame) and 3 < (frame_counter - top_frameSX) < 25 and (frame_counter - last_score_frameSX) > 50 and (frame_counter - last_score_frameDX) > 50:  # ricerchiamo la presenza della palla nel rettangolo sotto il canestro
            last_score_frameSX = frame_counter  # se e' presente dopo essere stata rilevata nel rettangolo sopra tra 3 e 25 frame prima e l’ultimo score e' stato segnato almeno 50 frame fa salviamo il numero del frame
            score_SX +=1  # incremento del contatore del numero di canetri rilevati a sinistra
            print("Score SX numero", score_SX, "al frame:", last_score_frameSX)  # segnaliamo in output il frame attuale a cui e' stato rilevato il canestro sinistro
            leftResult = svo.draw_rectangle(leftResult, upper_left3, bottom_right3, "green")  # coloriamo il rettangolo di verde
        else:
            leftResult = svo.draw_rectangle(leftResult, upper_left3, bottom_right3, "red")  # altrimenti lasciamo il rettangolo colorato di rosso

        # questa parte e' stata utilizzata per valutare che non venisse segnalata nuovamente la presenza della palla nel rettangolo in alto
        if top_frameSX - last_score_frameSX <  0 and frame_counter - last_score_frameSX == 5:  # effettuiamo un controllo 5 frame dopo che e' stato segnalato il canestro per valutare se la palla e' stata rilevata nuovamente
            print("Score SX numero", score_SX, "con precauzione top")  # se la condizione e' verificata segnaliamo in output che il canestro e' stato segnato con una ulteriore precauzione


def main_right(KNNDX):
    global svo
    global startingFrame
    global rightCut
    global rightResult
    global frame_counter
    global top_frameDX
    # global middle_frameDX
    global last_score_frameDX
    global last_score_frameSX
    global score_DX

    # posizioni dei vari rettangoli che vengono utilizzati nell’analisi
    upper_left1 = (90, 50)
    bottom_right1 = (150, 60)

    # upper_left2 = (90, 100)
    # bottom_right2 = (150, 110)

    upper_left3 = (75, 160)
    bottom_right3 = (175, 170)

    #rightCut = svo.cut_right(startingFrame)  # ritaglio della RoI
    # filtri mediani non utilizzati perché portavano ad errori
    # blurred = cv.GaussianBlur(rightCut, (5, 5), 0)
    # blurred = cv.medianBlur(blurred, 5)
    #hsvFrame = cv.cvtColor(rightCut, cv.COLOR_BGR2HSV)  # conversione in HSV per poter sogliare meglio sulla base del colore della palla
    #res = svo.get_hsvmask_on_ball(hsvFrame)  # esecuzione della sogliatura del colore con valori trovati usando l'euristica
    #finalFrame = svo.get_knn_on_right_frame(res)  # utilizzo della background subtraction KNN per la parte sinistra
    finalFrame = KNNDX
    rightResult = cv.cvtColor(finalFrame, cv.COLOR_GRAY2BGR)  # conversione in BGR per disegnare i rettangoli colorati in base al rilevamento della palla

    if frame_counter > 10:  # per evitare problemi dovuti alla background subtraction destra nei primi frame
        if svo.spotBallOnTop_right(finalFrame):  # ricerchiamo la presenza della palla nel rettangolo sopra il canestro
            top_frameDX = frame_counter  # se e' presente salviamo il numero del frame
            print("Top DX, frame:", top_frameDX)  # segnaliamo in output il numero del frame in cui la palla e' stata rilevata
            rightResult = svo.draw_rectangle(rightResult, upper_left1, bottom_right1, "green")  # coloriamo il rettangolo di verde
        else:
            rightResult = svo.draw_rectangle(rightResult, upper_left1, bottom_right1, "red")  # altrimenti lasciamo il rettangolo colorato di rosso

        """
        # il rettangolo centrale a livello della retina e' stato provato ma con risultati peggiori in quanto non veniva sempre segnalata la presenza della palla
        # e l'attivazione era dovuta principalmente al movimento retina o a causa del  monitor dietro il canestro (che spesso influisce e causa problemi anche sul rilevamento della palla nel rettangolo sotto il canestro)
        if svo.spotBallOnMedium_right(finalFrame)  and 2 < (frame_counter - top_frameDX) < 15:  # ricerchiamo la presenza della palla nel rettangolo a livello della retina 
            middle_frameDX = frame_counter  # se e' presente dopo essere stata rilevata nel rettangolo sopra tra 2 e 15 frame prima salviamo il numero del frame
            print("Middle DX, frame:", middle_frameDX)  # segnaliamo in output il numero del frame in cui la palla e' stata rilevata
            rightResult = svo.draw_rectangle(returnFrame, upper_left2, bottom_right2, "green")  # coloriamo il rettangolo di verde
        else:
            rightResult = svo.draw_rectangle(returnFrame, upper_left2, bottom_right2, "red")  # altrimenti lasciamo il rettangolo colorato di rosso
        """

        if svo.spotBallOnBottom_right(finalFrame) and 3 < (frame_counter - top_frameDX) < 25 and (frame_counter - last_score_frameDX) > 50 and (frame_counter - last_score_frameSX) > 50 :  # ricerchiamo la presenza della palla nel rettangolo sotto il canestro
            last_score_frameDX = frame_counter  # se e' presente dopo essere stata rilevata nel rettangolo sopra tra 3 e 25 frame prima e l’ultimo score e' stato segnato almeno 50 frame fa salviamo il numero del frame
            score_DX +=1  # incremento del contatore del numero di canetri rilevati a destra
            print("Score DX numero", score_DX, "al frame:", last_score_frameDX)  # segnaliamo in output il frame attuale a cui e' stato rilevato il canestro destro
            rightResult = svo.draw_rectangle(rightResult, upper_left3, bottom_right3, "green")  # coloriamo il rettangolo di verde
        else:
            rightResult = svo.draw_rectangle(rightResult, upper_left3, bottom_right3, "red")  # altrimenti lasciamo il rettangolo colorato di rosso

        # questa parte e' stata utilizzata per valutare che non venisse segnalata nuovamente la presenza della palla nel rettangolo in alto
        if top_frameDX - last_score_frameDX <  0 and frame_counter - last_score_frameDX == 5:  # effettuiamo un controllo 5 frame dopo che e' stato segnalato il canestro per valutare se la palla e' stata rilevata nuovamente
            print("Score DX numero", score_DX, "con precauzione top")  # se la condizione e' verificata segnaliamo in output che il canestro e' stato segnato con una ulteriore precauzione


if __name__ == "__main__":

    t = Timer()
    t.start()

    svo = StandardVideoOperations()  # istanza della nostra classe per eseguire le varie operazioni
    capture = cv.VideoCapture("/home/dennis/Video/BASKET/tripla.asf")  # rileva dal percorso fornito il video da analizzare


    svo.display_color_suggestion()
    color=svo.color_calibration() #ricavo i valori per la sogliatura hsv
    """
    color_lower = np.array([160, 75, 85])
    color_upper = np.array([180, 255, 255])
    color = (color_lower,color_upper)

    """

    # dato lo spostamento della videocamera le coordinate cambiano il base al quarto di gioco preso in analisi
    # da impostare per il 1° quarto
    # svo.set_left((455, 955), (655, 1155))
    # svo.set_right((3145, 895), (3345, 1095))

    # da impostare per il 2° quarto
    # svo.set_left((485, 950), (685, 1150))
    # svo.set_right((3185, 900), (3385, 1100))

    # da impostare per il 3° e il 4° quarto
    svo.set_left((540, 940), (740, 1140))
    svo.set_right((3225, 900), (3425, 1100))

    if not capture.isOpened:  # verifica la corretta apertura del video
        print("Unable to open")
        exit(0)

    # indicatori dei frame che saranno utili nell’analisi
    frame_counter = 0
    top_frameSX = 0
    top_frameDX = 0
    # middle_frameSX = 0
    # middle_frameDX = 0
    last_score_frameSX = 0
    last_score_frameDX = 0
    score_DX = 0
    score_SX = 0

    #PREPARAZIONE OPTICAL FLOW
    ret, first_frame = capture.read()
    first_cut_frame = svo.cut_frame(first_frame)
    hsvFrame = svo.hsv_thresholding(first_cut_frame,color)
    prev_gray = svo.change_color_space(first_cut_frame)
    masksx = np.zeros_like(first_cut_frame[0])
    maskdx = np.zeros_like(first_cut_frame[1])
    masksx[..., 1] = 255
    maskdx[..., 1] = 255

    while True:
        captureStatus, startingFrame = capture.read()  # lettura di un frame del video
        if startingFrame is None:  # interruzione del ciclo alla conclusione del video
            break

        frame_counter += 1  #incremento per avere un indicatore del numero di frame corrente

        # copia del frame del video per eseguire le operazioni nei thread e alla fine riportare i risultati

        cut = svo.cut_frame(startingFrame.copy())
        cutsx = cut[0]
        cutdx = cut[1]

        leftCut = cutsx
        rightCut = cutdx
        leftResult = cutsx
        rightResult = cutdx

        cut_hsv = svo.hsv_thresholding(cut,color)
        cut_knn = svo.get_knn_on_frame(cut_hsv)

        #TEST OPTICAL FLOW
        frame2 = cut
        gray = svo.change_color_space(cut)

        """
        flowsx = cv.calcOpticalFlowFarneback(prev_gray[0], gray[0],None,0.5, 3, 15, 3, 5, 1.2, 0)
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
        """
        masks = svo.cumpute_denseOpticalFlow(prev_gray,gray,masksx,maskdx)

        rgbsx = cv.cvtColor(masks[0], cv.COLOR_HSV2BGR)
        rgbdx = cv.cvtColor(masks[1], cv.COLOR_HSV2BGR)

        # Updates previous frame
        prev_gray = gray

        # inizio processing del frame per la parte sinistra e destra in parallelo su due thread
        thread_left = threading.Thread(target=main_left,args=[cut_knn[0]])
        thread_left.start()

        thread_right = threading.Thread(target=main_right,args=[cut_knn[1]])
        thread_right.start()

        # attendo la fine del processing sul frame e riportiamo a monitor i sultati sulla RoI dopo l’analisi e anche del video originale per visualizzare come l’algoritmo sta svolgendo il proprio lavoro
        thread_left.join()
        cv.imshow("originalFrameSX", leftCut)
        cv.imshow("returnFrameSX", leftResult)
        cv.imshow("dense optical flow_sx", rgbsx)

        thread_right.join()
        cv.imshow("originalFrameDX", rightCut)
        cv.imshow("returnFrameDX", rightResult)
        cv.imshow("dense optical flow_dx", rgbdx)

        key = cv.waitKey(1)  # attesa minima tra un frame e il successivo, ma può essere prolungata per visualizzare più lentamente l’esecuzione dell’algoritmo e capire la cause di eventuali problematiche
        if key == 27:  # per ogni evenienza se viene premuto esc si interrompe l’esecuzione
            break

    print("Score SX effettuati", score_SX)  # riportiamo il numero complessivo di canestri rilevati a sinistra
    print("Score DX effettuati", score_DX)  # riportiamo il numero complessivo di canestri rilevati a destra
    cv.destroyAllWindows()  # alla fine dell’esecuzione rimuove tutte le finestre dei frame dallo schermo

    t.stop()
    print("tempo totale esecuzione programma [s]: ",t.total_time)

