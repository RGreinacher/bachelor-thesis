#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

# import python libs

import nltk
import pickle
import json
from nltk import Tree
from pprint import pprint as pp
from nltk.chunk.api import ChunkParserI
from os import listdir
from os.path import isfile, join

# import project libs

# import nltk_tree_converter
import maxent_chunker

# defining globals & constants

POS_TAGGER_PATH = 'nltk_german_pos_classifier_data.pickle'
CHUNKER_PICKLE_NAME = 'self_trained_ne_chunker_multiclass.pickle'
TEXT_SET = 'NER-de-train'

global german_pos_tagger, self_trained_chunker
german_pos_tagger = False
self_trained_chunker = False

# methods

def ner_pipeline(raw_sentence):
    print('NER pipeline: tokenizing / tagging / chunking / converting ...')

    # create a lists of strings
    tokenized_sentence = word_tokenization(raw_sentence)

    # create a list of nltk trees containing named entity chunks
    chunk_tree = named_entity_token_chunking(tokenized_sentence)

    # convert NLTKs tree format to Hannes' JSON
    hannes_json = tree_to_sentence(chunk_tree)

    return hannes_json

def word_tokenization(sentence):
    return nltk.word_tokenize(sentence)

def part_of_speech_tagging(sentence):
    global german_pos_tagger

    if not german_pos_tagger:
        with open(POS_TAGGER_PATH, 'rb') as f:
            german_pos_tagger = pickle.load(f)

    return german_pos_tagger.tag(sentence)

def named_entity_token_chunking(tokenized_sentence):
    global self_trained_chunker

    if not self_trained_chunker:
        with open(CHUNKER_PICKLE_NAME, 'rb') as f:
            self_trained_chunker = pickle.load(f)

    return self_trained_chunker.parse(tokenized_sentence)

def tree_to_sentence(tree):
    sentence = []

    def add_token_from(node):
        token = {
            'term': node[0]
        }
        sentence.append(token)

    def add_tokens_from(tree):
        length = len(tree)
        token = {
            'term': tree[0][0],
            'annotation': {
                'label': annotation_label(tree),
                'length': length
            }
        }

        sentence.append(token)
        if length > 1:
            for node_index in range(1, length):
                add_token_from(tree[node_index])

    def annotation_label(node):
        return node.label()

    for node in tree:
        if type(node) is Tree:
            add_tokens_from(node)
        else:
            add_token_from(node)

    return sentence

# helper

def read_corpus_files(path):
    corpus = []

    for file_name in sorted(listdir(path)):
        file_path = join(path, file_name)
        if not (isfile(file_path) and (file_name.endswith('.json') or file_name.endswith('.txt'))): continue

        file_handler = open(path + file_name, 'r', encoding='utf-8')
        raw_content = file_handler.read()
        file_handler.close()

        print("processing contents of file %s" % (file_name))
        deconded_content = json.JSONDecoder().decode(raw_content)
        text_content = deconded_content['content']
        for paragraph in text_content:
            for sentence in paragraph:
                corpus.append(sentence)

    return corpus

def sentences_to_tree(paragraph, tree_with_entities = Tree('S', [])):
    skip_count = 0

    for sentence in paragraph:
        for index, token in enumerate(sentence):
            if skip_count > 0:
                skip_count = skip_count - 1
                continue

            if 'annotation' in token:
                annotation = token['annotation']
                if annotation['label'] == 'NAE':
                    logging.info('nltk_tree_converter.sentences_to_tree: skipping NAE label')
                    continue

                length = annotation['length']
                sub_tree = Tree(annotation['label'], [token['term']])

                if length > 1:
                    skip_count = length - 1
                    for next_index in range((index + 1), (index + length)):
                        word = sentence[next_index]['term']
                        sub_tree.append(word)

                tree_with_entities.append(sub_tree)

            else:
                tree_with_entities.extend([token['term']])

    return tree_with_entities

def train_maxent_chunker():
    print('loading...')
    with open('training/germeval/' + TEXT_SET + '.pickle', 'rb') as f:
        germ_eval_corpus = pickle.load(f)

    print('start training...')
    self_trained_chunker = maxent_chunker.NEChunkParser(germ_eval_corpus)

    print('Saving chunker to %s...' % CHUNKER_PICKLE_NAME)
    with open(CHUNKER_PICKLE_NAME, 'wb') as outfile:
        pickle.dump(self_trained_chunker, outfile, -1)

def train_maxent_chunker_with(training_set):
    print('start training...')
    return maxent_chunker.NEChunkParser(training_set)

# entry point as a stand alone script

if __name__ == '__main__':
    train_maxent_chunker()
