#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SOURCE FILES

SUBJECTS_TABEL_JSON = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Apps/Vorverarbeitung/subjects_table.json'
GOLD_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/Implisense/json gold/'
SUBJECT_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP vorbereitet/'
SUBJECT_ANNOTATED_CORPUS_FILES = '/Users/rg/Nextcloud/Uni/Bachelorarbeit/Korpora/VP annotiert/'

# TARGET FILES

JSON_ANNOTATION_CLASSES_FILE_NAME = 'data/annotation_classes_per_subject.json'
CSV_DATA_FILE_NAME = 'data/data_frame.csv'
JSON_DATA_FRAME_FILE_NAME = 'data/data_frame.json'

# constants

ASSISTANCE_SYSTEM_LEVELS = {
    0: 10,
    1: 50,
    2: 90,
}

ASSISTANCE_SYSTEM_LEVELS_AS_TEXT = {
    0: 'ohne Assistenz',
    1: 'bei 10% korrekter Assistenz',
    2: 'bei 50% korrekter Assistenz',
    3: 'bei 90% korrekter Assistenz',
}

ANNOTATION_ANSWER_CLASSES = [
    'correct',
    'wrong span',
    'wrong category',
    'wrong span & category',
    'unnecessary',
    'missed'
]

REWARDS = [
  [ 38 ], # Nichts
  [ 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 28, 29, 30, 32, 33, 35, 36, 37, 39, 40, 44, 45, 48 ], # Gutschein
  [ 6, 11, 20, 23, 24, 31, 34, 42, 43, 50 ], # VP Stunden + Gutschein
  [ 0, 41, 46, 47, 49, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65 ] # Geld
]

