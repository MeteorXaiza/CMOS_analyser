# coding:utf-8

from math import *
import argparse
import os
import time

import numpy as np

from my_functions_2 import *


startTime = time.time()


parser = argparse.ArgumentParser(
    description='generate spectrm image (png).')
parser.add_argument(
    '-c', '--config_file', help='config file path (init : None)')
parser.add_argument('-o', '--spectrum_file', help='spectrum file path (output) (init : None)')
args = parser.parse_args()

if args.config_file is not None:
    dicConfig = getDicIni(args.config_file)
else:
    print('config file is None')
    quit()

strOutputSpectrumFilePath = getConfig(
    args.spectrum_file, ['-o','--spectrum_file'], dicConfig, 'output',
    'spectrum_file_path')

if dicConfig['input']['auto_color_set'] != 'True':
    autoColorSet = False
else:
    autoColorSet = True

lsStrConfigFilePath = []
for cnt in range(len(dicConfig['input'])):
    strParamName = 'config_file_' + str(cnt+1)
    if strParamName in dicConfig['input'].keys():
        lsStrConfigFilePath.append(dicConfig['input'][strParamName])
    else:
        break


lsStrInputEvlistFilePath, lsStrValidEventCondition, lsStrYScale, lsStrSpectrumVal, lsStrBins, lsStrXLabel, lsStrYLabel, lsStrLabel, lsStrEvent_th, lsStrSplit_th, lsStrColor, lsStrMeanBGFilePath, lsStrStdBGFilePath, lsStrKurtosisBGFilePath, lsStrMaxLeak = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
for strConfigFilePath in lsStrConfigFilePath:
    dicConfig = getDicIni(strConfigFilePath)
    lsStrInputEvlistFilePath.append(getConfig(None, [], dicConfig, 'input', 'event_list_file_path'))
    lsStrValidEventCondition.append(getConfig(None, [], dicConfig, 'input', 'valid_event'))
    lsStrYScale.append(getConfig(None, [], dicConfig, 'input', 'y_scale', stringNone=False))
    lsStrSpectrumVal.append(getConfig('PHasum', [], dicConfig, 'input', 'spectrum_value'))
    lsStrBins.append(getConfig(None, [], dicConfig, 'input', 'bins', stringNone=False))
    lsStrXLabel.append(getConfig(None, [], dicConfig, 'input', 'x_label', stringNone=False))
    lsStrYLabel.append(getConfig(None, [], dicConfig, 'input', 'y_label', stringNone=False))
    lsStrLabel.append(getConfig(None, [], dicConfig, 'input', 'label'))
    lsStrEvent_th.append(getConfig('default', [], dicConfig, 'input', 'event_th'))
    lsStrSplit_th.append(getConfig('default', [], dicConfig, 'input', 'split_th'))
    lsStrColor.append(getConfig('red', [], dicConfig, 'input', 'color'))
    lsStrMaxLeak.append(getConfig('default', [], dicConfig, 'input', 'max_leak'))
    lsStrMeanBGFilePath.append(getConfig(None, [], dicConfig, 'input', 'mean_BG_file_path'))
    lsStrStdBGFilePath.append(getConfig(None, [], dicConfig, 'input', 'std_BG_file_path'))
    lsStrKurtosisBGFilePath.append(getConfig(None, [], dicConfig, 'input', 'kurtosis_BG_file_path'))

arrStrYScale = np.array(lsStrYScale)
if (arrStrYScale == None).all():
    strYScale = 'log'
else:
    strYScale = arrStrYScale[arrStrYScale != None][0]
if strYScale == 'lin':
    strYScale = 'linear'

arrStrBins = np.array(lsStrBins)
if (arrStrBins == None).all():
    strBins = None
else:
    strBins = arrStrBins[arrStrBins != None][0]
    if strBins == 'None':
        strBins = None

arrStrXLabel = np.array(lsStrXLabel)
if (arrStrXLabel == None).all():
    strXLabel = 'PHasum'
else:
    strXLabel = arrStrXLabel[arrStrXLabel != None][0]

arrStrYLabel = np.array(lsStrYLabel)
if (arrStrYLabel == None).all():
    strYLabel = 'counts/bin'
else:
    strYLabel = arrStrYLabel[arrStrYLabel != None][0]


strThisScriptFileDir = os.path.dirname(os.path.abspath(__file__)) + '/'

lsStrValidEventTxtLine = getLsStrTxtLine(strThisScriptFileDir + 'valid_event_functions_0.py')
lsStrValidEventTxtLine.pop(-4)
for strValidEventCondition in lsStrValidEventCondition:
    if strValidEventCondition is None:
        strValidEventCondition = 'True'
    lsStrValidEventTxtLine.insert(-3, '    ' * 3 + strValidEventCondition + ',')
lsStrValidEventTxtLine[-4] = lsStrValidEventTxtLine[-4][:-1]
saveAsTxt(lsStrValidEventTxtLine, strThisScriptFileDir+'valid_event_functions.py')
from valid_event_functions import *

lsStrSpectrumValTxtLine = getLsStrTxtLine(strThisScriptFileDir + 'spectrum_val_functions_0.py')
lsStrSpectrumValTxtLine.pop(-4)
for strSpectrumVal in lsStrSpectrumVal:
    lsStrSpectrumValTxtLine.insert(-3, '    ' * 3 + strSpectrumVal + ',')
lsStrSpectrumValTxtLine[-4] = lsStrSpectrumValTxtLine[-4][:-1]
saveAsTxt(lsStrSpectrumValTxtLine, strThisScriptFileDir+'spectrum_val_functions.py')
from spectrum_val_functions import *

