#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

# import python libs

from pprint import pprint as pp
import base64
import json
import logging
import copy

# import project libs
# -

# defining globals & constants

SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_table.json'

# methods

def read_subject_table():
    file_handler = open(SUBJECTS_TABEL_JSON, 'r', encoding='utf-8')
    raw_content = file_handler.read()
    file_handler.close()
    return json.JSONDecoder().decode(raw_content)[0]

def process_iteration(raw_data):
    corpus = decode_post_data(raw_data)
    documents = iterate_corpus(corpus)
    return documents

def decode_post_data(request_json):
    for raw_datum in request_json:
        encoded_content = raw_datum['data']
        deconded_content = base64.b64decode(encoded_content).decode('utf-8')
        deconded_content = json.JSONDecoder().decode(deconded_content)
        raw_datum['data'] = deconded_content
    return request_json

def iterate_corpus(corpus):
    def flat_corpus(corpus):
        paragraphs = []
        for document in corpus:
            raw_datum_id = document['id']
            for paragraph in document['data']['data']:
                paragraphs.append({
                    'raw_datum_id': raw_datum_id,
                    'paragraph': paragraph
                })
        return paragraphs

    subject_table_blocks = read_subject_table()
    annotation_documents = []
    paragraph_index = 0
    block_index = 0
    paragraphs_of_block = []

    use_questionnaires = 'questions' in corpus[0]['data']['data'][0]
    if use_questionnaires:
        corpus_documents = corpus[1:]
        questionnaire_document_id = corpus[0]['id']
        questions = corpus[0]['data']['data']
        demographic_questionnaire = questions.pop(0)
    else:
        corpus_documents = corpus

    for content in flat_corpus(corpus_documents):
        raw_datum_id = content['raw_datum_id']
        paragraph = content['paragraph']

        paragraphs_of_block.append(paragraph)
        add_annotation_document(annotation_documents, raw_datum_id, paragraph)

        paragraph_index += 1
        if paragraph_index >= len(subject_table_blocks[block_index]):
            current_block_was_annotated = paragraphs_are_annotated(paragraphs_of_block)
            paragraph_index = 0
            block_index += 1
            paragraphs_of_block = []

            if use_questionnaires:
                question = copy.deepcopy(questions[current_block_was_annotated])
                add_questionnaire_document(annotation_documents, questionnaire_document_id, question, block_index)

    if use_questionnaires:
        add_questionnaire_document(annotation_documents, questionnaire_document_id, demographic_questionnaire, block_index + 1)
    return annotation_documents

def add_annotation_document(document_list, raw_id, document_content):
    document_list.append({
        'rank': len(document_list),
        'raw_datum_id': raw_id,
        'payload': {
            'content': [document_content],
            'label_set': [
                {
                    "name": "Person",
                    "label": "PER",
                    "id": 0
                },
                {
                    "name": "Firma / Organisation",
                    "label": "COM",
                    "id": 1
                }
            ]
        },
        'interface_type': 'ner_complete'
    })

def add_questionnaire_document(document_list, raw_id, question_document, block_index):
    question_document['order'] = block_index
    document_list.append({
        'rank': len(document_list),
        'raw_datum_id': raw_id,
        'payload': question_document,
        'interface_type': 'questionnaire',
        'meta': {
            'order': block_index
        }
    })

def paragraphs_are_annotated(paragraphs):
    for paragraph in paragraphs:
        for sentence in paragraph:
            for token in sentence:
                if 'annotation' in token:
                    return 1
    return 0
