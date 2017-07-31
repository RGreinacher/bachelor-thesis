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

TEXT_SET = 'NER-de-train'

def read_germeval():
    total_annotation_count = 0
    total_sentence_count = 0
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
                    total_annotation_count += count_annotations(current_sentence)
                    total_sentence_count += 1
                current_sentence = []
            else:
                current_sentence.append((row[1], row[2]))

    return total_annotation_count, total_sentence_count

def count_annotations(sentence):
    annotations = 0
    for word in sentence:
        if word[1][0] == 'B':
            annotations += 1
    return annotations

if __name__ == '__main__':
    total_annotation_count, total_sentence_count = read_germeval()
    print('%s: %s sentences and %s annotations' % (TEXT_SET, total_sentence_count, total_annotation_count))
