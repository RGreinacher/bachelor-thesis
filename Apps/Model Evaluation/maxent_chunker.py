# Natural Language Toolkit: Chunk parsing API
#
# original file: http://www.nltk.org/_modules/nltk/chunk/named_entity.html
#
# Copyright (C) 2001-2016 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
Named entity chunker
"""
from __future__ import print_function

import os, re, pickle, json, nltk
from xml.etree import ElementTree as ET

from pprint import pprint as pp

from nltk.tag import ClassifierBasedTagger, pos_tag

try:
    from nltk.classify import MaxentClassifier
except ImportError:
    pass

from nltk.tree import Tree
from nltk.tokenize import word_tokenize
from nltk.data import find

from nltk.chunk.api import ChunkParserI
from nltk.chunk.util import ChunkScore

import ner_pipeline
POS_TAGGER_PATH = 'nltk_german_pos_classifier_data.pickle'

class NEChunkParserTagger(ClassifierBasedTagger):
    """
    The IOB tagger used by the chunk parser.
    """
    def __init__(self, train):
        ClassifierBasedTagger.__init__(
            self, train=train,
            classifier_builder=self._classifier_builder)

    def _classifier_builder(self, train):
        return MaxentClassifier.train(train, algorithm='megam',
                                           gaussian_prior_sigma=1,
                                           trace=2)

    def _german_wordlist(self):
        try:
            wl = self._de_wordlist
        except AttributeError:
            self._de_wordlist = read_german_dict()
            wl = self._de_wordlist
        return wl

    def _feature_detector(self, tokens, index, history):
        word = tokens[index][0]
        pos = simplify_pos(tokens[index][1])
        if index == 0:
            prevword = prevprevword = None
            prevpos = prevprevpos = None
            prevshape = prevtag = prevprevtag = None
        elif index == 1:
            prevword = tokens[index-1][0].lower()
            prevprevword = None
            prevpos = simplify_pos(tokens[index-1][1])
            prevprevpos = None
            prevtag = history[index-1][0]
            prevshape = prevprevtag = None
        else:
            prevword = tokens[index-1][0].lower()
            prevprevword = tokens[index-2][0].lower()
            prevpos = simplify_pos(tokens[index-1][1])
            prevprevpos = simplify_pos(tokens[index-2][1])
            prevtag = history[index-1]
            prevprevtag = history[index-2]
            prevshape = shape(prevword)
        if index == len(tokens)-1:
            nextword = nextnextword = None
            nextpos = nextnextpos = None
        elif index == len(tokens)-2:
            nextword = tokens[index+1][0].lower()
            nextpos = tokens[index+1][1].lower()
            nextnextword = None
            nextnextpos = None
        else:
            nextword = tokens[index+1][0].lower()
            nextpos = tokens[index+1][1].lower()
            nextnextword = tokens[index+2][0].lower()
            nextnextpos = tokens[index+2][1].lower()

        # 89.6
        features = {
            'bias': True,
            'shape': shape(word),
            'wordlen': len(word),
            'prefix3': word[:3].lower(),
            'suffix3': word[-3:].lower(),
            'pos': pos,
            'word': word,
            'de-wordlist': (word in self._german_wordlist()),
            'prevtag': prevtag,
            'prevpos': prevpos,
            'nextpos': nextpos,
            'prevword': prevword,
            'nextword': nextword,
            'word+nextpos': '%s+%s' % (word.lower(), nextpos),
            'pos+prevtag': '%s+%s' % (pos, prevtag),
            'shape+prevtag': '%s+%s' % (prevshape, prevtag),
            }

        return features

class NEChunkParser(ChunkParserI):
    """
    Expected input: list of pos-tagged words
    """
    def __init__(self, train):
        print('load german POS tagger...')
        with open(POS_TAGGER_PATH, 'rb') as f:
            self.german_pos_tagger = pickle.load(f)

        print('start NE Chunk Parser training...')
        self._train(train)

    def parse(self, pos_tagged):
        """
        Takes a tokenized, pos-tagged sentence (list of tuples)
        """
        # pos_tagged = self.german_pos_tagger.tag(sentence)
        ne_tagged = self._tagger.tag(pos_tagged)
        tree = self._tagged_to_parse(ne_tagged)
        return tree

    def _train(self, corpus):
        # Convert to tagged sequence
        corpus = [self._parse_to_tagged(s) for s in corpus]
        self._tagger = NEChunkParserTagger(train=corpus)

    def _tagged_to_parse(self, tagged_tokens):
        """
        Convert a list of tagged tokens to a chunk-parse tree.
        """
        sent = Tree('S', [])

        for (tok,tag) in tagged_tokens:
            if tag == 'O':
                sent.append(tok)
            elif tag.startswith('B-'):
                sent.append(Tree(tag[2:], [tok]))
            elif tag.startswith('I-'):
                if (sent and isinstance(sent[-1], Tree) and
                    sent[-1].label() == tag[2:]):
                    sent[-1].append(tok)
                else:
                    sent.append(Tree(tag[2:], [tok]))
        return sent

    @staticmethod
    def _parse_to_tagged(sent):
        """
        Convert a chunk-parse tree to a list of tagged tokens.
        """
        toks = []
        for child in sent:
            if isinstance(child, Tree):
                if len(child) == 0:
                    print("Warning -- empty chunk in sentence")
                    continue
                toks.append((child[0], 'B-%s' % child.label()))
                for tok in child[1:]:
                    toks.append((tok, 'I-%s' % child.label()))
            else:
                toks.append((child, 'O'))
        return toks

def shape(word):
    if re.match('[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word, re.UNICODE):
        return 'number'
    elif re.match('\W+$', word, re.UNICODE):
        return 'punct'
    elif re.match('\w+$', word, re.UNICODE):
        if word.istitle():
            return 'upcase'
        elif word.islower():
            return 'downcase'
        else:
            return 'mixedcase'
    else:
        return 'other'

def simplify_pos(s):
    if s.startswith('V'): return "V"
    else: return s.split('-')[0]

def postag_tree(tree):
    # Part-of-speech tagging.
    words = tree.leaves()
    tagged_words = ner_pipeline.part_of_speech_tagging(words)

    tag_iter = (pos for (word, pos) in tagged_words)
    newtree = Tree('S', [])
    for child in tree:
        if isinstance(child, Tree):
            newtree.append(Tree(child.label(), []))
            for subchild in child:
                newtree[-1].append( (subchild, next(tag_iter)) )
        else:
            newtree.append( (child, next(tag_iter)) )
    return newtree

def read_german_dict():
    print('read german word list...')
    with open('german.dic', 'r', encoding='latin_1') as file_handler:
        raw_content = file_handler.readlines()

    content_list = [x.strip() for x in raw_content]
    content_set = set(content_list)

    print("processed %s words" % (len(content_set)))
    return content_set

if __name__ == '__main__':
    word_list = read_german_dict()
    print('super' in word_list)

#     training_corpus = ner_pipeline.load_annotated_raw_datum('raw_data.json')
#     tree = nltk_tree_converter.corpus_to_tree(training_corpus)
#     pos_tagged_tree = postag_tree(tree)
#     pp(pos_tagged_tree)