lsArrSpectrumVal, lsArrValidSpectrumVal, lsColor = [], [], []
for cnt in range(len(lsStrInputEvlistFilePath)):
    print('set' + str(cnt) + ' : ' + lsStrConfigFilePath[cnt])
    strInputEvlistFilePath = lsStrInputEvlistFilePath[cnt]
    if strInputEvlistFilePath is not None:
        dicEvlistData = getArrFits(strInputEvlistFilePath, header=True, message=True)
        arrEvlist = dicEvlistData['data']
        dicEvlistHeader = dicEvlistData['header']
    else:
        quit()

    strEvent_th = lsStrEvent_th[cnt]
    if strEvent_th != 'default':
        event_th = float(strEvent_th)
        arrEvlist = arrEvlist[arrEvlist[:,5] >= event_th]
    else:
        event_th = float(dicEvlistHeader['EVENT_TH'])

    strMaxLeak = lsStrMaxLeak[cnt]
    if strMaxLeak != 'default':
        maxLeak = int(strMaxLeak)
        arrEvlist = arrEvlist[:, :(2*maxLeak+1)**2+5]
    else:
        maxLeak = int(dicEvlistHeader['MAXLEAK'])

    strSplit_th = lsStrSplit_th[cnt]
    if strSplit_th != 'default':
        if strSplit_th is None:
            split_th = None
        else:
            split_th = float(strSplit_th)
    else:
        split_th = float(dicEvlistHeader['SPLIT_TH'])

    strMeanBGFilePath = lsStrMeanBGFilePath[cnt]
    if strMeanBGFilePath is not None:
        arrMeanBG = getArrFits(strMeanBGFilePath, message=True)
    else:
        arrMeanBG = None

    strStdBGFilePath = lsStrStdBGFilePath[cnt]
    if strStdBGFilePath is not None:
        arrStdBG = getArrFits(strStdBGFilePath, message=True)
    else:
        arrStdBG = None

    strKurtosisBGFilePath = lsStrKurtosisBGFilePath[cnt]
    if strKurtosisBGFilePath is not None:
        arrKurtosisBG = getArrFits(strKurtosisBGFilePath, message=True)
    else:
        arrKurtosisBG = None

    arrEvlist[:, 3] = genArrEvlistPHasum(arrEvlist[:,5:], split_th, maxLeak)
    arrEvlist[:, 4] = genArrEvlistVortex(arrEvlist[:,5:], split_th)

    print('detecting valid event...')
    arrEvlistIsValid = genArrEvlistIsValid(arrEvlist, cnt, event_th, split_th, arrMeanBG, arrStdBG, arrKurtosisBG)
    print('finished.')
    print('calcurating spectrum value...')
    arrSpectrumVal = genArrSpectrumVal(arrEvlist, split_th, event_th, cnt, arrMeanBG, arrStdBG, arrKurtosisBG)
    print('finished.')
    arrValidSpectrumVal = arrSpectrumVal[arrEvlistIsValid]
    print('valid_event_num : ' + str(arrValidSpectrumVal.size))
    lsArrSpectrumVal.append(arrSpectrumVal)
    lsArrValidSpectrumVal.append(arrValidSpectrumVal)

    strColor = lsStrColor[cnt]
    match = re.match('\((\d+) *, *(\d+) *, *(\d+)\)', strColor)
    if match is None:
        color = strColor
    else:
        color = tuple(np.array(match.groups()).astype(float) / 255.)
    lsColor.append(color)
    print('')

lsStrBinsTxtLine = getLsStrTxtLine(strThisScriptFileDir + 'spectrum_bins_function_0.py')
lsStrBinsTxtLine[-1] = '    return ' + strBins
saveAsTxt(lsStrBinsTxtLine, strThisScriptFileDir+'spectrum_bins_function.py')
from spectrum_bins_function import *
numSpectrumVal, numValidSpectrumVal = 0, 0
for cnt in range(len(lsArrSpectrumVal)):
    numSpectrumVal += lsArrSpectrumVal[cnt].size
    numValidSpectrumVal += lsArrValidSpectrumVal[cnt].size
arrSpectrumVal = np.zeros(numSpectrumVal)
arrValidSpectrumVal = np.zeros(numValidSpectrumVal)
numSpectrumVal, numValidSpectrumVal = 0, 0
for cnt in range(len(lsArrSpectrumVal)):
    arrSpectrumVal[numSpectrumVal : numSpectrumVal+lsArrSpectrumVal[cnt].size] = lsArrSpectrumVal[cnt]
    arrValidSpectrumVal[numValidSpectrumVal : numValidSpectrumVal+lsArrValidSpectrumVal[cnt].size] = lsArrValidSpectrumVal[cnt]
    numSpectrumVal += lsArrSpectrumVal[cnt].size
    numValidSpectrumVal += lsArrValidSpectrumVal[cnt].size
arrBins = genArrBins(arrSpectrumVal, arrValidSpectrumVal)

if autoColorSet:
    arrColor = genArrHueCircle(np.linspace(0,2*pi,len(lsArrValidSpectrumVal)+1))[:-1] / 255.
else:
    arrColor = np.array(lsColor)

for cnt in range(len(lsArrValidSpectrumVal)):
    setHist(lsArrValidSpectrumVal[-cnt-1], bins=arrBins, color=arrColor[-cnt-1], label=lsStrLabel[-cnt-1])
plt.xlabel(strXLabel)
plt.ylabel(strYLabel)
plt.yscale(strYScale)
setLegend()

plt.savefig(strOutputSpectrumFilePath)


print('required time : ' + str(time.time() - startTime) + ' sec')
