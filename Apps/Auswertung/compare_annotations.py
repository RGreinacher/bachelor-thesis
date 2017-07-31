#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import re
import json
import argparse
import json
import collections
import copy
from os import listdir
from os.path import isfile, join
from pprint import pprint as pp
from operator import itemgetter

# import project libs

from constants import *
from helper import *
from answer_class_correction_analysis import *

# settings

BE_VERBOSE = True

# methods

def general_corpus_information(annotated_corpus):
    (paragraphs, sentences, tokens, _, _) = corpus_runner(annotated_corpus)
    reading_time = round(tokens / 240, 1)
    print('Corpus contains', paragraphs, 'paragraphs,', sentences, 'sentences and', tokens, 'tokens.')
    print('Estimated reading time:', reading_time, 'min')

def questionnaire_evaluation(subject_id, questionnaire_corpus_document):
    def restructure(seq):
        return dict((d['id'], d['selected']) for (index, d) in enumerate(seq))

    questionnaires = sorted(questionnaire_corpus_document['data'], key=itemgetter('order'))
    original_order_questionnaires = copy.deepcopy(questionnaires)
    demographic = restructure(questionnaires.pop(4)['answers'])

    annotation_experience_prefix = 'not '
    if demographic['experience_text_annotation'] == 'Ja':
        annotation_experience_prefix = ''
    print("Subject #%s (%s, %s): %sexperienced annotator, computer experience %s/7" % (subject_id, demographic['age'], demographic['sex'], annotation_experience_prefix, demographic['experience_computer']))

    sorted_quesionnaires = [[], [], demographic]
    for questionnaire in questionnaires:
        restructured_questionnaire = restructure(questionnaire['answers'])
        restructured_questionnaire['order'] = questionnaire['order']
        block_was_annotated = 'reliability' in restructured_questionnaire
        sorted_quesionnaires[block_was_annotated].append(restructured_questionnaire)

    return (sorted_quesionnaires, original_order_questionnaires)

def general_subject_annotation_analysis(gold_annotated_corpus, subject_annotated_corpus, durations_per_block):
    (_, _, _, gold_annotations, gold_words) = corpus_runner(gold_annotated_corpus)
    (_, _, _, subject_annotations, subject_words) = corpus_runner(subject_annotated_corpus)
    total_seconds = sum(list(map(lambda x: sum(x), durations_per_block)))

    print("made %s/%s annotations (%s/%s words) in %s minutes" % (subject_annotations, gold_annotations, subject_words, gold_words, seconds_to_min(total_seconds)))

def quantitative_analysis(subject_annotation_classes, subject_id, subject_table, empty_subjects_table, annotation_durations_per_block, questionnaire_information):
    level = subject_id % 3
    class_rates = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    total_annotations_per_level = [0, 0]
    annotation_durations_per_level = [0, 0]
    average_monotony = [0, 0]
    average_stress = [0, 0]
    average_reliability = sum(int(answers['reliability']) for answers in questionnaire_information[1]) / 2.0
    average_correctness = sum(int(answers['correctness']) for answers in questionnaire_information[1]) / 2.0

    for block_index, block in enumerate(subject_annotation_classes):
        subject_table_block = subject_table[block_index]
        block_was_annotated = subject_table_block_is_annotated(subject_table_block)

        total_annotations_per_level[block_was_annotated] += annotations_per_subject_table_block(empty_subjects_table[block_index])
        annotation_durations_per_level[block_was_annotated] += sum(annotation_durations_per_block[block_index])
        average_monotony[block_was_annotated] = sum(int(answers['monotonous']) for answers in questionnaire_information[block_was_annotated]) / 2.0
        average_stress[block_was_annotated] = sum(int(answers['stress']) for answers in questionnaire_information[block_was_annotated]) / 2.0

        distribution = distribution_per_block(block)
        for class_rate_index, class_rate in enumerate(distribution):
            class_rates[block_was_annotated][class_rate_index] += class_rate

    for block_was_annotated, class_rates_per_level in enumerate(class_rates):
        total_annotations = total_annotations_per_level[block_was_annotated]
        percental_distribution = list(map(lambda x: str(round(((x * 100.0) / total_annotations), 3)) + '%', class_rates_per_level))
        percental_correct_annotations = percental_distribution.pop(0)
        correct_annotations = class_rates_per_level[0]

        formatted_duration = seconds_to_min(annotation_durations_per_level[block_was_annotated])
        duration_per_annotation = round(annotation_durations_per_level[block_was_annotated] / total_annotations, 3)

        print()
        if block_was_annotated == 1:
            print("%s minutes using a %s%% correct assistance system - %s seconds/annotation" % (formatted_duration, ASSISTANCE_SYSTEM_LEVELS[level], duration_per_annotation))
            print("\taverage guessed assistance system reliability: %s/7" % (average_reliability))
            print("\taverage guessed assistance system correctness: %s%%" % (average_correctness))
        else:
            print("%s minutes without an assistance system - %s seconds/annotation" % (formatted_duration, duration_per_annotation))

        print("\taverage monotony: %s/7" % (average_monotony[block_was_annotated]))
        print("\taverage stress: %s/7" % (average_stress[block_was_annotated]))

        print()
        for answer_class_index in range(0, 6):
            if answer_class_index == 0:
                print("\t%s: %s (%s/%s)" % (ANNOTATION_ANSWER_CLASSES[answer_class_index], percental_correct_annotations, correct_annotations, total_annotations))
            else:
                print("\t%s: %s (%s)" % (ANNOTATION_ANSWER_CLASSES[answer_class_index], percental_distribution[answer_class_index - 1], class_rates_per_level[answer_class_index]))

