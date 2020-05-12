# coding:utf-8


import numpy as np


def genArrIsValidPixel(tpValidFrameShape, mean, std, kurtosis):
    arrOnes = np.ones(tpValidFrameShape)
    X = arrOnes * np.arange(tpValidFrameShape[1]).reshape((1,tpValidFrameShape[1]))
    Y = arrOnes * np.arange(tpValidFrameShape[0]).reshape((tpValidFrameShape[0],1))
    return ###function_area###
