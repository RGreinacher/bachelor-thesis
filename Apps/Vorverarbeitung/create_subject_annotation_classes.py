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

# import project libs

import create_annotated_corpus

# defining globals & constants

GOLD_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/Implisense/json gold/'
SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_tabel.json'

TARGET_DISTRIBUTION = [
    [
        10, # correct annotation
        16.5141, # manipulated span
        6.606, # manipulated cat
        0, # manipulated cat & span
        3.3021, # unnecessary annotation
        63.5778  # no annotation
    ],
    [
        50, # correct annotation
        9.1745, # manipulated span
        3.67, # manipulated cat
        0, # manipulated cat & span
        1.8345, # unnecessary annotation
        35.321  # no annotation
    ],
    [
        90, # correct annotation
        1.8349, # manipulated span
        0.734, # manipulated cat
        0, # manipulated cat & span
        0.3669, # unnecessary annotation
        7.0642  # no annotation
    ]
]

TOTAL_ANNOTATIONS = 310
MIN_NUMBER_OF_ANNOTATIONS_PER_BLOCK = 75
NUMBER_OF_SUBJECTS = 66

# methods

def read_corpus_files(path):
    corpus = []
    for file_name in sorted(listdir(path)):
        if not (isfile(join(path, file_name)) and file_name.endswith('.json')): continue
        file_handler = open(path + file_name, 'r', encoding='utf-8')
        raw_content = file_handler.read()
        file_handler.close()

        deconded_content = json.JSONDecoder().decode(raw_content)
        corpus.append(deconded_content)
    return corpus

def define_blocks(annotated_corpus):
    annotations_per_paragraph = []

    # create list with annotations per sentence / paragraph
    for document in annotated_corpus:
        for paragraph in document['data']:
            annotations_per_sentences = []
            for sentence in paragraph:
                annotations_per_sentence = 0
                for token in sentence:
                    if 'annotation' in token:
                        annotations_per_sentence += 1
                annotations_per_sentences.append(annotations_per_sentence)
            annotations_per_paragraph.append(annotations_per_sentences)

    # define blocks
    blocks = []
    annotations_per_block = 0
    last_index = 0
    for index, annotations_per_sentence_in_paragraph in enumerate(annotations_per_paragraph):
        annotations_per_block += sum(annotations_per_sentence_in_paragraph)
        if annotations_per_block >= MIN_NUMBER_OF_ANNOTATIONS_PER_BLOCK or index == (len(annotations_per_paragraph) - 1):
            print('add', annotations_per_block, 'annotations to block')
            index_for_partitioning = index + 1
            blocks.append(annotations_per_paragraph[last_index:index_for_partitioning])
            last_index = index_for_partitioning
            annotations_per_block = 0
    return blocks

def create_reference_distributions(blocks):
    def distribution_per_block(annotations, level):
        factor = annotations / 100.0
        absolute_distribution = list(map(lambda x: int(x * factor), TARGET_DISTRIBUTION[level]))
        difference = annotations - sum(absolute_distribution)
        if difference > 0:
            for i in range(0, difference):
                index = random.choice([0, 1, 2, 4, 5]) # 3 is missing, because it is not occuring
                absolute_distribution[index] += 1

        annotation_class_list = []
        for class_id, count in enumerate(absolute_distribution):
            for i in range(0, count):
                annotation_class_list.append(class_id)
        random.shuffle(annotation_class_list)
        return annotation_class_list

    def collate_distribution_to_block_structure(block, distribution):
        block_with_annotation_classes = []
        for document in block:
            annotation_classes_per_document = []
            for number_of_annotations_per_sentence in document:
                annotation_classes_per_sentence = []
                for i in range(0, number_of_annotations_per_sentence):
                    annotation_classes_per_sentence.append(distribution.pop(0))
                annotation_classes_per_document.append(annotation_classes_per_sentence)
            block_with_annotation_classes.append(annotation_classes_per_document)
        return block_with_annotation_classes

    annotation_classes_in_blocks_per_level = []
    for level in range(0, 3):
        annotation_classes_in_blocks = []
        for block in blocks:
            annotations = sum(map(lambda sentence: sum(sentence), block))
            distribution = distribution_per_block(annotations, level)
            collated_block = collate_distribution_to_block_structure(block, distribution)
            annotation_classes_in_blocks.append(collated_block)
        annotation_classes_in_blocks_per_level.append(annotation_classes_in_blocks)
    return annotation_classes_in_blocks_per_level

def create_distribution_per_subject(reference_annotation_classes, subject_id):
    def clear_block(block):
        clean_block = []
        for document in block:
            cleaned_document = []
            for sentence in document:
                cleaned_sentence = []
                for annotation in sentence:
                    cleaned_sentence.append(5)
                cleaned_document.append(cleaned_sentence)
            clean_block.append(cleaned_document)
        return clean_block

    def collate_distribution_to_block_structure(block, distribution):
        block_with_annotation_classes = []
        for document in block:
            annotation_classes_per_document = []
            for sentence in document:
                annotation_classes_per_sentence = []
                for annotation_class in sentence:
                    annotation_classes_per_sentence.append(distribution.pop(0))
                annotation_classes_per_document.append(annotation_classes_per_sentence)
            block_with_annotation_classes.append(annotation_classes_per_document)
        return block_with_annotation_classes

    def shift_annotation_classes(block, offset):
        distribution = flat_block_structure(block)
        items = deque(distribution)
        items.rotate(offset)
        rotated_distribution = list(items)
        return collate_distribution_to_block_structure(block, rotated_distribution)

    subject_blocks = []
    for i in range(subject_id, (subject_id + 4)):
        reference_block = reference_annotation_classes[i - subject_id]
        if i % 2 == 0:
            block = clear_block(reference_block)
        else:
            block = shift_annotation_classes(reference_block, subject_id - 1)
        subject_blocks.append(block)

    return subject_blocks

