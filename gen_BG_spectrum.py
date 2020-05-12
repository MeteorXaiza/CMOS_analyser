# coding:utf-8


import argparse
import re
import time
from math import *

import numpy as np

from my_functions_2 import *


startTime = time.time()


parser = argparse.ArgumentParser(
    description='generate mean BG file (fits/csv).')
parser.add_argument(
    '-c', '--config_file', help='config file path (init : None)')
parser.add_argument(
    '-i', '--input_directory', default='./',
    help='input directory path (init : ./)')
parser.add_argument(
    '-m', '--mean_BG_file', help='mean BG file path(output) (init : None)')
parser.add_argument(
    '--std_BG_file', help='std BG file path(output) (init : None)')
parser.add_argument(
    '--kurtosis_BG_file', help='kurtosis BG file path(output) (init : None)')
parser.add_argument(
    '--event_list_file', help='event list file path (init : None)')
parser.add_argument(
    '--exclude_rim',
    default='True', help='exclude_event_mixing_rim_of_frame (init : True)')
parser.add_argument(
    '-st', '--BG_stats_file', help='BG stats file path (init : None)')
parser.add_argument(
    '--valid_pixel', help='valid pixel condition (init : None)')
parser.add_argument(
    '-b', '--bins', default='arange(ceil(min_PH)-1, floor(max_PH) + 2)',
    help='bins (init : arange(ceil(min_PH)-1, floor(max_PH) + 2)')
parser.add_argument(
    '-ys', '--y_scale', default='log', help='y scale (lin or log) (init : log)')
parser.add_argument(
    '--x_label', default='PH [ch]', help='x label (init : PH [ch])')
parser.add_argument(
    '--y_label', default='intensity [counts/bin]',
    help='y label (init : intensity [counts/bin]')
parser.add_argument(
    '--limit_frame_num', help='limit frame number in analysis (init : None)')
parser.add_argument(
    '--match_file_name',
    help='file name as regular expression (init : .+\\.fits)')
parser.add_argument(
    '--HDU_index', default='0',
    help='HDU index containing frame data (init : 0)')
parser.add_argument(
    '--valid_frame_shape',
    help='valid frame shape (init : None)')
parser.add_argument(
    '--color', default='red', help='color of spectrum curve (init : red)')
parser.add_argument(
    '--invalid_shape_process', default='first',
    help='invalid shape process (init : first)')
parser.add_argument(
    '-o', '--BG_spectrum_file',
    help='BG spectrum file path (output) (init : None)')
args = parser.parse_args()

if args.config_file is not None:
    dicConfig = getDicIni(args.config_file, message=True)
else:
    dicConfig = None

strInputDirPath = getConfig(
    args.input_directory, ['-i','--input_directory'], dicConfig, 'input',
    'directory_path')
strMeanBGFilePath = getConfig(
    args.mean_BG_file, ['-m','--mean_BG_file'], dicConfig, 'input',
    'mean_BG_file_path')
strStdBGFilePath = getConfig(
    args.std_BG_file, ['--std_BG_file'], dicConfig, 'input',
    'std_BG_file_path')
strKurtosisBGFilePath = getConfig(
    args.kurtosis_BG_file, ['--kurtosis_BG_file'], dicConfig, 'input',
    'kurtosis_BG_file_path')
strEvlistFilePath = getConfig(
    args.event_list_file, ['--event_list_file'], dicConfig, 'input',
    'event_list_file_path')
strExcludeRim = getConfig(
    args.exclude_rim, ['--exclude_rim'], dicConfig, 'input', 'exclude_rim')
strBGStatsFilePath = getConfig(
    args.BG_stats_file, ['-st','--BG_stats_file'], dicConfig, 'input',
    'BG_stats_file_path')
strValidPixelCondition = getConfig(
    args.valid_pixel, ['--valid_pixel'], dicConfig, 'input',
    'valid_pixel')
strBins = getConfig(args.bins, ['-b','--bins'], dicConfig, 'input', 'bins')
strYScale = getConfig(
    args.y_scale, ['-ys','--y_scale'], dicConfig, 'input', 'y_scale')
strXLabel = getConfig(
    args.x_label, ['--x_label'], dicConfig, 'input', 'x_label')
strYLabel = getConfig(
    args.y_label, ['--y_label'], dicConfig, 'input', 'y_label')
strLimitFrameNum = getConfig(
    args.limit_frame_num, ['--limit_frame_num'], dicConfig, 'input',
    'limit_frame_num')
strMatchFileName = getConfig(
    args.match_file_name, ['--match_file_name'], dicConfig, 'input',
    'match_file_name')
strHDUIndex = getConfig(
    args.HDU_index, ['--HDU_index'], dicConfig, 'input', 'HDU_index')
strValidFrameShape = getConfig(
    args.valid_frame_shape, ['--valid_frame_shape'], dicConfig, 'input',
    'valid_frame_shape')
strColor = getConfig(args.color, ['--color'], dicConfig, 'input', 'color')
strInvalidShapeProcess = getConfig(
    args.invalid_shape_process, ['--invalid_shape_process'], dicConfig, 'input',
    'invalid_shape_process')
