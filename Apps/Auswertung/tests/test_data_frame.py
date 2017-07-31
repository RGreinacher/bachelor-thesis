#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import json
from pprint import pprint as pp
import sys
sys.path.append('../')

# import project libs

from constants import *
from helper import *

# defining globals & constants

PREANNOTATIONS_START_INDEX = 27
BLOCK_OFFSET = 58

# methods

def check_annotation_corrections(data_frame):
    for subject_id, subject_data in enumerate(data_frame):
        for block_index in range(0, 4):
            (preannotations, corrections) = restructure_data(subject_data, block_index)
            for index, number_of_annotations in enumerate(preannotations):
                if number_of_annotations != sum(corrections[index]):
                    print('ERROR FOUND! subject', subject_id, ' block', block_index)
                    print('sum does not match for class', index)
                    print('expecting', number_of_annotations, 'annotations, got:', corrections[index])
                    print('full distribution and answer table for subject:')
                    pp(preannotations)
                    pp(corrections)
                    exit()
        print('✓ annotation corrections of subject ID', subject_id, 'are valid')

def restructure_data(subject_data, block_index):
    start_index = PREANNOTATIONS_START_INDEX + (BLOCK_OFFSET * block_index)
    preannotations = [
        subject_data[start_index],
        subject_data[start_index + 7],
        subject_data[start_index + 14],
        subject_data[start_index + 21],
        subject_data[start_index + 28],
        subject_data[start_index + 35]
    ]
    corrections = [
        [],
        [],
        [],
        [],
        [],
        []
    ]

    data_offset = (BLOCK_OFFSET * block_index)
    for class_index in range(0, 6):
        for answer_index in range(0, 6):
            answer_count = subject_data[PREANNOTATIONS_START_INDEX + data_offset + 1 + class_index + answer_index]
            corrections[class_index].append(answer_count)
        data_offset += 6

    return (preannotations, corrections)

def check_shape(data_frame):
    header_length = len(data_frame[0])
    for subject_id in range(0, len(data_frame) - 1):
        subject_row = data_frame[subject_id + 1]
        current_length = len(subject_row)
        if current_length != header_length:
            print('ERROR FOUND! row of subject ID', subject_id, 'is', current_length, 'but should be', header_length)
            exit()
        print('✓ length of subject ID', subject_id, 'is valid')

data = read_json_file('../' + JSON_DATA_FRAME_FILE_NAME)
check_shape(data)
check_annotation_corrections(data)
