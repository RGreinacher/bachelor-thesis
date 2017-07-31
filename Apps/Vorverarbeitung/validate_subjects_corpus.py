#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import argparse
import json
import random
import sys
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp
from collections import deque

# import project libs

sys.path.append('../Auswertung')
import compare_annotations

# defining globals & constants

GOLD_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/Implisense/json gold/'
SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_tabel.json'
SUBJECT_CORPUS_FOLDER = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet'

# methods

def read_subject_table(file_path):
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

    file_handler = open(file_path, 'r', encoding='utf-8')
    raw_content = file_handler.read()
    file_handler.close()
    blocks = json.JSONDecoder().decode(raw_content)
    return flatten_annotations_per_block(blocks)

def read_corpora(path):
    corpora = []
    for folder_name in sorted(listdir(path)):
        subject_folder = join(path, folder_name)
        if isfile(subject_folder): continue
        corpus = []

        for file_name in sorted(listdir(subject_folder)):
            file_path = join(subject_folder, file_name)
            if not (isfile(file_path) and file_name.endswith('.json')): continue
            file_handler = open(file_path, 'r', encoding='utf-8')
            raw_content = file_handler.read()
            file_handler.close()

            deconded_content = json.JSONDecoder().decode(raw_content)
            corpus.append(deconded_content)

        corpora.append(corpus)
    return corpora

def read_corpus_files(path):
    corpus = []
    for file_name in sorted(listdir(path)):
        file_path = join(path, file_name)
        if not (isfile(file_path) and (file_name.endswith('.json') or file_name.endswith('.txt'))): continue
        file_handler = open(file_path, 'r', encoding='utf-8')
        raw_content = file_handler.read()
        file_handler.close()

        deconded_content = json.JSONDecoder().decode(raw_content)
        corpus.append(deconded_content)
    return corpus

def analyze_corpus(corpus, annotation_class_distribution, gold_annotated_corpus):
    total_paragraph_index = -1
    if not validate_questionnaire(corpus.pop(0)):
        print('questionnaire not valid!')
        exit()

    for document_index, document in enumerate(corpus):
        for paragraph_index, paragraph in enumerate(document['data']):
            total_paragraph_index += 1
            for sentence_index, sentence in enumerate(paragraph):
                gold_annotated_sentence = gold_annotated_corpus[document_index]['data'][paragraph_index][sentence_index]

                annotations_of_sentence = compare_annotations.compare_annotations_in_sentences(gold_annotated_sentence, sentence)
                subjects_tabel_extract = annotation_class_distribution[total_paragraph_index][sentence_index]

                if annotations_of_sentence != subjects_tabel_extract or len(gold_annotated_sentence) != len(sentence):
                    print('specification:', subjects_tabel_extract, '- real annotations:', annotations_of_sentence)
                    print('gold sentence')
                    pp(gold_annotated_sentence)
                    print('generated corpus')
                    pp(sentence)
                    print('ANNOTATION MISSMATCH!')
                    exit()
                    return False
    return True

def validate_questionnaire(questionnaire_document):
    return questionnaire_document['id'] == 'questionnaire_document.json'

# entry point as a stand alone script

if __name__ == '__main__':
    print('read all corpora...')
    gold_annotated_corpus = read_corpus_files(GOLD_ANNOTATED_CORPUS_FILES)
    subjects_table = read_subject_table(SUBJECTS_TABEL_JSON)
    all_subjets_corpora = read_corpora(SUBJECT_CORPUS_FOLDER)
    all_corpora_passed = len(all_subjets_corpora) > 0

    for index, corpus in enumerate(all_subjets_corpora):
        if not analyze_corpus(corpus, subjects_table[index], gold_annotated_corpus):
            print('✗ Corpus', index, 'did not pass the analysis!')
            all_corpora_passed = False
            break

    if all_corpora_passed:
        print('✓ all corpora are correct!')
    else:
        print('✗ bad corpora!')
