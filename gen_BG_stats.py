# coding:utf-8


import argparse
import re
import time
from math import *

import numpy as np

from my_functions_2 import *


startTime = time.time()


parser = argparse.ArgumentParser(
    description='analyse BG and output BG stats parameter(number of sample ,sum, , mean, std, kurtosis, max, min, middle, sum(2, 3, 4)')
parser.add_argument(
    '-c', '--config_file', help='config file path (init : None)')
parser.add_argument(
    '-i', '--input_directory', default='./',
    help='input directory path (init : ./)')
parser.add_argument(
    '-m', '--mean_BG_file', help='mean BG file path (init : None)')
parser.add_argument(
    '-std', '--std_BG_file', help='std BG file path (init : None)')
parser.add_argument(
    '-kurtosis', '--kurtosis_BG_file',
    help='kurtosis BG file path (init : None)')
parser.add_argument(
    '--valid_pixel', help='valid pixel condition (init : None)')
parser.add_argument(
    '--event_list_file', help='event list file path (init : None)')
parser.add_argument(
    '--exclude_rim', default='True',
    help='exclude event mixing rim of frame (init : True)')
parser.add_argument(
    '--limit_frame_num', help='limit frame number in analysis (init : None)')
parser.add_argument(
    '--match_file_name', default='.+\.fits',
    help='file name as regular expression (init : .+\\.fits)')
parser.add_argument(
    '--HDU_index', default='0',
    help='HDU index containing frame data (init : 0)')
parser.add_argument(
    '--valid_frame_shape',
    help='valid frame shape (init : None)')
parser.add_argument(
    '--invalid_shape_process', default='first',
    help='invalid shape process (init : first)')
parser.add_argument(
    '-o', '--BG_stats_file', help='BG stats file path(output) (init : None)')
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
    args.std_BG_file, ['-std','--std_BG_file'], dicConfig, 'input',
    'std_BG_file_path')
strKurtosisBGFilePath = getConfig(
    args.kurtosis_BG_file, ['-kurtosis','--kurtosis_BG_file'], dicConfig, 'input',
    'kurtosis_BG_file_path')
strValidPixelCondition = getConfig(
    args.valid_pixel, ['--valid_pixel'], dicConfig, 'input',
    'valid_pixel')
strEvlistFilePath = getConfig(
    args.event_list_file, ['--event_list_file'], dicConfig,
    'input', 'event_list_file_path')
strExcludeRim = getConfig(
    args.exclude_rim, ['--exclude_rim'], dicConfig,
    'input', 'exclude_rim')
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
strInvalidShapeProcess = getConfig(
    args.invalid_shape_process, ['--invalid_shape_process'], dicConfig, 'input',
    'invalid_shape_process')
strOutputBGStatsFilePath = getConfig(
    args.BG_stats_file, ['-o','--BG_stats_file'], dicConfig, 'output',
    'BG_stats_file_path')

strInputDirPath = getStrAbsPath(strInputDirPath)
if strInputDirPath[-1] != '/':
    strInputDirPath += '/'
lsStrFileName = sorted(
    getLsStrFileName(strInputDirPath, match=strMatchFileName))

if strMeanBGFilePath is not None:
    strMeanBGFilePath = getStrAbsPath(strMeanBGFilePath)
    arrMeanBG = getArrFits(strMeanBGFilePath, message=True)
else:
    arrMeanBG = None

if strStdBGFilePath is not None:
    strStdBGFilePath = getStrAbsPath(strStdBGFilePath)
    arrStdBG = getArrFits(strStdBGFilePath, message=True)
else:
    arrStdBG = None

if strKurtosisBGFilePath is not None:
    strKurtosisBGFilePath = getStrAbsPath(strKurtosisBGFilePath)
    arrKurtosisBG = getArrFits(strKurtosisBGFilePath, message=True)
else:
    arrKurtosisBG = None

if strEvlistFilePath is not None:
    strEvlistFilePath = getStrAbsPath(strEvlistFilePath)
    dicEvlistData = getArrFits(strEvlistFilePath, header=True, message=True)
else:
    dicEvlistData = None

if strExcludeRim != 'True':
    excludeRim = False
else:
    excludeRim = True

if strLimitFrameNum is not None:
    limitFrameNum = int(strLimitFrameNum)
else:
    limitFrameNum = None

HDUIndex = int(strHDUIndex)

tpValidFrameShape = getTpValidFrameShape(
    strValidFrameShape, strInputDirPath, lsStrFileName, HDUIndex, arrMeanBG)

strThisScriptFileDir = os.path.dirname(os.path.abspath(__file__)) + '/'
if strValidPixelCondition not in [None, 'True']:
    lsStrValidPixelTxtLine = getLsStrTxtLine(strThisScriptFileDir + 'valid_pixel_function_0.py')
    lsStrValidPixelTxtLine[-1] = '    return ' + strValidPixelCondition
    saveAsTxt(lsStrValidPixelTxtLine, strThisScriptFileDir+'valid_pixel_function.py')
    from valid_pixel_function import *
    arrIsValidPixel = genArrIsValidPixel(tpValidFrameShape, arrMeanBG, arrStdBG, arrKurtosisBG)
else:
    arrIsValidPixel = np.zeros(tpValidFrameShape) == 0

if dicEvlistData is None:
    dicStrBGStatsParam = genDicStrBGStatsParamWithoutEvlist(
        strInputDirPath, lsStrFileName, arrMeanBG, arrStdBG, arrKurtosisBG,
        arrIsValidPixel, limitFrameNum, strMatchFileName, HDUIndex,
        tpValidFrameShape, strInvalidShapeProcess)
else:
    dicStrBGStatsParam = genDicStrBGStatsParamWithEvlist(
        strInputDirPath, lsStrFileName, arrMeanBG, arrStdBG, arrKurtosisBG,
        arrIsValidPixel, dicEvlistData, excludeRim, limitFrameNum,
        strMatchFileName, HDUIndex, tpValidFrameShape, strInvalidShapeProcess)

if dicConfig is None:
    dicConfig = {'input' : {
        'directory_path' : setHeader(strInputDirPath),
        'mean_BG_file_path' : setHeader(strMeanBGFilePath),
        'std_BG_file_path' : setHeader(strStdBGFilePath),
        'kurtosis_BG_file_path' : setHeader(strKurtosisBGFilePath),
        'valid_pixel' : setHeader(strValidPixelCondition),
        'event_list_file_path' : setHeader(strEvlistFilePath),
        'limit_frame_num' : setHeader(strLimitFrameNum),
        'match_file_name' : setHeader(strMatchFileName),
        'HDU_index' : setHeader(strHDUIndex),
        'valid_frame_shape' : setHeader(strValidFrameShape),
        'invalid_shape_process' : setHeader(strInvalidShapeProcess)
    }}
dicOutput = {
    'config' : dicConfig['input'],
    'stats_data' : dicStrBGStatsParam
}


saveAsIni(dicOutput, strOutputBGStatsFilePath, message=True)


print('required time : ' + str(time.time() - startTime) + ' sec')
