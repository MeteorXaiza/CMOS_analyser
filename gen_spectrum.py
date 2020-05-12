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
parser.add_argument(
    '-i', '--event_list_file', help='event list file path (init : None)')
parser.add_argument('-v', '--valid_event', help='valid event condition (init : None)')
parser.add_argument(
    '-ys', '--y_scale', default='log', help='y scale (lin or log) (init : log)')
parser.add_argument(
    '--spectrum_value', default='PHasum',
    help='value drawn as spectrum (init : PHasum)')
parser.add_argument('-b', '--bins', default='arange(ceil(valid_spectrum_value.min())-1, floor(valid_spectrum_value.max()) + 2)', help='bins (init : arange(ceil(valid_spectrum_value.min())-1, floor(valid_spectrum_value.max()) + 2)')
parser.add_argument(
    '--x_label', default='PHasum [ch]', help='x label (init : PHasum [ch])')
parser.add_argument(
    '--y_label', default='intensity [counts/bin]',
    help='y label (init : intensity [counts/bin])')
parser.add_argument(
    '-eth', '--event_th', default='default',
    help='event threshold (init : default)')
parser.add_argument(
    '-sth', '--split_th', default='default',
    help='split threshold (init : default)')
parser.add_argument('--color', default='red', help='color of spectrum curve (init : red)')
parser.add_argument(
    '-ml', '--max_leak', default='default',
    help='max leak calcurating PHasum (init : default)')
parser.add_argument('--mean_BG', help='mean BG file (init : None)')
parser.add_argument('--std_BG', help='std BG file (init : None)')
parser.add_argument('--kurtosis_BG', help='kurtosis BG file (init : None)')
parser.add_argument('-o', '--spectrum_img_file', help='spectrum img file path (output) (init : None)')
parser.add_argument('--spectrum_bin_file', help='spectrum bin file path (output) (init : None)')
args = parser.parse_args()

if args.config_file is not None:
    dicConfig = getDicIni(args.config_file)
else:
    dicConfig = None

strInputEvlistFilePath = getConfig(
    args.event_list_file, ['-i','--event_list_file'], dicConfig, 'input',
    'event_list_file_path')
strValidEventCondition = getConfig(args.valid_event, ['-v','--valid_event'], dicConfig, 'input', 'valid_event')
strYScale = getConfig(args.y_scale, ['-ys','--y_scale'], dicConfig, 'input', 'y_scale')
strSpectrumVal = getConfig(args.spectrum_value, ['--spectrum_value'], dicConfig, 'input', 'spectrum_value')
strBins = getConfig(args.bins, ['-b','--bins'], dicConfig, 'input', 'bins')
strXLabel = getConfig(args.x_label, ['--x_label'], dicConfig, 'input', 'x_label')
strYLabel = getConfig(args.y_label, ['--y_label'], dicConfig, 'input', 'y_label')
strEvent_th = getConfig(args.event_th, ['-eth','--event_th'], dicConfig, 'input', 'event_th')
strSplit_th = getConfig(args.split_th, ['-sth','--split_th'], dicConfig, 'input', 'split_th')
strColor = getConfig(args.color, ['--color'], dicConfig, 'input', 'color')
strMaxLeak = getConfig(args.max_leak, ['-ml','--max_leak'], dicConfig, 'input', 'max_leak')
strMeanBGFilePath = getConfig(args.mean_BG, ['--mean_BG'], dicConfig, 'input', 'mean_BG_file_path')
strStdBGFilePath = getConfig(args.std_BG, ['--std_BG'], dicConfig, 'input', 'std_BG_file_path')
strKurtosisBGFilePath = getConfig(args.kurtosis_BG, ['--kurotsis_BG'], dicConfig, 'input', 'kurtosis_BG_file_path')
strOutputSpectrumImgFilePath = getConfig(args.spectrum_img_file, ['-o','--spectrum_img_file'], dicConfig, 'output', 'spectrum_img_file_path')
strOutputSpectrumBinFilePath = getConfig(args.spectrum_bin_file, ['--spectrum_bin_file'], dicConfig, 'output', 'spectrum_bin_file_path')
if strInputEvlistFilePath is not None:
    dicEvlistData = getArrFits(strInputEvlistFilePath, header=True, message=True)
    arrEvlist = dicEvlistData['data']
    dicEvlistHeader = dicEvlistData['header']
else:
    quit()

if strEvent_th != 'default':
    event_th = float(strEvent_th)
    arrEvlist = arrEvlist[arrEvlist[:,5] >= event_th]
else:
    event_th = float(dicEvlistHeader['EVENT_TH'])

