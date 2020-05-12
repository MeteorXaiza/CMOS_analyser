# coding:utf-8
from numpy import *


def genArrBins(spectrum_value, valid_spectrum_value):
    return arange(ceil(spectrum_value.min())-1, floor(spectrum_value.max()) + 2)