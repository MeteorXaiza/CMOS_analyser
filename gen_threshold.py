# coding:utf-8


import argparse
from math import *
import time

import numpy as np
from scipy.stats import norm
from scipy.stats import t as student_t

from my_functions_2 import *


startTime = time.time()


parser = argparse.ArgumentParser(
    description='generate threshold file (ini).')
parser.add_argument(
    '-c', '--config_file', help='config file path (init : None)')
parser.add_argument(
    '-i', '--BG_stats_file', help='BG stats file path (init : None)')
parser.add_argument(
    '-m', '--threshold_mode', default='default',
    help='threshold mode (init : default)')
parser.add_argument(
    '--false_event_rareness', default='1',
    help='false_event_rareness (init : 1)')
parser.add_argument(
    '-o', '--threshold_file', help='threshold_file_path (init : None)')

args = parser.parse_args()

if args.config_file is not None:
    dicConfig = getDicIni(args.config_file)
else:
    dicConfig = None

strBGStatsFilePath = getConfig(
    args.BG_stats_file, ['-i','--BG_stats_file'], dicConfig, 'input',
    'BG_stats_file_path')
strThresholdMode = getConfig(
    args.threshold_mode, ['-m','--threshold_mode'], dicConfig, 'input',
    'threshold_mode')
strFalseEventRareness = getConfig(
    args.false_event_rareness, ['--false_event_rareness'], dicConfig, 'input',
    'false_event_rareness')
strOutputThresholdFilePath = getConfig(
    args.threshold_file, ['-o','--threshold_file'], dicConfig, 'output',
    'threshold_file_path')


if strBGStatsFilePath is not None:
    dicStrBGStsats = getDicIni(strBGStatsFilePath, message=True)['stats_data']
else:
    quit()

dicBGStsats = {}
for strKey in dicStrBGStsats.keys():
    dicBGStsats[strKey] = float(dicStrBGStsats[strKey])

if strThresholdMode in ['default']:
    event_th = 10. * dicBGStsats['std']
    split_th = 3. * dicBGStsats['std']
elif strThresholdMode in ['t', 'student_t']:
    falseEventRareness = float(strFalseEventRareness)
    nu = 6. / dicBGStsats['kurtosis'] + 4
    sigma = sqrt((nu - 2) / (nu)) * dicBGStsats['std']
    event_th = student_t.isf(
        1./(falseEventRareness*dicBGStsats['frame_X']*dicBGStsats['frame_Y']),
        df=nu, loc=0, scale=sigma)
    split_th = student_t.isf(norm.sf(3), df=nu, loc=0, scale=sigma)

dicOutput = {'threshold' : {
    'event_th' : str(event_th),
    'split_th' : str(split_th)
}}

saveAsIni(dicOutput, strOutputThresholdFilePath, message=True)


print('required time : ' + str(time.time() - startTime) + ' sec')
