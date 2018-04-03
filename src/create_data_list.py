#!/bin/bash
from glob import glob
import os
import math

def getCleanName(in_name):
    return in_name.split('.')[0].split('_')[0]

# global settings
isToyData = True
fake_label = 0 # we do not care the label's value
its_val_start = 10001 # its val set starts from 10001.png
if isToyData:
    toy_train_data_size = 1000
    toy_val_data_size = 1000
    toy_data_size = toy_train_data_size + toy_val_data_size
else:
    ots_train_portion = 0.9

# setup dirs
raw_data_root = '/media/guanlong/DATA/633_data/'
its_train_haze = raw_data_root + 'ITS/train/ITS_haze/'
its_train_clean = raw_data_root + 'ITS/train/ITS_clear/'
its_val_haze = raw_data_root + 'ITS/val/haze/'
its_val_clean = raw_data_root + 'ITS/val/clear/'
ots_haze = raw_data_root + 'OTS_haze/'
ots_clean = raw_data_root + 'OTS_clean/'
if isToyData:
    data_tag = 'toy_'
else:
    data_tag = ''
data_train = '../%sdata/train/' % (data_tag)
data_val = '../%sdata/val/' % (data_tag)
if not os.path.exists(data_train):
    os.mkdir(data_train)
if not os.path.exists(data_val):
    os.mkdir(data_val)
train_haze_txt = open('../%sdata/train_haze.txt' % (data_tag), 'w')
train_clean_txt = open('../%sdata/train_clean.txt' % (data_tag), 'w')
val_haze_txt = open('../%sdata/val_haze.txt' % (data_tag), 'w')
val_clean_txt = open('../%sdata/val_clean.txt' % (data_tag), 'w')

# get full file list
its_haze_list = (glob(its_train_haze + '*.png') + glob(its_val_haze + '*.png'))
its_haze_list.sort()
its_clean_list = glob(its_train_clean + '*.png') + glob(its_val_clean + '*.png')
for ii in range(len(its_clean_list)):
    its_clean_list[ii] = its_clean_list[ii].split('/')[-1]
its_clean_list = set(its_clean_list)

ots_haze_list = glob(ots_haze + '*.jpg')
ots_haze_list.sort()
ots_clean_list = glob(ots_clean + '*.jpg')
for ii in range(len(ots_clean_list)):
    ots_clean_list[ii] = ots_clean_list[ii].split('/')[-1]
ots_clean_list = set(ots_clean_list)

# build the txt files
if isToyData: # only use OTS
    for ii in range(toy_data_size):
        haze_name = ots_haze_list[ii].split('/')[-1]
        clean_name = getCleanName(haze_name) + '.jpg'
        isCleanExists = (clean_name in ots_clean_list)
        haze_output = '%s%s %d\n' % (ots_haze, haze_name, fake_label)
        clean_output = '%s%s %d\n' % (ots_clean, clean_name, fake_label)
        if isCleanExists:
            if ii < toy_val_data_size:
                train_haze_txt.write(haze_output)
                train_clean_txt.write(clean_output)
            else:
                val_haze_txt.write(haze_output)
                val_clean_txt.write(clean_output)
else: # real data
    for haze_name in its_haze_list: # deal with ITS, png
        haze_name = haze_name.split('/')[-1]
        clean_idx = getCleanName(haze_name)
        clean_idx_num = int(clean_idx)
        clean_name = clean_idx + '.png'
        isCleanExists = (clean_name in its_clean_list)
        isTrainingSample = (clean_idx_num < its_val_start)
        if isTrainingSample: # in training set
            haze_output = '%s%s %d\n' % (its_train_haze, haze_name, fake_label)
            clean_output = '%s%s %d\n' % (its_train_clean, clean_name, fake_label)
        else: # in val set
            haze_output = '%s%s %d\n' % (its_val_haze, haze_name, fake_label)
            clean_output = '%s%s %d\n' % (its_val_clean, clean_name, fake_label)
        if isCleanExists:
            if isTrainingSample:
                train_haze_txt.write(haze_output)
                train_clean_txt.write(clean_output)
            else:
                val_haze_txt.write(haze_output)
                val_clean_txt.write(clean_output)

    # determine the data split for OTS set
    ots_val_start = math.ceil(len(ots_haze_list)*ots_train_portion) + 1
    nSample = 0
    for haze_name in ots_haze_list: # deal with OTS, jpg
        haze_name = haze_name.split('/')[-1]
        nSample += 1
        clean_idx = getCleanName(haze_name)
        clean_name = clean_idx + '.jpg'
        isCleanExists = (clean_name in ots_clean_list)
        isTrainingSample = (nSample < ots_val_start)
        haze_output = '%s%s %d\n' % (ots_haze, haze_name, fake_label)
        clean_output = '%s%s %d\n' % (ots_clean, clean_name, fake_label)
        if isCleanExists:
            if isTrainingSample: # in train set
                train_haze_txt.write(haze_output)
                train_clean_txt.write(clean_output)
            else: # in val set
                val_haze_txt.write(haze_output)
                val_clean_txt.write(clean_output)
train_haze_txt.close()
train_clean_txt.close()
val_haze_txt.close()
val_clean_txt.close()