def subject_annotation_classes(gold_annotated_corpus, subject_corpus, subject_annotated_corpus, subject_table):
    blocks = []
    block = []
    block_index = 0
    paragraph_index_per_block = -1

    for document_index, document in enumerate(subject_corpus):
        for paragraph_index, paragraph in enumerate(document['data']):
            paragraph_index_per_block += 1
            annotations_per_paragraph = []

            for sentence_index, subject_sentence in enumerate(paragraph):
                gold_annotated_sentence = gold_annotated_corpus[document_index]['data'][paragraph_index][sentence_index]
                subject_annotated_sentence = subject_annotated_corpus[document_index]['data'][paragraph_index][sentence_index]

                if len(gold_annotated_sentence) != len(subject_annotated_sentence):
                    print('gold')
                    pp(gold_annotated_sentence)
                    print('subject')
                    pp(subject_annotated_sentence)
                    print('LENGTH MISSMATCH!')
                    exit()

                annotations_of_sentence = compare_annotations_in_sentences(gold_annotated_sentence, subject_annotated_sentence)
                annotations_per_paragraph.append(annotations_of_sentence)

            if paragraph_index_per_block == len(subject_table[block_index]):
                blocks.append(block)
                block = [annotations_per_paragraph]

                block_index += 1
                paragraph_index_per_block = 0
            else:
                block.append(annotations_per_paragraph)

    blocks.append(block)
    return blocks

