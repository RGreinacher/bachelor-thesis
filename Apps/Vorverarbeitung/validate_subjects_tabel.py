#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import argparse
import json
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp
from collections import deque
import sys
sys.path.append('../Auswertung')

# import project libs

from create_subject_annotation_classes import TARGET_DISTRIBUTION
from create_subject_annotation_classes import find_four
from helper import *

# defining globals & constants

SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_table.json'
DISTRIBUTION_TOLERANCE = 2.5

# methods

def read_subject_table(file_path):
    file_handler = open(file_path, 'r', encoding='utf-8')
    raw_content = file_handler.read()
    file_handler.close()
    blocks = json.JSONDecoder().decode(raw_content)
    return blocks

def general_meta_info(subjects_table):
    for block_index, block in enumerate(subjects_table[0]):
        print(len(block), 'paragraphs in block', block_index)

    empty_blocks = empty_subjects_table(subjects_table)
    for block_index, block in enumerate(empty_blocks):
        distribution = distribution_per_block(block)
        print(distribution[5], 'target annotations in block', block_index)

def analyze_blocks(subject_blocks, subject_id):
    level = subject_id % 3
    correct_classes = True

    for block_index, block in enumerate(subject_blocks):
        distribution = distribution_per_block(block)
        if (block_index + subject_id) % 2 == 0:
            if sum(distribution[:5]) != 0:
                correct_classes = False
                print('wrong order')
                break
        else:
            if not validate_distribution(distribution, level):
                correct_classes = False
                print('bad distribution')
                break
            if not validate_fives_for_every_four(block):
                correct_classes = False
                print('bad unnecessary annotations')
                break

    return correct_classes

def distribution_per_block(block):
    annotation_class_distribution = [0, 0, 0, 0, 0, 0]
    for paragraph in block:
        for sentence in paragraph:
            for annotation_class in sentence:
                annotation_class_distribution[annotation_class] += 1
    return annotation_class_distribution

def validate_distribution(distribution, level):
    correct_distribution = True
    total_annotations = sum(distribution)

    for annotation_class, annotation_occurence in enumerate(distribution):
        percentage = (annotation_occurence / total_annotations) * 100.0
        if annotation_class == 3 and annotation_occurence > 0:
            print('✗ class', annotation_class, ' is present, but should not! Level', level, '(', annotation_occurence, 'occurence(s),', round(percentage, 2), '%)')
            correct_distribution = False

        lower_bound = TARGET_DISTRIBUTION[level][annotation_class] - DISTRIBUTION_TOLERANCE
        upper_bound = TARGET_DISTRIBUTION[level][annotation_class] + DISTRIBUTION_TOLERANCE

        if not (lower_bound <= percentage <= upper_bound):
            print('✗ class', annotation_class, ', level', level, '(', round(percentage, 2), ')')
            correct_distribution = False

    return correct_distribution

def validate_fives_for_every_four(block):
    for sentence in find_four([block]):
        start_index = 0
        while 4 in sentence[start_index:] and start_index < len(sentence):
            index = sentence.index(4, start_index)
            if index > 0 and index < len(sentence) - 1:
                if sentence[index - 1] < 5 and sentence[index + 1] < 5:
                    print('sentence', index)
                    pp(sentence)
                    return False
            elif index > 0:
                if sentence[index - 1] < 5:
                    print('sentence', index)
                    pp(sentence)
                    return False
            elif index < len(sentence) - 1:
                if sentence[index + 1] < 5:
                    print('sentence', index)
                    pp(sentence)
                    return False
            else:
                print('uncought case!', sentence)
            start_index = index + 1
    return True

# entry point as a stand alone script

if __name__ == '__main__':
    blocks = read_subject_table(SUBJECTS_TABEL_JSON)
    general_meta_info(blocks)

    all_blocks_passed = True
    for index, distribution in enumerate(blocks):
        if not analyze_blocks(blocks[index], index):
            print('✗ Block', index, 'did not pass the analysis!')
            all_blocks_passed = False
            break

    if all_blocks_passed:
        print('✓ subjects table is correct!')
    else:
        print('✗ bad subjects table!')