defaultMaxLeak = int(dicEvlistHeader['MAXLEAK'])
if strMaxLeak != 'default':
    maxLeak = int(strMaxLeak)
    if maxLeak < defaultMaxLeak:
        arrEvlist = arrEvlist[:, :(2*maxLeak+1)**2+5]
else:
    maxLeak = defaultMaxLeak

if strSplit_th != 'default':
    if strSplit_th is None:
        split_th = None
    else:
        split_th = float(strSplit_th)
else:
    split_th = float(dicEvlistHeader['SPLIT_TH'])

if strMeanBGFilePath is not None:
    arrMeanBG = getArrFits(strMeanBGFilePath, message=True)
else:
    arrMeanBG = None

if strStdBGFilePath is not None:
    arrStdBG = getArrFits(strStdBGFilePath, message=True)
else:
    arrStdBG = None

if strKurtosisBGFilePath is not None:
    arrKurtosisBG = getArrFits(strKurtosisBGFilePath, message=True)
else:
    arrKurtosisBG = None

arrEvlist[:, 3] = genArrEvlistPHasum(arrEvlist[:,5:], split_th, maxLeak)
arrEvlist[:, 4] = genArrEvlistVortex(arrEvlist[:,5:], split_th)

print('detecting valid event...')
strThisScriptFileDir = os.path.dirname(os.path.abspath(__file__)) + '/'
if strValidEventCondition is None:
    arrEvlistIsValid = np.zeros(arrEvlist.shape[0]) == 0
else:
    lsStrValidEventTxtLine = getLsStrTxtLine(strThisScriptFileDir + 'valid_event_function_0.py')
    lsStrValidEventTxtLine[-2] = '        lsRet.append(' + strValidEventCondition + ')'
    saveAsTxt(lsStrValidEventTxtLine, strThisScriptFileDir+'valid_event_function.py')
    from valid_event_function import *
    arrEvlistIsValid = genArrEvlistIsValid(arrEvlist, event_th, split_th, arrMeanBG, arrStdBG, arrKurtosisBG)
print('finished.')

print('calcurating spectrum value...')
lsStrSpectrumValTxtLine = getLsStrTxtLine(strThisScriptFileDir + 'spectrum_val_function_0.py')
lsStrSpectrumValTxtLine[-2] = '        lsRet.append(' + strSpectrumVal + ')'
saveAsTxt(
    lsStrSpectrumValTxtLine, strThisScriptFileDir+'spectrum_val_function.py')
from spectrum_val_function import *
arrSpectrumVal = genArrSpectrumVal(arrEvlist, split_th, event_th, arrMeanBG, arrStdBG, arrKurtosisBG)
arrValidSpectrumVal = arrSpectrumVal[arrEvlistIsValid]
print('finished.')
print('valid_event_num : ' + str(arrValidSpectrumVal.size))

if strYScale == 'lin':
    strYScale = 'linear'

lsStrBinsTxtLine = getLsStrTxtLine(
    strThisScriptFileDir + 'spectrum_bins_function_0.py')
lsStrBinsTxtLine[-1] = '    return ' + strBins
saveAsTxt(lsStrBinsTxtLine, strThisScriptFileDir+'spectrum_bins_function.py')
from spectrum_bins_function import *
arrBins = genArrBins(arrSpectrumVal, arrValidSpectrumVal)

match = re.match('\((\d+) *, *(\d+) *, *(\d+)\)', strColor)
if match is None:
    color = strColor
else:
    color = tuple(np.array(match.groups()).astype(float) / 255.)

if strOutputSpectrumImgFilePath is not None:
    setHist(arrValidSpectrumVal, bins=arrBins, color=color)
    plt.xlabel(strXLabel)
    plt.ylabel(strYLabel)
    plt.yscale(strYScale)
    plt.savefig(strOutputSpectrumImgFilePath)
    print(strOutputSpectrumImgFilePath + ' has been saved.')

if strOutputSpectrumBinFilePath is not None:
    lsArrHistVal = np.histogram(arrValidSpectrumVal, bins=arrBins)
    arrOutputSpectrumVal = np.zeros((2, lsArrHistVal[1].size))
    arrOutputSpectrumVal[0, :-1] = lsArrHistVal[0]
    arrOutputSpectrumVal[0, -1] = np.nan
    arrOutputSpectrumVal[1] = lsArrHistVal[1]
    saveAsFits(arrOutputSpectrumVal, strOutputSpectrumBinFilePath, message=True)


print('required time : ' + str(time.time() - startTime) + ' sec')
