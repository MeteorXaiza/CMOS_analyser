# coding:utf-8


import numpy as np
from my_functions_2 import *

def genArrEvlistIsValid(arrEvlist, event_th, split_th, mean_BG, std_BG, kurtosis_BG):
    lsRet = []
    for cnt in range(arrEvlist.shape[0]):
        frame_num = arrEvlist[cnt, 0]
        Y = int(arrEvlist[cnt, 1])
        X = int(arrEvlist[cnt, 2])
        PHasum = arrEvlist[cnt, 3]
        vortex = arrEvlist[cnt, 4]
        PH = arrEvlist[cnt, 5:]
        lsRet.append(###function_area###)
    return np.array(lsRet)