def compare_annotations_in_sentences(gold_annotated_sentence, subject_annotated_sentence):
    annotations_per_sentence = []
    last_gold_annotation_index = -1
    last_subject_annotation_index = -1

    for token_index, gold_token in enumerate(gold_annotated_sentence):
        subject_token = subject_annotated_sentence[token_index]

        if 'annotation' in gold_token and token_index != last_gold_annotation_index:
            last_gold_annotation_index = token_index
            gold_annotation = gold_token['annotation']

            # same annotation start
            if 'annotation' in subject_token:
                last_subject_annotation_index = token_index
                subject_annotation = subject_token['annotation']
                length = gold_annotation['length'] == subject_annotation['length']
                label = gold_annotation['label'] == subject_annotation['label']

                # correct annotation
                if gold_annotation == subject_annotation:
                    annotations_per_sentence.append(0)

                # too short or too long
                elif label and not length:
                    annotations_per_sentence.append(1)

                # wrong category
                elif length and not label:
                    annotations_per_sentence.append(2)

                # length and category wrong
                else:
                    annotations_per_sentence.append(3)

            # no subject annotation
            else:
                next_gold_annotation_index = next_annotation_index(token_index + 1, gold_annotated_sentence)
                next_subject_annotation_index = next_annotation_index(token_index + 1, subject_annotated_sentence)

                # no subject annotation left
                if next_subject_annotation_index == -1:
                    annotations_per_sentence.append(5)

                # upcoming subject annotation is overlapping the current gold annotation
                elif (token_index + gold_annotation['length'] - 1) >= next_subject_annotation_index:
                    last_subject_annotation_index = next_subject_annotation_index # save that this subject annotation was already handeled

                    # upcoming with same label
                    if gold_annotation['label'] == subject_annotated_sentence[next_subject_annotation_index]['annotation']['label']:
                        annotations_per_sentence.append(1)

                    # upcoming with different label
                    else:
                        annotations_per_sentence.append(3)

                # not overlapping and no gold annotation left => just unnecessary annotations
                elif next_gold_annotation_index == -1:

                    annotations_per_sentence.append(5) # current position was omitted

                    while next_subject_annotation_index >= 0:
                        annotations_per_sentence.append(4)
                        next_subject_annotation_index = next_annotation_index(next_subject_annotation_index + 1, subject_annotated_sentence)
                    break
                    last_subject_annotation_index = next_subject_annotation_index # save that this subject annotation was already handeled

                # there is a subject and a gold annotation ahead, subject first
                elif next_subject_annotation_index < next_gold_annotation_index:
                    last_subject_annotation_index = next_subject_annotation_index # save that this subject annotation was already handeled
                    next_subject_annotation = subject_annotated_sentence[next_subject_annotation_index]['annotation']

                    # the upcoming annotation is overlapping the next gold annotation
                    if (next_subject_annotation_index + next_subject_annotation['length'] - 1) >= next_gold_annotation_index:
                        annotations_per_sentence.append(5) # the current annotation position was omitted
                        last_gold_annotation_index = next_gold_annotation_index
                        next_gold_annotation = gold_annotated_sentence[next_gold_annotation_index]['annotation']

                        # just the span is wrong
                        if next_subject_annotation['label'] == next_gold_annotation['label']:
                            annotations_per_sentence.append(1)

                        # span and cat is wrong
                        else:
                            annotations_per_sentence.append(3)

                    # the subject's annotation is not overlapping a gold annotation
                    else:
                        annotations_per_sentence.append(5) # current position was omitted
                        annotations_per_sentence.append(4) # wrong annotation was made

                # there is a subject and a gold annotation ahead, gold first or both with same index
                else:
                    annotations_per_sentence.append(5)

        # the first annotation in the paragraph is before a gold annotation
        elif 'annotation' in subject_token and token_index > last_subject_annotation_index: # and last_gold_annotation_index == -1:
            next_gold_annotation_index = next_annotation_index(token_index + 1, gold_annotated_sentence)

            # no (more) gold annotation present
            if next_gold_annotation_index < 0:
                annotations_per_sentence.append(4)

            # a gold annotation is ahead
            else:
                next_gold_annotation = gold_annotated_sentence[next_gold_annotation_index]['annotation']
                subject_annotation = subject_token['annotation']

                # subject's annotation is overlapping
                if (token_index + subject_annotation['length'] - 1) >= next_gold_annotation_index:
                    last_gold_annotation_index = next_gold_annotation_index

                    # just the span is wrong
                    if subject_annotation['label'] == next_gold_annotation['label']:
                        annotations_per_sentence.append(1)

                    # span and cat is wrong
                    else:
                        annotations_per_sentence.append(3)

                # annotation is not overlapping
                else:
                    annotations_per_sentence.append(4)

    return annotations_per_sentence

    total_annotations = sum(total_class_distribution)
    return list(map(lambda x: round((x * 100.0) / total_annotations, 3), total_class_distribution))

