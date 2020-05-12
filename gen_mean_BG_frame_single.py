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
    '--event_list_file', help='event list file path (init : None)')
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
    '--invalid_shape_process',
    help='invalid shape process (init : first)')
parser.add_argument(
    '-o', '--mean_BG_file', help='mean BG file path(output) (init : None)')
parser.add_argument(
    '--std_BG_file', help='std BG file path(output) (init : None)')
parser.add_argument(
    '--kurtosis_BG_file', help='kurtosis BG file path(output) (init : None)')
args = parser.parse_args()

if args.config_file is not None:
    dicConfig = getDicIni(args.config_file, message=True)
else:
    dicConfig = None

strInputDirPath = getConfig(
    args.input_directory, ['-i','--input_directory'], dicConfig, 'input',
    'directory_path')
strEvlistFilePath = getConfig(
    args.event_list_file, ['--event_list_file'], dicConfig,
    'input', 'event_list_file_path')
strLimitFrameNum = getConfig(
    args.limit_frame_num, ['--limit_frame_num'], dicConfig, 'input', 'limit_frame_num')
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
strMeanBGFilePath = getConfig(
    args.mean_BG_file, ['-o','--mean_BG_file'], dicConfig, 'output',
    'mean_BG_file_path')
strStdBGFilePath = getConfig(
    args.std_BG_file, ['--std_BG_file'], dicConfig, 'output',
    'std_BG_file_path')
strKurtosisBGFilePath = getConfig(
    args.kurtosis_BG_file, ['--kurtosis_BG_file'], dicConfig, 'output',
    'kurtosis_BG_file_path')


strInputDirPath = getStrAbsPath(strInputDirPath)
if strInputDirPath[-1] != '/':
    strInputDirPath += '/'
lsStrFileName = sorted(
    getLsStrFileName(strInputDirPath, match=strMatchFileName))

if strEvlistFilePath is not None:
    strEvlistFilePath = getStrAbsPath(strEvlistFilePath)
    dicEvlistData = getArrFits(strEvlistFilePath, header=True, message=True)
else:
    dicEvlistData = None

if strLimitFrameNum is not None:
    limitFrameNum = int(strLimitFrameNum)
else:
    limitFrameNum = None

HDUIndex = int(strHDUIndex)

tpValidFrameShape = getTpValidFrameShape(
    strValidFrameShape, strInputDirPath, lsStrFileName, HDUIndex)


if dicEvlistData is None:
    arrMeanBG, arrStdBG, arrKurtosisBG, lsStrValidFileName = \
    genLsBGDataWithoutEvlist(strInputDirPath, lsStrFileName, limitFrameNum,
    strMatchFileName, HDUIndex, tpValidFrameShape, strInvalidShapeProcess)
else:
    arrMeanBG, arrStdBG, arrKurtosisBG, lsStrValidFileName = \
    genLsBGDataWithEvlist(
        strInputDirPath, lsStrFileName, dicEvlistData, limitFrameNum, strMatchFileName, HDUIndex,
        tpValidFrameShape, strInvalidShapeProcess)

dicOutputHeader = {}
lsStrKey = ['TYPEVER', 'MODE', 'INPUTDIR', 'EVLIST', 'FRAMENUM', 'HDUINDEX']
lsStrVal = [
    '1.1', 'single', strInputDirPath, strEvlistFilePath,
    str(len(lsStrValidFileName)), str(HDUIndex)
]
for cnt in range(len(lsStrKey)):
    dicOutputHeader[lsStrKey[cnt]] = setHeader(lsStrVal[cnt])

'''
dicOutputHeader['TYPEVER'] = setHeader('1.1')
dicOutputHeader['MODE'] = setHeader('single')
dicOutputHeader['INPUTDIR'] = setHeader(strInputDirPath)
dicOutputHeader['EVLIST'] = setHeader(strEvlistFilePath)
dicOutputHeader['FRAMENUM'] = setHeader(str(len(lsStrValidFileName)))
dicOutputHeader['HDUINDEX'] = setHeader(HDUIndex)
'''
for cnt in range(len(lsStrValidFileName)):
    dicOutputHeader['F' + str(cnt)] = lsStrValidFileName[cnt]

if strMeanBGFilePath is not None:
    dicOutputHeader['FILETYPE'] = setHeader('mean_BG')
    saveAsFits(arrMeanBG, strMeanBGFilePath, header=dicOutputHeader,
        message=True)

if strStdBGFilePath is not None:
    dicOutputHeader['FILETYPE'] = setHeader('std_BG')
    saveAsFits(arrStdBG, strStdBGFilePath, header=dicOutputHeader,
        message=True)

if strKurtosisBGFilePath is not None:
    dicOutputHeader['FILETYPE'] = setHeader('kurtosis_BG')
    saveAsFits(arrKurtosisBG, strKurtosisBGFilePath, header=dicOutputHeader,
        message=True)


print('required time : ' + str(time.time() - startTime) + ' sec')
