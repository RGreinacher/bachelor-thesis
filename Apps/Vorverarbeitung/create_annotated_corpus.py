#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import argparse
import json
import random
import math
import os
import copy
import sys
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp

# import project libs

sys.path.append('../Auswertung')
import compare_annotations

# defining globals & constants

SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_tabel.json'
QUESTIONNAIRE_DOCUMENT_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/questionnaire_document.json'

# PLAIN_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/test_text/raw/'
# GOLD_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/test_text/gold-annotiert/'
PLAIN_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/Implisense/json/'
GOLD_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/Implisense/json gold/'

SUBJECT_CORPUS_FOLDER = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet'
CORPUS_SUFFIX = 'preannotated_subject_corpus_document'

# methods

def read_subject_table():
    def flatten_annotations_per_block(blocks_per_subject):
        # return a list of paragraphs for each subject
        subjects = []
        for blocks_for_subject in blocks_per_subject:
            paragraphs = []
            for block in blocks_for_subject:
                for paragraph in block:
                    paragraphs.append(paragraph)
            subjects.append(paragraphs)
        return subjects

    file_handler = open(SUBJECTS_TABEL_JSON, 'r', encoding='utf-8')
    raw_content = file_handler.read()
    file_handler.close()
    blocks = json.JSONDecoder().decode(raw_content)
    return flatten_annotations_per_block(blocks)

def read_questionnaire_document():
    file_handler = open(QUESTIONNAIRE_DOCUMENT_JSON, 'r', encoding='utf-8')
    raw_content = file_handler.read()
    file_handler.close()
    return json.JSONDecoder().decode(raw_content)

def read_corpus_files(path):
    def clean_unrecognized_labels(corpus):
        for document in corpus:
            for paragraph in document['data']:
                for sentence in paragraph:
                    for token in sentence:
                        if 'annotation' in token and token['annotation']['label'] not in LABELS:
                            del token['annotation']

    corpus = []
    for file_name in sorted(listdir(path)):
        if not (isfile(join(path, file_name)) and file_name.endswith('.json')): continue
        file_handler = open(path + file_name, 'r', encoding='utf-8')
        raw_content = file_handler.read()
        file_handler.close()

        deconded_content = json.JSONDecoder().decode(raw_content)
        corpus.append(deconded_content)
    # clean_unrecognized_labels(corpus)
    return corpus

def create_annotated_corpus(subject_corpus, gold_annotated_corpus, subject_annotation_classes):
    total_paragraph_index = -1
    for document_index, document in enumerate(gold_annotated_corpus):
        for paragraph_index, paragraph in enumerate(document['data']):
            total_paragraph_index += 1
            for sentence_index, sentence in enumerate(paragraph):
                annotation_classes_of_sentence = subject_annotation_classes[total_paragraph_index][sentence_index]
                if len(annotation_classes_of_sentence) == 0: continue
                annotation_number = 0

                for token_index, token in enumerate(sentence):
                    next_annotation_class = annotation_classes_of_sentence[annotation_number]
                    subject_sentence = subject_corpus[document_index]['data'][paragraph_index][sentence_index]

                    # look ahead annotation for class 4 annotations
                    if next_annotation_class == 4:
                        (new_subject_sentence, _) = unnecessary_annotation(subject_sentence, token_index, sentence)

                    # skip if token not annotated
                    elif not ('annotation' in token):
                        continue

                    # if current token is annotated, apply the specificated annotation class
                    else:
                        manipulator = ANNOTATION_CLASSES[next_annotation_class]
                        (new_subject_sentence, _) = manipulator(subject_sentence, token_index, sentence)

                    subject_corpus[document_index]['data'][paragraph_index][sentence_index] = new_subject_sentence
                    annotation_number += 1
                    if annotation_number >= len(annotation_classes_of_sentence): break

    return subject_corpus

# annotation manipulation

def manipulate_span(sentence, token_index, reference_sentence):
    length = reference_sentence[token_index]['annotation']['length']
    debug_length = reference_sentence[token_index]['annotation']['length']
    new_start_index = token_index
    index_offset = 0
    possible_offsets_reference = possible_start_index_offsets(reference_sentence, token_index)
    possible_offsets_sentence = possible_start_index_offsets(sentence, token_index)
    possible_offsets = list(set(possible_offsets_reference).intersection(possible_offsets_sentence))
    if not (len(possible_offsets) == 0):
        index_offset = random.choice(possible_offsets)
        new_start_index += index_offset

    sentence[new_start_index]['annotation'] = copy.deepcopy(reference_sentence[token_index]['annotation'])

    # chunk has a new beginning but stil same length - let's change that!
    length_with_offset = (length - index_offset)
    if index_offset < 0:
        min_length = length_with_offset - (length - 1)
        if min_length < 1: min_length = 1
        max_length = maximum_chunk_length(reference_sentence, token_index + 1) - index_offset
    else:
        min_length = length_with_offset
        max_length = maximum_chunk_length(reference_sentence, new_start_index)

    if min_length == length and length + 1 <= max_length:
        min_length += 1

    length = random.choice(range(min_length, max_length + 1))
    if length > 4:
        length = 4

    sentence[new_start_index]['annotation']['length'] = length
    return (sentence, new_start_index)

