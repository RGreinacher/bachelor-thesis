#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import argparse
import json
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp
from operator import itemgetter

# import project libs
# -

# defining globals & constants

SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_tabel.json'

# Implisense corpus
SUBJECT_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP annotiert/'

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

def read_questionnaire_files():
    questionnaires = []
    for folder_name in sorted(listdir(SUBJECT_ANNOTATED_CORPUS_FILES)):
        subject_folder = join(SUBJECT_ANNOTATED_CORPUS_FILES, folder_name)
        if isfile(subject_folder): continue

        for file_name in sorted(listdir(subject_folder)):
            file_path = join(subject_folder, file_name)
            if not (isfile(file_path) and file_name.endswith('.json') and file_name.startswith('a_')): continue
            file_handler = open(file_path, 'r', encoding='utf-8')
            raw_content = file_handler.read()
            file_handler.close()

            deconded_content = json.JSONDecoder().decode(raw_content)
            deconded_content['data'] = sorted(deconded_content['data'], key=itemgetter('order'))
            questionnaires.append(deconded_content)

    return questionnaires

# helpers
# -

# entry point as a stand alone script

if __name__ == '__main__':
    questionnaires = read_questionnaire_files()

    print('questionnaires')
    pp(questionnaires)
