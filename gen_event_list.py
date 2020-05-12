# coding:utf-8


import argparse
import re
import time

import numpy as np

from my_functions_2 import *


startTime = time.time()


parser = argparse.ArgumentParser(
    description='generate event list file (fits).')
parser.add_argument(
    '-c', '--config_file', help='config file path (init : None)')
parser.add_argument(
    '-i', '--input_directory', default='./',
    help='input directory path (init : ./)')
parser.add_argument(
    '-th', '--threshold_file', help='threshold ini file path (init:None)')
parser.add_argument(
    '-bg', '--mean_BG_file', help='mean BG file path (init : None)')
parser.add_argument('-eth', '--event_th', help='event threshold (init : None)')
parser.add_argument('-sth', '--split_th', help='split threshold (init : None)')
parser.add_argument(
    '-ml', '--max_leak', default='1', help='max leak (init : 1)')
parser.add_argument(
    '--limit_frame_num', help='limit frame number in analysis (init : None)')
parser.add_argument(
    '--match_file_name', default='.+\.fits',
    help='file name as regular expression (init : .+\\.fits)')
parser.add_argument(
    '--valid_frame_shape',
    help='valid frame shape (init : None)')
parser.add_argument(
    '--HDU_index', default='0',
    help='HDU index containing frame data (init : 0)')
parser.add_argument(
    '--input_event_list_file', help='input event list file path (init : None)')
parser.add_argument(
    '--invalid_shape_process', default='first',
    help='invalid shape process (init : first)')
parser.add_argument(
    '-o', '--event_list_file',
    help='event list file path(output) (init : None)')
args = parser.parse_args()

if args.config_file is not None:
    dicConfig = getDicIni(args.config_file)
else:
    dicConfig = None

strInputDirPath = getConfig(
    args.input_directory, ['-i','--input_directory'], dicConfig, 'input',
    'directory_path')
strThresholdFilePath = getConfig(
    args.threshold_file, ['-th','--threshold_file'], dicConfig, 'input',
    'threshold_file_path')
strMeanBGFilePath = getConfig(
    args.mean_BG_file, ['-bg','--mean_BG_file'], dicConfig, 'input',
    'mean_BG_file_path')
strEvent_th = getConfig(
    args.event_th, ['-eth','--event_th'], dicConfig, 'input', 'event_th')
strSplit_th = getConfig(
    args.split_th, ['-sth','--split_th'], dicConfig, 'input', 'split_th')
strMaxLeak = getConfig(
    args.max_leak, ['-ml','--max_leak'], dicConfig, 'input', 'max_leak')
strLimitFrameNum = getConfig(
    args.limit_frame_num, ['--limit_frame_num'], dicConfig, 'input',
    'limit_frame_num')
strMatchFileName = getConfig(
    args.match_file_name, ['--match_file_name'], dicConfig, 'input',
    'match_file_name')
strValidFrameShape = getConfig(
    args.valid_frame_shape, ['--valid_frame_shape'], dicConfig, 'input',
    'valid_frame_shape')
strHDUIndex = getConfig(
    args.HDU_index, ['--HDU_index'], dicConfig, 'input', 'HDU_index')
strInputEvlistFilePath = getConfig(
    args.input_event_list_file, ['--input_event_list_file'], dicConfig,
    'input', 'event_list_file_path')
strInvalidShapeProcess = getConfig(
    args.invalid_shape_process, ['--invalid_shape_process'], dicConfig, 'input',
    'invalid_shape_process')
strOutputEvlistFilePath = getConfig(
    args.event_list_file, ['-o','--event_list_file'], dicConfig, 'output',
    'event_list_file_path')


strInputDirPath = getStrAbsPath(strInputDirPath)
if strInputDirPath[-1] != '/':
    strInputDirPath += '/'
lsStrFileName = sorted(
    getLsStrFileName(strInputDirPath, match=strMatchFileName))

if strMeanBGFilePath is not None:
    strMeanBGFilePath = getStrAbsPath(strMeanBGFilePath)
    arrMeanBG = getArrFits(strMeanBGFilePath, message=True)
else:
    arrMeanBG = genArrMeanBGFromFrameData(
        strInputDirPath, lsStrFileName, strValidFrameShape, HDUIndex,
        strInvalidShapeProcess)

maxLeak = int(strMaxLeak)

if strLimitFrameNum is not None:
    limitFrameNum = int(strLimitFrameNum)
else:
    limitFrameNum = None

HDUIndex = int(strHDUIndex)

event_th, split_th = getLsThreshold(
    strInputDirPath, strThresholdFilePath, arrMeanBG, strEvent_th, strSplit_th,
    lsStrFileName, HDUIndex)

tpValidFrameShape = getTpValidFrameShape(
    strValidFrameShape, strInputDirPath, lsStrFileName, HDUIndex, arrMeanBG)

if strInputEvlistFilePath is not None:
    strInputEvlistFilePath = getStrAbsPath(strInputEvlistFilePath)
    arrInputEvlist = getArrFits(strInputEvlistFilePath, message=True)
else:
    arrInputEvlist = None


if arrInputEvlist is None:
    arrOutputEvlist, lsStrValidFileName = genLsEventDataWithoutEvlist(
        strInputDirPath, lsStrFileName, event_th, split_th, maxLeak,
        limitFrameNum, HDUIndex, arrMeanBG)


dicOutputHeader = {}
lsStrKey = [
    'FILETYPE', 'TYPEVER', 'MODE', 'INPUTDIR', 'MEANBG', 'EVENT_TH', 'SPLIT_TH',
    'MAXLEAK', 'FRAMENUM', 'HDUINDEX', 'EVLIST'
]
lsStrVal = [
    'event_list', '1.1', 'single', strInputDirPath, strMeanBGFilePath,
    str(event_th), str(split_th), str(maxLeak), str(len(lsStrValidFileName)),
    str(HDUIndex), strInputEvlistFilePath
]
for cnt in range(len(lsStrKey)):
    dicOutputHeader[lsStrKey[cnt]] = setHeader(lsStrVal[cnt])

'''
dicOutputHeader['FILETYPE'] = setHeader('event_list')
dicOutputHeader['TYPEVER'] = setHeader('1.1')
dicOutputHeader['MODE'] = setHeader('single')
dicOutputHeader['INPUTDIR'] = setHeader(strInputDirPath)
dicOutputHeader['MEANBG'] = setHeader(strMeanBGFilePath)
dicOutputHeader['EVENT_TH'] = setHeader(str(event_th))
dicOutputHeader['SPLIT_TH'] = setHeader(str(split_th))
dicOutputHeader['MAXLEAK'] = setHeader(str(maxLeak))
dicOutputHeader['FRAMENUM'] = setHeader(str(len(lsStrValidFileName)))
dicOutputHeader['HDUINDEX'] = setHeader(HDUIndex)
dicOutputHeader['EVLIST'] = setHeader(strInputEvlistFilePath)
'''
for cnt in range(len(lsStrValidFileName)):
    dicOutputHeader['F' + str(cnt)] = lsStrValidFileName[cnt]

saveAsFits(
    arrOutputEvlist, strOutputEvlistFilePath, header=dicOutputHeader,
    message=True)


print('required time : ' + str(time.time() - startTime) + ' sec')