def manipulate_cat(sentence, token_index, reference_sentence):
    annotated_token = reference_sentence[token_index]
    new_label = change_label(annotated_token['annotation']['label'])
    annotated_token['annotation']['label'] = new_label
    sentence[token_index] = annotated_token
    return (sentence, token_index)

def manipulate_cat_span(sentence, token_index, reference_sentence):
    (sentence, token_index) = manipulate_span(sentence, token_index, reference_sentence)
    return manipulate_cat(sentence, token_index, sentence)

def correct_annotation(sentence, token_index, reference_sentence):
    sentence[token_index] = copy.deepcopy(reference_sentence[token_index])
    return (sentence, token_index)

def no_annotation(sentence, token_index, reference_sentence):
    return (sentence, token_index)

def unnecessary_annotation(sentence, token_index, reference_sentence):
    if token_index == 0:
        begin = 0
    else:
        if not 'annotation' in reference_sentence[token_index - 1]: # DEBUG!
            print('DEBBUG token_index', token_index, 'sentence:')
            pp(reference_sentence)
        current_annotation_length = reference_sentence[token_index - 1]['annotation']['length']
        begin = token_index - 1 + current_annotation_length

    end = begin + maximum_chunk_length(reference_sentence, begin)
    annotation_index = random.choice(range(begin, end))
    max_length = maximum_chunk_length(reference_sentence, annotation_index)

    annotation_label = random.choice(LABELS)
    annotation_length = 1
    if max_length >= 3:
        annotation_length = random.choice([1, 2, 3])
    elif max_length == 2:
        annotation_length = random.choice([1, 2])

    sentence[annotation_index]['annotation'] = {
        'label': annotation_label,
        'length': annotation_length
    }
    return (sentence, annotation_index)

# helpers

def possible_start_index_offsets(sentence, token_index):
    possible_offsets = []
    length = 3 # >= 2
    if 'annotation' in sentence[token_index]:
        length = sentence[token_index]['annotation']['length']

    max_left_shift = token_index - earliest_chunk_start_index(sentence, token_index)
    max_right_shift = maximum_chunk_length(sentence, token_index) - 1

    if max_left_shift >= 2 and length > 2:
        possible_offsets = [-2, -1]
    elif max_left_shift >= 1:
        possible_offsets = [-1]

    if max_right_shift >= 2 and length > 2:
        possible_offsets += [1, 2]
    elif max_right_shift >= 1 and length >= 2:
        possible_offsets += [1]

    return possible_offsets

def earliest_chunk_start_index(sentence, start_index):
    sentence_length = len(sentence)
    if start_index == 0:
        return 0

    earliest_index = start_index
    for iteration_index in range((start_index - 1), -1, -1):
        earliest_index -= 1
        if 'annotation' in sentence[iteration_index]:
            length = sentence[iteration_index]['annotation']['length']
            earliest_index += length
            break

    return earliest_index

def maximum_chunk_length(sentence, start_index):
    sentence_length = len(sentence)
    if start_index == sentence_length - 1:
        return 1

    max_chunk_length = 1
    for iteration_index in range((start_index + 1), sentence_length):
        if 'annotation' in sentence[iteration_index]:
            break
        max_chunk_length = max_chunk_length + 1

    return max_chunk_length

def change_label(label):
    index = LABELS.index(label)
    if index > 0: return LABELS[0]
    return LABELS[1]

def save_document_to_file(corpus, subject_id):
    for document_index, document in enumerate(corpus):
        prefix = chr(97 + document_index)
        folder_postfix = subject_id
        if subject_id < 10:
            folder_postfix = "%s%s" % (0, subject_id)

        subject_folder = "%s/VP%s" % (SUBJECT_CORPUS_FOLDER, folder_postfix)
        file_name = "%s_%s.json" % (prefix, CORPUS_SUFFIX)
        file_path = "%s/%s" % (subject_folder, file_name)

        if not os.path.exists(subject_folder):
            os.makedirs(subject_folder)

        json_encoded_document = json.dumps(document)
        file_handler = open(file_path, 'w')
        file_handler.write(json_encoded_document)
        file_handler.close()

# experiment definitions

ANNOTATION_CLASSES = {
    0 : correct_annotation,
    1 : manipulate_span,
    2 : manipulate_cat,
    3 : manipulate_cat_span,
    4 : unnecessary_annotation,
    5 : no_annotation
}
LABELS = [
    'PER', 'COM'
]

# entry point as a stand alone script

if __name__ == '__main__':
    subjects_table = read_subject_table()
    questionnaire_document = read_questionnaire_document()

    for subject_id, subject_annotation_classes in enumerate(subjects_table):
    # for i in range(0, 20):
    #     subject_id = i
    #     subject_annotation_classes = subjects_table[i]

        print('create corpus for subject #', subject_id)
        gold_annotated_corpus = read_corpus_files(GOLD_ANNOTATED_CORPUS_FILES)
        plain_corpus = read_corpus_files(PLAIN_CORPUS_FILES)

        subject_corpus = create_annotated_corpus(plain_corpus, gold_annotated_corpus, subject_annotation_classes)
        subject_corpus.insert(0, questionnaire_document)
        save_document_to_file(subject_corpus, subject_id)
