#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import csv
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

# methods

def read_subject_table():
    return read_json_file(SUBJECTS_TABEL_JSON)

def read_json_file(file_name):
    file_handler = open(file_name, 'r', encoding='utf-8')
    raw_content = file_handler.read()
    file_handler.close()
    return json.JSONDecoder().decode(raw_content)

def read_corpus_files(path, subject_id = -1):
    corpus = []
    if subject_id >= 0:
        path = "%sVP%s/" % (path, str(subject_id).zfill(2))

    for file_name in sorted(listdir(path)):
        file_path = join(path, file_name)
        if not (isfile(file_path) and (file_name.endswith('.json') or file_name.endswith('.txt'))): continue
        if 'VP vorbereitet' in path and file_name.startswith('a_'): continue # ignore raw questionnaire documents

        file_handler = open(path + file_name, 'r', encoding='utf-8')
        raw_content = file_handler.read()
        file_handler.close()

        deconded_content = json.JSONDecoder().decode(raw_content)
        corpus.append(deconded_content)
    return corpus

def reward_for_subject(subject_id):
    for reward_index, subject_list in enumerate(REWARDS):
        if subject_id in subject_list:
            return reward_index
    raise NoRewardForSubjectError

def corpus_runner(annotated_corpus):
    paragraphs = 0 # total number of paragraphs
    sentences = 0 # total number of sentences
    tokens = 0 # total tokens
    annotations = 0 # chunks
    words = 0 # words in chunks

    for document in annotated_corpus:
        for paragraph in document['data']:
            paragraphs += 1
            for sentence in paragraph:
                sentences += 1
                tokens += len(sentence)
                for token in sentence:
                    if 'annotation' in token:
                        annotations += 1
                        words += token['annotation']['length']

    return (paragraphs, sentences, tokens, annotations, words)

def annotation_durations(subjects_table, annotated_corpus):
    durations_per_block = [[]]
    block_index = 0
    paragraph_index_per_block = -1

    for document in annotated_corpus:
        durations = document['annotation_duration_per_paragraph']

        for paragraph_index in range(0, len(document['data'])):
            paragraph_index_per_block += 1
            if paragraph_index_per_block == len(subjects_table[block_index]):
                durations_per_block.append([])
                block_index += 1
                paragraph_index_per_block = 0

            durations_per_block[block_index].append(durations[paragraph_index])

    return durations_per_block

def distribution_per_block(block):
    total_class_distribution = [0, 0, 0, 0, 0, 0]
    for paragraph in block:
        for sentence in paragraph:
            for annotation_class in sentence:
                total_class_distribution[annotation_class] += 1
    return total_class_distribution

def paragraph_is_annotated(paragraph):
    for sentence in paragraph:
        for token in sentence:
            if 'annotation' in token:
                return True
    return False

def empty_subjects_table(subjects_table):
    first_subject = subjects_table[0]
    second_subject = subjects_table[1]
    empty_blocks = []

    if subject_table_block_is_annotated(first_subject[0]):
        empty_blocks.append(second_subject[0])
        empty_blocks.append(first_subject[1])
        empty_blocks.append(second_subject[2])
        empty_blocks.append(first_subject[3])
    else:
        empty_blocks.append(first_subject[0])
        empty_blocks.append(second_subject[1])
        empty_blocks.append(first_subject[2])
        empty_blocks.append(second_subject[3])

    return empty_blocks

def subject_table_block_is_annotated(block):
    for paragraph in block:
        for sentence in paragraph:
            if sum(sentence) != len(sentence) * 5:
                return True
    return False

def annotations_per_subject_table_block(block):
    annotations = 0
    for paragraph in block:
        for sentence in paragraph:
            annotations += len(sentence)
    return annotations

def next_annotation_index(start, sentence):
    current_index = start
    for token in sentence[start:]:
        if 'annotation' in token:
            return current_index
        current_index += 1
    return -1

def seconds_to_min(seconds):
    minutes = int(seconds / 60)
    seconds = (seconds % 60)
    if seconds < 10:
        seconds = "0" + str(seconds)
    return "%s:%s" % (minutes, seconds)

def save_json(data, file_name):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def save_csv(data_frame_list):
    myfile = open(CSV_DATA_FILE_NAME, 'w')
    csv_writer = csv.writer(myfile, delimiter=';')
    csv_writer.writerow(DATA_FRAME_HEADER)
    csv_writer.writerows(data_frame_list)
    myfile.close()