def combine_to_data_frame(subject_id, subject_table, empty_subjects_table, annotation_classes, annotation_durations_per_block, questionnaires):
    data_row = [subject_id] # VP ID

    # demographic questionnaire
    demographic = questionnaires.pop(4)['answers']
    for item in demographic:
        if item['id'] == 'study_subject' or item['id'] == 'profession':
            data_row.append(item['selected'])
        elif item['id'] == 'study_semester':
            parsable = item['selected']
            if parsable == '':
                data_row.append(None)
            else:
                data_row.append(int(parsable))
        elif item['id'] == 'sex':
            if item['selected'] == 'männlich':
                data_row.append('m')
            elif item['selected'] == 'weiblich':
                data_row.append('w')
            else:
                data_row.append('-')
        else:
            parsable = item['selected']
            try:
                value = int(parsable)
            except ValueError:
                if parsable == 'Nein':
                    value = 'FALSE'
                elif parsable == 'Ja':
                    value = 'TRUE'
            data_row.append(value)

    data_row.append(reward_for_subject(subject_id)) # reward
    data_row.append(ASSISTANCE_SYSTEM_LEVELS[subject_id % 3]) # assistance level

    # block specific
    interim_results = [
        [],
        [],
        [],
        []
    ]
    for block_index in range(0, 4):
        block_was_annotated = subject_table_block_is_annotated(subject_table[block_index])
        interim_results[block_index].append(block_was_annotated)
        data_row.append(block_was_annotated) # AS active

        seconds_per_block = sum(annotation_durations_per_block[block_index])
        data_row.append(seconds_per_block) # seconds per block

        annotation_count = annotations_per_subject_table_block(empty_subjects_table[block_index])
        avg_time = round(seconds_per_block / annotation_count, 6)
        interim_results[block_index].append(avg_time)
        data_row.append(avg_time) # time per annotation

        distribution = distribution_per_block(annotation_classes[block_index])
        correct_annotation_count = distribution[0]
        avg_correct_time = round(seconds_per_block / correct_annotation_count, 6)
        interim_results[block_index].append(avg_correct_time) # time per correct annotation

        correctness_percentage = round((correct_annotation_count / annotation_count) * 100.0, 6)
        interim_results[block_index].append(correctness_percentage)
        data_row.append(correctness_percentage) # correctness, percentage

        data_row.append(annotation_count) # number of annotations
        data_row.append(correct_annotation_count) # number of correct annotations
        data_row.append(distribution[1]) # number of wrong span annotations
        data_row.append(distribution[2]) # number of wrong cat annotations
        data_row.append(distribution[3]) # number of wrong span & cat annotations
        data_row.append(distribution[4]) # number of unnecessary annotations
        data_row.append(distribution[5]) # number of missed annotations
        interim_results[block_index].append(distribution[5] / annotation_count)

        questionnair_answers = questionnaires[block_index]['answers']
        data_row.append(int(questionnair_answers[0]['selected'])) # questionnaire stress
        data_row.append(int(questionnair_answers[1]['selected'])) # questionnaire monotonous
        if block_was_annotated:
            data_row.append(int(questionnair_answers[2]['selected'])) # questionnaire assistance reliability
            data_row.append(int(questionnair_answers[3]['selected'])) # questionnaire assistance correctness
        else:
            data_row.append(None) # questionnaire assistance reliability
            data_row.append(None) # questionnaire assistance correctness

        # preannotation changes
        preannotation_distribution = distribution_per_block(subject_table[block_index])
        preannotation_changes = quantitative_answer_class_correction_analysis_per_block(
            annotation_classes[block_index],
            subject_table[block_index]
        )
        for preannotation_class in range(0, 6):
            data_row.append(preannotation_distribution[preannotation_class])
            for correction_index in range(0, 6):
                data_row.append(preannotation_changes[preannotation_class][correction_index])
        data_row.append(preannotation_changes[6])

    # inter block ratios
    if interim_results[0][0]: # first block was annotated
        data_row.append(interim_results[0][3] - interim_results[1][3]) # assistance_no_assistance_correctness_difference_block_0_1
        data_row.append(interim_results[0][1] - interim_results[1][1]) # assistance_no_assistance_time_difference_block_0_1
        data_row.append(interim_results[0][2] - interim_results[1][2]) # assistance_no_assistance_correct_time_difference_block_0_1
        data_row.append(interim_results[0][4] - interim_results[1][4]) # assistance_no_assistance_misses_ratio_difference_block_0_1
        data_row.append(interim_results[2][3] - interim_results[3][3]) # assistance_no_assistance_correctness_difference_block_2_3
        data_row.append(interim_results[2][1] - interim_results[3][1]) # assistance_no_assistance_time_difference_block_2_3
        data_row.append(interim_results[2][2] - interim_results[3][2]) # assistance_no_assistance_correct_time_difference_block_2_3
        data_row.append(interim_results[2][4] - interim_results[3][4]) # assistance_no_assistance_misses_ratio_difference_block_2_3
    else:
        data_row.append(interim_results[1][3] - interim_results[0][3]) # assistance_no_assistance_correctness_difference_block_0_1
        data_row.append(interim_results[1][1] - interim_results[0][1]) # assistance_no_assistance_time_difference_block_0_1
        data_row.append(interim_results[1][2] - interim_results[0][2]) # assistance_no_assistance_correct_time_difference_block_0_1
        data_row.append(interim_results[1][4] - interim_results[0][4]) # assistance_no_assistance_misses_ratio_difference_block_0_1
        data_row.append(interim_results[3][3] - interim_results[2][3]) # assistance_no_assistance_correctness_difference_block_2_3
        data_row.append(interim_results[3][1] - interim_results[2][1]) # assistance_no_assistance_time_difference_block_2_3
        data_row.append(interim_results[3][2] - interim_results[2][2]) # assistance_no_assistance_correct_time_difference_block_2_3
        data_row.append(interim_results[3][4] - interim_results[2][4]) # assistance_no_assistance_misses_ratio_difference_block_2_3

    return data_row

