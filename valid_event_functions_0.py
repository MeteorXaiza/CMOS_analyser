# coding:utf-8


import numpy as np


def genArrEvlistIsValid(arrEvlist, index, event_th, split_th, mean_BG, std_BG, kurtosis_BG):
    lsRet = []
    for cnt in range(arrEvlist.shape[0]):
        frame_num, Y, X, PHasum, vortex = arrEvlist[cnt, :5]
        Y = int(Y)
        X = int(X)
        PH = arrEvlist[cnt, 5:]
        lsIsValid = [
            ###function_area###
        ]
        lsRet.append(lsIsValid[index])
    return np.array(lsRet)
