# coding:utf-8
import numpy


def genArrSpectrumVal(arrArrEvlist, event_th, split_th, mean_BG, std_BG, kurtosis_BG):
    lsRet = []
    for arrEvlist in arrArrEvlist:
        frame_num, Y, X, PHasum, vortex = arrEvlist[:5]
        Y = int(Y)
        X = int(X)
        PH = arrEvlist[5:]
        lsRet.append(###function_area###)
    return numpy.array(lsRet)