def iteration_for_subject(subject_id, subjects_table, gold_annotated_corpus, empty_subjects_table):
    print()

    # read subject files
    subject_table = subjects_table[subject_id]
    subject_corpus = read_corpus_files(SUBJECT_CORPUS_FILES, subject_id)
    subject_annotated_corpus = read_corpus_files(SUBJECT_ANNOTATED_CORPUS_FILES, subject_id)

    # general subject information
    (questionnaire_information, original_order_questionnaires) = questionnaire_evaluation(subject_id, subject_annotated_corpus.pop(0))

    # basic analysis of subject's annotations and durations
    annotation_durations_per_block = annotation_durations(subject_table, subject_annotated_corpus)

    # analyse annotation classes
    annotation_classes = subject_annotation_classes(gold_annotated_corpus, subject_corpus, subject_annotated_corpus, subject_table)

    if BE_VERBOSE:
        general_subject_annotation_analysis(
            gold_annotated_corpus,
            subject_annotated_corpus,
            annotation_durations_per_block
        )
        quantitative_analysis(
            annotation_classes,
            subject_id,
            subject_table,
            empty_subjects_table,
            annotation_durations_per_block,
            questionnaire_information
        )

    # create data frame row
    data_frame_row = combine_to_data_frame(
        subject_id,
        subject_table,
        empty_subjects_table,
        annotation_classes,
        annotation_durations_per_block,
        original_order_questionnaires
    )
    return (annotation_classes, data_frame_row)

# entry point as a stand alone script

if __name__ == '__main__':
    annotation_classes = []
    data_frame_list = []

    # read general data
    subjects_table = read_subject_table()
    gold_annotated_corpus = read_corpus_files(GOLD_ANNOTATED_CORPUS_FILES)
    general_corpus_information(gold_annotated_corpus)
    empty_subjects_table = empty_subjects_table(subjects_table)

    # (annotations, _) = iteration_for_subject(0, subjects_table, gold_annotated_corpus, empty_subjects_table)
    # exit()

    for subject_id in range(0, 66):
        (annotations, data_frame_row) = iteration_for_subject(subject_id, subjects_table, gold_annotated_corpus, empty_subjects_table)
        annotation_classes.append(annotations)
        data_frame_list.append(data_frame_row)

    print()
    print('saving collected data to files...')
    save_json(annotation_classes, JSON_ANNOTATION_CLASSES_FILE_NAME)
    save_json(data_frame_list, JSON_DATA_FRAME_FILE_NAME)
    save_csv(data_frame_list)
