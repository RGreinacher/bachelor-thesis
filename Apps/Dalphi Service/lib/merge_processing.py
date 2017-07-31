#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

# import python libs

from pprint import pprint as pp
import base64
import json
import os
from datetime import datetime

# import project libs
# -

# defining globals & constants

SAVE_DOCUMENTS_TO_FILE = True
SAVE_CORPUS_TO_FILE = True
SAVE_ANNOTATION_DURATIONS = True
DOCUMENT_FOLDER = 'processed_annotation_documents'
CORPUS_FOLDER = 'processed_corpus_documents'

# methods

def decode_post_data(request_json):
    post_json_data = json.dumps(request_json)
    dict_content = json.JSONDecoder().decode(post_json_data)
    annotation_documents = dict_content['annotation_documents']
    raw_datum_id = dict_content['raw_datum']['id']
    return (raw_datum_id, annotation_documents)

def create_new_raw_datum(raw_datum_id, annotation_documents):
    content = []
    annotation_durations = []
    document_type = 'annotation_document'

    for index, document in enumerate(annotation_documents):
        if SAVE_DOCUMENTS_TO_FILE:
            save_document_to_file(document, 'annotation_document', index)
        if document['raw_datum_id'] == raw_datum_id:
            json_encoded_payload = document['payload']

            # questionnaire document
            if document['interface_type'] == 'questionnaire':
                document_type = 'questionnaire'
                order = -1
                if document['meta'] and 'order' in document['meta']:
                    order = document['meta']['order']

                content.append({
                    "order": order,
                    "answers": json_encoded_payload['content'],
                    "duration": calculate_annotation_time(document)
                })

            # annotation document
            else:
                # the `content` of an annotation document holds only one paragraph;
                paragraph = json_encoded_payload['content'][0]
                content.append(paragraph)

                if SAVE_ANNOTATION_DURATIONS:
                    duration = calculate_annotation_time(document)
                    annotation_durations.append(duration)

    raw_datum = {
        'data': content,
        'id': raw_datum_id
    }
    if SAVE_ANNOTATION_DURATIONS and document_type == 'annotation_document':
        raw_datum['annotation_duration_per_paragraph'] = annotation_durations
    if SAVE_CORPUS_TO_FILE:
        save_document_to_file(raw_datum, 'corpus_document')

    byte_encoded_content = json.dumps(raw_datum).encode('utf-8')
    b64_encoded_content = base64.b64encode(byte_encoded_content)
    string_content = str(b64_encoded_content, encoding='utf-8')

    return {
        'data': string_content,
        'id': raw_datum_id
    }

def calculate_annotation_time(document):
    time_delta = -1
    time_format = '%Y-%m-%d %H:%M:%S %Z'

    if document['requested_at'] and document['updated_at']:
        start_annotation_datetime = datetime.strptime(document['requested_at'], time_format)
        end_annotation_datetime = datetime.strptime(document['updated_at'], time_format)
        time_delta = (end_annotation_datetime - start_annotation_datetime).seconds

    return time_delta

def save_document_to_file(document, content_type, id=False):
    json_encoded_document = json.dumps(document)
    if content_type == 'annotation_document':
        file_name = generate_document_filename_for(document, id)
    else:
        file_name = generate_corpus_filename_for(document)

    file_handler = open(file_name, 'w')
    file_handler.write(json_encoded_document)
    file_handler.close()

def generate_document_filename_for(document, id):
    prefix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    raw_datum_id = document['raw_datum_id']
    rank = document['rank']

    if DOCUMENT_FOLDER:
        if not os.path.exists(DOCUMENT_FOLDER):
            os.makedirs(DOCUMENT_FOLDER)
        return "%s/%s_%s_%s_%s.json" % (DOCUMENT_FOLDER, id, raw_datum_id, rank, prefix)
    else:
        return "%s_%s_%s.json" % (prefix, raw_datum_id, rank)

def generate_corpus_filename_for(corpus):
    prefix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    raw_datum_id = corpus['id']

    if CORPUS_FOLDER:
        if not os.path.exists(CORPUS_FOLDER):
            os.makedirs(CORPUS_FOLDER)
        return "%s/raw-datum-%s_%s.json" % (CORPUS_FOLDER, raw_datum_id, prefix)
    else:
        return "%s_%s_%s.json" % (prefix, raw_datum_id, rank)
