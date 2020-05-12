# coding:utf-8
import numpy as np


def genArrSpectrumVal(arrArrEvlist, split_th, event_th, index, mean_BG, std_BG, kurtosis_BG):
    lsRet = []
    for arrEvlist in arrArrEvlist:
        frame_num, Y, X, PHasum, vortex = arrEvlist[:5]
        Y = int(Y)
        X = int(X)
        PH = arrEvlist[5:]
        lsSpectrumVal = [
            ###function_area###
        ]
        lsRet.append(lsSpectrumVal[index])
    return np.array(lsRet)