strOutputBGSpectrumFilePath = getConfig(
    args.BG_spectrum_file, ['-o','--BG_spectrum_file'], dicConfig, 'output',
    'BG_spectrum_file_path')


if strInputDirPath[-1] != '/':
    strInputDirPath += '/'
lsStrFileName = sorted(
    getLsStrFileName(strInputDirPath, match=strMatchFileName))

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

if strEvlistFilePath is not None:
    dicEvlistData = getArrFits(strEvlistFilePath, header=True, message=True)
else:
    dicEvlistData = None

if strExcludeRim != 'True':
    excludeRim = False
else:
    excludeRim = True

if strYScale == 'lin':
    strYScale = 'linear'

if strLimitFrameNum is not None:
    limitFrameNum = int(strLimitFrameNum)
else:
    limitFrameNum = None

HDUIndex = int(strHDUIndex)

tpValidFrameShape = getTpValidFrameShape(
    strValidFrameShape, strInputDirPath, lsStrFileName, HDUIndex, arrMeanBG)

strThisScriptFileDir = os.path.dirname(os.path.abspath(__file__)) + '/'
if strValidPixelCondition not in [None, 'True']:
    lsStrValidPixelTxtLine = getLsStrTxtLine(
        strThisScriptFileDir + 'valid_pixel_function_0.py')
    lsStrValidPixelTxtLine[-1] = '    return ' + strValidPixelCondition
    saveAsTxt(
        lsStrValidPixelTxtLine, strThisScriptFileDir+'valid_pixel_function.py')
    from valid_pixel_function import *
    arrIsValidPixel = genArrIsValidPixel(
        tpValidFrameShape, arrMeanBG, arrStdBG, arrKurtosisBG)
else:
    arrIsValidPixel = np.zeros(tpValidFrameShape) == 0

if strBGStatsFilePath is not None:
    dicStrBGStsats = getDicIni(strBGStatsFilePath, message=True)['stats_data']
else:
    if dicEvlistData is None:
        dicStrBGStsats = genDicStrBGStatsParamWithoutEvlist(
            strInputDirPath, lsStrFileName, arrMeanBG, arrStdBG, arrKurtosisBG,
            arrIsValidPixel, limitFrameNum, strMatchFileName, HDUIndex,
            tpValidFrameShape, strInvalidShapeProcess)
    else:
        dicStrBGStsats = genDicStrBGStatsParamWithEvlist(
            strInputDirPath, lsStrFileName, arrMeanBG, arrStdBG, arrKurtosisBG,
            arrIsValidPixel, dicEvlistData, excludeRim, limitFrameNum,
            strMatchFileName, HDUIndex, tpValidFrameShape,
            strInvalidShapeProcess)

dicBGStsats = {}
for strKey in dicStrBGStsats.keys():
    dicBGStsats[strKey] = float(dicStrBGStsats[strKey])

lsStrBinsTxtLine = getLsStrTxtLine(
    strThisScriptFileDir + 'BG_spectrum_bins_function_0.py')
lsStrBinsTxtLine[-1] = '    return ' + strBins
saveAsTxt(lsStrBinsTxtLine, strThisScriptFileDir+'BG_spectrum_bins_function.py')
from BG_spectrum_bins_function import *
arrBins = genArrBins(dicBGStsats)
if type(arrBins) in [int, float]:
    maxPH = float(dicBGStsats['max'])
    minPH = float(dicBGStsats['min'])
    arrBins = np.linspace(minPH, maxPH, arrBins)

match = re.match('\((\d+) *, *(\d+) *, *(\d+)\)', strColor)
if match is None:
    color = strColor
else:
    color = tuple(np.array(match.groups()).astype(float) / 255.)


if dicEvlistData is None:
    arrBGSpectrumY = genArrBGSpectrumYWithoutEvlist(
        strInputDirPath, lsStrFileName, arrMeanBG, arrStdBG, arrKurtosisBG,
        arrIsValidPixel, arrBins, limitFrameNum, strMatchFileName, HDUIndex,
        tpValidFrameShape, strInvalidShapeProcess)
else:
    arrBGSpectrumY = genArrBGSpectrumYWithEvlist(
        strInputDirPath, lsStrFileName, arrMeanBG, arrStdBG, arrKurtosisBG,
        arrIsValidPixel, arrBins, dicEvlistData, excludeRim, limitFrameNum,
        strMatchFileName, HDUIndex, tpValidFrameShape, strInvalidShapeProcess)

setHistFromVal(arrBGSpectrumY, arrBins, color=color)
plt.xlabel(strXLabel)
plt.ylabel(strYLabel)
plt.yscale(strYScale)
if re.match('.+\.fits', strOutputBGSpectrumFilePath) is not None:
    saveAsFits(
        [arrBGSpectrumY, arrBins], strOutputBGSpectrumFilePath, divide=True,
        message=True)
else:
    plt.savefig(strOutputBGSpectrumFilePath)


print('required time : ' + str(time.time() - startTime) + ' sec')