def add_no_annotations_to_unnecessary_annotations(blocks, gold_annotated_corpus):
    def flatten_blocks(blocks_per_subject):
        # return a list of paragraphs for each subject
        paragraphs = []
        for block in blocks_per_subject:
            for paragraph in block:
                paragraphs.append(paragraph)
        return paragraphs

    def insert_index_addition(token_index, sentence):
        current_annotation_length = sentence[token_index]['annotation']['length']
        space_to_the_left = token_index - create_annotated_corpus.earliest_chunk_start_index(sentence, token_index)
        space_to_the_right = create_annotated_corpus.maximum_chunk_length(sentence, token_index) - current_annotation_length
        # print('sentence')
        # pp(sentence)
        # print('index', token_index, 'left', space_to_the_left, 'right', space_to_the_right)
        if space_to_the_left > space_to_the_right: return 1
        return 0

    def collate_paragraphs_to_blocks_structure(blocks, paragraphs):
        total_paragraph_index = -1
        for block in blocks:
            for i in range(0, len(block)):
                total_paragraph_index += 1
                block[i] = paragraphs[total_paragraph_index]
        return blocks

    total_paragraph_index = -1
    annotations_per_paragraph = flatten_blocks(blocks)
    for document_index, document in enumerate(gold_annotated_corpus):
        for paragraph_index, paragraph in enumerate(document['data']):
            total_paragraph_index += 1
            for sentence_index, sentence in enumerate(paragraph):
                annotations_per_sentence = annotations_per_paragraph[total_paragraph_index][sentence_index]
                annotation_index = -1
                for token_index, token in enumerate(sentence):
                    if 'annotation' in token:
                        annotation_index += 1
                        if annotations_per_sentence[annotation_index] == 4:
                            # print('annotations list before', annotations_per_sentence)
                            insert_index = annotation_index + insert_index_addition(token_index, sentence)
                            # print('insert_index', insert_index)
                            annotations_per_sentence.insert(insert_index, 5)
                            # print('annotations list after', annotations_per_sentence)
                            annotation_index += 1

    return collate_paragraphs_to_blocks_structure(blocks, annotations_per_paragraph)

# helpers

def validate_target_distribution():
    for index, distribution in enumerate(TARGET_DISTRIBUTION):
        if sum(distribution) != 100:
            print('TARGET_DISTRIBUTION is not valid!', index)
            exit()

def flat_block_structure(block):
    flatted_list = []
    for document in block:
        for sentence in document:
            for annotation_class in sentence:
                flatted_list.append(annotation_class)
    return flatted_list

def save_document_to_file(document):
    json_encoded_document = json.dumps(document)
    file_handler = open(SUBJECTS_TABEL_JSON, 'w')
    file_handler.write(json_encoded_document)
    file_handler.close()

def find_four(blocks, prefix = False):
    return find_occurences(4, blocks, prefix)

def find_occurences(number, blocks, prefix = False):
    relevant_sentences = []
    for block_index, block in enumerate(blocks):
        for paragraph_index, paragraph in enumerate(block):
            for sentence_index, sentence in enumerate(paragraph):
                if number in sentence:
                    relevant_sentences.append(sentence)
                    if prefix: print(prefix, sentence)
    return relevant_sentences

# entry point as a stand alone script

if __name__ == '__main__':
    validate_target_distribution()
    gold_annotated_corpus = read_corpus_files(GOLD_ANNOTATED_CORPUS_FILES)
    blocks = define_blocks(gold_annotated_corpus)
    reference_annotation_classes_in_blocks = create_reference_distributions(blocks)

    for level, reference_annotation_classes_per_level in enumerate(reference_annotation_classes_in_blocks):
        find_occurences(3, reference_annotation_classes_per_level, 'found forbidden number in level' + str(level))

    subject_table = []
    for subject_id in range(0, NUMBER_OF_SUBJECTS):
        level = subject_id % 3
        reference_annotation_classes = reference_annotation_classes_in_blocks[level]
        subject_annotation_classes = create_distribution_per_subject(reference_annotation_classes, subject_id)
        with_no_annotations = add_no_annotations_to_unnecessary_annotations(subject_annotation_classes, gold_annotated_corpus)
        subject_table.append(with_no_annotations)

    save_document_to_file(subject_table)

    # blocks = [[[[4, 1]]]]
    # gold = [
    #     {
    #         'data': [
    #             [
    #                 [
    #                     {'annotation': {'label': 'COM', 'length': 2}, 'term': 'eBay'},
    #                     {'term': 'Kleinanzeigen'},
    #                     {'term': 'gehört'},
    #                     {'term': 'zur'},
    #                     {'term': 'internationalen'},
    #                     {'annotation': {'label': 'COM', 'length': 3}, 'term': 'eBay'},
    #                     {'term': 'Classifieds'},
    #                     {'term': 'Group'},
    #                     {'term': '.'}
    #                 ]
    #             ]
    #         ]
    #     }
    # ]
    # add_no_annotations_to_unnecessary_annotations(blocks, gold)
