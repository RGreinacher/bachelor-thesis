#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import argparse
import json
import collections
import copy
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp
from operator import itemgetter

# import project libs

from constants import *
from helper import *

# methods

def quantitative_answer_class_correction_analysis_per_block(subject_classes_per_block, table_classes_per_block, corrections=False):
    if not corrections:
        corrections = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            0
        ]

    for paragraph_index, paragraph in enumerate(table_classes_per_block):
        for sentence_index, preannotation_sentence in enumerate(paragraph):
            subject_annotation_sentence = subject_classes_per_block[paragraph_index][sentence_index]
            (preannotation_sentence, subject_annotation_sentence) = normailize_sentence_length(
                preannotation_sentence,
                subject_annotation_sentence
            )

            for annotation_index, preannotation in enumerate(preannotation_sentence):
                subject_annotation = subject_annotation_sentence[annotation_index]

                if preannotation == 9:
                    corrections[6] += 1
                elif subject_annotation == 9:
                    corrections[4][0] += 1
                else:
                    corrections[preannotation][subject_annotation] += 1

    return corrections

def quantitative_answer_class_correction_analysis(annotation_classes, subjects_table):
    answer_class_corrections_per_level = [False, False, False]

    for subject_id in range(0, len(annotation_classes)):
        level = subject_id % 3
        for block_index, block in enumerate(annotation_classes[subject_id]):
            subject_table_block = subjects_table[subject_id][block_index]
            block_was_annotated = subject_table_block_is_annotated(subject_table_block)

            if block_was_annotated:
                answer_class_corrections_per_level[level] = quantitative_answer_class_correction_analysis_per_block(block, subject_table_block, answer_class_corrections_per_level[level])

    for level, answer_class_corrections in enumerate(answer_class_corrections_per_level):
        print()
        print("Given a %s%% correct annotation system:" % (ASSISTANCE_SYSTEM_LEVELS[level]))
        for answer_class_index in range(0, 6):
            number_of_annotations = sum(answer_class_corrections[answer_class_index])
            if number_of_annotations > 0:
                print("\tPredefined %s annotations (%s) were changed to:" % (ANNOTATION_ANSWER_CLASSES[answer_class_index], number_of_annotations))
                correction_list = []

                for correction_index, correction in enumerate(answer_class_corrections[answer_class_index]):
                    if correction > 0:
                        percentage = round(((correction * 100.0) / number_of_annotations), 2)
                        if correction_index == answer_class_index:
                            correction_list.append({
                                'frequency': int(correction),
                                'description': "\t\t%s%% NOT CHANGED (%s)" % (percentage, correction)
                            })
                        else:
                            correction_list.append({
                                'frequency': int(correction),
                                'description': "\t\t%s%% %s (%s)" % (percentage, ANNOTATION_ANSWER_CLASSES[correction_index], correction)
                            })

                correction_list = sorted(correction_list, key=itemgetter('frequency'), reverse=True)
                for element in correction_list: print(element['description'])

def normailize_sentence_length(preannotation_sentence, subject_annotation_sentence):
    index = 0
    while True:
        pre_length = len(preannotation_sentence)
        sub_length = len(subject_annotation_sentence)
        if index >= pre_length and index >= sub_length:
            return (preannotation_sentence, subject_annotation_sentence)

        if index >= pre_length and subject_annotation_sentence[index] == 4:
            preannotation_sentence.insert(index, 9)
        elif index >= sub_length and preannotation_sentence[index] == 4:
            subject_annotation_sentence.insert(index, 9)
        elif preannotation_sentence[index] == 4 and subject_annotation_sentence[index] != 4:
            subject_annotation_sentence.insert(index, 9)
        elif preannotation_sentence[index] != 4 and subject_annotation_sentence[index] == 4:
            preannotation_sentence.insert(index, 9)

        index += 1



# entry point as a stand alone script

if __name__ == '__main__':
    # read data
    annotation_classes = read_json_file(JSON_ANNOTATION_CLASSES_FILE_NAME)
    subjects_table = read_subject_table()

    quantitative_answer_class_correction_analysis(annotation_classes, subjects_table)