DATA_FRAME_HEADER = [
    # general information
    'subject_id', 'sex', 'age', 'color_blindness', 'experience_text_annotation', 'currently_studying', 'study_subject', 'study_semester', 'profession', 'experience_computer', 'reward', 'assistance_level',

    # block_0
    'block_0_assistance_present', 'block_0_time_block', 'block_0_time_avg_per_annotation', 'block_0_correctness', 'block_0_total_annotations_count', 'block_0_correct_count', 'block_0_mistake_span_count', 'block_0_mistake_category_count', 'block_0_mistake_span_category_count', 'block_0_mistake_unnecessary_count', 'block_0_mistake_missed_count', 'block_0_questionnaire_stress', 'block_0_questionnaire_monotonous', 'block_0_questionnaire_reliability', 'block_0_questionnaire_correctness',
    # preannotation changes
    'block_0_total_class_0_preannotation_count',
    'block_0_0_to_0_count', 'block_0_0_to_1_count', 'block_0_0_to_2_count', 'block_0_0_to_3_count', 'block_0_0_to_4_count', 'block_0_0_to_5_count',
    'block_0_total_class_1_preannotation_count',
    'block_0_1_to_0_count', 'block_0_1_to_1_count', 'block_0_1_to_2_count', 'block_0_1_to_3_count', 'block_0_1_to_4_count', 'block_0_1_to_5_count',
    'block_0_total_class_2_preannotation_count',
    'block_0_2_to_0_count', 'block_0_2_to_1_count', 'block_0_2_to_2_count', 'block_0_2_to_3_count', 'block_0_2_to_4_count', 'block_0_2_to_5_count',
    'block_0_total_class_3_preannotation_count',
    'block_0_3_to_0_count', 'block_0_3_to_1_count', 'block_0_3_to_2_count', 'block_0_3_to_3_count', 'block_0_3_to_4_count', 'block_0_3_to_5_count',
    'block_0_total_class_4_preannotation_count',
    'block_0_4_to_0_count', 'block_0_4_to_1_count', 'block_0_4_to_2_count', 'block_0_4_to_3_count', 'block_0_4_to_4_count', 'block_0_4_to_5_count',
    'block_0_total_class_5_preannotation_count',
    'block_0_5_to_0_count', 'block_0_5_to_1_count', 'block_0_5_to_2_count', 'block_0_5_to_3_count', 'block_0_5_to_4_count', 'block_0_5_to_5_count',
    'block_0_additional_class_4_mistake_count',

    # block_1
    'block_1_assistance_present', 'block_1_time_block', 'block_1_time_avg_per_annotation', 'block_1_correctness', 'block_1_total_annotations_count', 'block_1_correct_count', 'block_1_mistake_span_count', 'block_1_mistake_category_count', 'block_1_mistake_span_category_count', 'block_1_mistake_unnecessary_count', 'block_1_mistake_missed_count', 'block_1_questionnaire_stress', 'block_1_questionnaire_monotonous', 'block_1_questionnaire_reliability', 'block_1_questionnaire_correctness',
    # preannotation changes
    'block_1_total_class_0_preannotation_count',
    'block_1_0_to_0_count', 'block_1_0_to_1_count', 'block_1_0_to_2_count', 'block_1_0_to_3_count', 'block_1_0_to_4_count', 'block_1_0_to_5_count',
    'block_1_total_class_1_preannotation_count',
    'block_1_1_to_0_count', 'block_1_1_to_1_count', 'block_1_1_to_2_count', 'block_1_1_to_3_count', 'block_1_1_to_4_count', 'block_1_1_to_5_count',
    'block_1_total_class_2_preannotation_count',
    'block_1_2_to_0_count', 'block_1_2_to_1_count', 'block_1_2_to_2_count', 'block_1_2_to_3_count', 'block_1_2_to_4_count', 'block_1_2_to_5_count',
    'block_1_total_class_3_preannotation_count',
    'block_1_3_to_0_count', 'block_1_3_to_1_count', 'block_1_3_to_2_count', 'block_1_3_to_3_count', 'block_1_3_to_4_count', 'block_1_3_to_5_count',
    'block_1_total_class_4_preannotation_count',
    'block_1_4_to_0_count', 'block_1_4_to_1_count', 'block_1_4_to_2_count', 'block_1_4_to_3_count', 'block_1_4_to_4_count', 'block_1_4_to_5_count',
    'block_1_total_class_5_preannotation_count',
    'block_1_5_to_0_count', 'block_1_5_to_1_count', 'block_1_5_to_2_count', 'block_1_5_to_3_count', 'block_1_5_to_4_count', 'block_1_5_to_5_count',
    'block_1_additional_class_4_mistake_count',

    # block_2
    'block_2_assistance_present', 'block_2_time_block', 'block_2_time_avg_per_annotation', 'block_2_correctness', 'block_2_total_annotations_count', 'block_2_correct_count', 'block_2_mistake_span_count', 'block_2_mistake_category_count', 'block_2_mistake_span_category_count', 'block_2_mistake_unnecessary_count', 'block_2_mistake_missed_count', 'block_2_questionnaire_stress', 'block_2_questionnaire_monotonous', 'block_2_questionnaire_reliability', 'block_2_questionnaire_correctness',
    # preannotation changes
    'block_2_total_class_0_preannotation_count',
    'block_2_0_to_0_count', 'block_2_0_to_1_count', 'block_2_0_to_2_count', 'block_2_0_to_3_count', 'block_2_0_to_4_count', 'block_2_0_to_5_count',
    'block_2_total_class_1_preannotation_count',
    'block_2_1_to_0_count', 'block_2_1_to_1_count', 'block_2_1_to_2_count', 'block_2_1_to_3_count', 'block_2_1_to_4_count', 'block_2_1_to_5_count',
    'block_2_total_class_2_preannotation_count',
    'block_2_2_to_0_count', 'block_2_2_to_1_count', 'block_2_2_to_2_count', 'block_2_2_to_3_count', 'block_2_2_to_4_count', 'block_2_2_to_5_count',
    'block_2_total_class_3_preannotation_count',
    'block_2_3_to_0_count', 'block_2_3_to_1_count', 'block_2_3_to_2_count', 'block_2_3_to_3_count', 'block_2_3_to_4_count', 'block_2_3_to_5_count',
    'block_2_total_class_4_preannotation_count',
    'block_2_4_to_0_count', 'block_2_4_to_1_count', 'block_2_4_to_2_count', 'block_2_4_to_3_count', 'block_2_4_to_4_count', 'block_2_4_to_5_count',
    'block_2_total_class_5_preannotation_count',
    'block_2_5_to_0_count', 'block_2_5_to_1_count', 'block_2_5_to_2_count', 'block_2_5_to_3_count', 'block_2_5_to_4_count', 'block_2_5_to_5_count',
    'block_2_additional_class_4_mistake_count',

    # block_3
    'block_3_assistance_present', 'block_3_time_block', 'block_3_time_avg_per_annotation', 'block_3_correctness', 'block_3_total_annotations_count', 'block_3_correct_count', 'block_3_mistake_span_count', 'block_3_mistake_category_count', 'block_3_mistake_span_category_count', 'block_3_mistake_unnecessary_count', 'block_3_mistake_missed_count', 'block_3_questionnaire_stress', 'block_3_questionnaire_monotonous', 'block_3_questionnaire_reliability', 'block_3_questionnaire_correctness',
    # preannotation changes
    'block_3_total_class_0_preannotation_count',
    'block_3_0_to_0_count', 'block_3_0_to_1_count', 'block_3_0_to_2_count', 'block_3_0_to_3_count', 'block_3_0_to_4_count', 'block_3_0_to_5_count',
    'block_3_total_class_1_preannotation_count',
    'block_3_1_to_0_count', 'block_3_1_to_1_count', 'block_3_1_to_2_count', 'block_3_1_to_3_count', 'block_3_1_to_4_count', 'block_3_1_to_5_count',
    'block_3_total_class_2_preannotation_count',
    'block_3_2_to_0_count', 'block_3_2_to_1_count', 'block_3_2_to_2_count', 'block_3_2_to_3_count', 'block_3_2_to_4_count', 'block_3_2_to_5_count',
    'block_3_total_class_3_preannotation_count',
    'block_3_3_to_0_count', 'block_3_3_to_1_count', 'block_3_3_to_2_count', 'block_3_3_to_3_count', 'block_3_3_to_4_count', 'block_3_3_to_5_count',
    'block_3_total_class_4_preannotation_count',
    'block_3_4_to_0_count', 'block_3_4_to_1_count', 'block_3_4_to_2_count', 'block_3_4_to_3_count', 'block_3_4_to_4_count', 'block_3_4_to_5_count',
    'block_3_total_class_5_preannotation_count',
    'block_3_5_to_0_count', 'block_3_5_to_1_count', 'block_3_5_to_2_count', 'block_3_5_to_3_count', 'block_3_5_to_4_count', 'block_3_5_to_5_count',
    'block_3_additional_class_4_mistake_count',

    # inter block ratios
    'assistance_no_assistance_correctness_difference_block_0_1',
    'assistance_no_assistance_time_difference_block_0_1',
    'assistance_no_assistance_correct_time_difference_block_0_1',
    'assistance_no_assistance_misses_ratio_difference_block_0_1',
    'assistance_no_assistance_correctness_difference_block_2_3',
    'assistance_no_assistance_time_difference_block_2_3',
    'assistance_no_assistance_correct_time_difference_block_2_3',
    'assistance_no_assistance_misses_ratio_difference_block_2_3'
]
