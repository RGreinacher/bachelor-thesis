from itertools import repeat
from nltk import Tree
from nltk.chunk.api import ChunkParserI
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp
import csv
import json
import nltk
import pickle
import ner_pipeline

TEXT_SET = 'NER-de-test'

def read_germeval():
    nltk_trees = []
    print('reading corpus...')

    with open('training/germeval/' + TEXT_SET + '.tsv') as tsv:
        tsvin = csv.reader(
            tsv,
            delimiter='\t',
            quotechar='"',
            doublequote = True,
            quoting = csv.QUOTE_NONE
        )
        current_sentence = []

        for row in tsvin:
            if len(row) == 0:
                continue

            if row[0] == '#':
                if current_sentence != []:
                    nltk_trees.append(create_nltk_tree(current_sentence))
                current_sentence = []
            else:
                current_sentence.append((row[1], row[2]))

    return nltk_trees

def create_nltk_tree(sentence):
    tree_with_entities = Tree('S', [])
    raw_sentence = [token[0] for token in sentence]
    pos_tagged_sentence = ner_pipeline.part_of_speech_tagging(raw_sentence)

    current_sub_tree = None
    length = len(sentence)
    index = 0

    while index < length:
        ne_tag = sentence[index][1]
        pos_tuple = pos_tagged_sentence[index]
        index += 1

        if ne_tag[0] == 'O':
            if current_sub_tree:
                tree_with_entities.append(current_sub_tree)
                current_sub_tree = None
            tree_with_entities.extend([pos_tuple])

        else:
            if current_sub_tree:
                current_sub_tree.append(pos_tuple)
            else:
                current_sub_tree = Tree(ne_tag[2:], [pos_tuple])

    # print('RESULT')
    # pp(sentence)
    # pp(tree_with_entities)
    return tree_with_entities

if __name__ == '__main__':
    nltk_trees = read_germeval()
    print('Saving corpus as NLTK trees to %s...' % 'CORPUS.pickle')
    with open('training/germeval/' + TEXT_SET + '.pickle', 'wb') as outfile:
        pickle.dump(nltk_trees, outfile, -1)
