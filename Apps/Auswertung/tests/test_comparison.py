#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import sys
sys.path.append('../')

# import project libs

from compare_annotations import compare_annotations_in_sentences

test_cases =[
    {
        'reference': [{'annotation': {'label': 'PER', 'length': 2}, 'term': 'Wolfgang'}, {'term': 'Schwetz'}, {'term': ','}, {'term': 'Inhaber'}, {'term': 'der'}, {'annotation': {'label': 'COM', 'length': 2}, 'term': 'Schwetz'}, {'term': 'Consulting'}, {'term': 'und'}, {'term': 'Mitglied'}, {'term': 'des'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Expertenrates'}, {'term': ','}, {'term': 'betont'}, {'term': ':'}, {'term': '``'}, {'term': 'Ziel'}, {'term': 'unserer'}, {'term': 'Initiative'}, {'term': 'ist'}, {'term': 'eine'}, {'term': 'Qualitätssicherung'}, {'term': 'der'}, {'term': 'Praxistauglichkeit'}, {'term': 'von'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Softwarelösungen'}, {'term': '.'}],
        'annotation': [{'annotation': {'label': 'COM', 'length': 2}, 'term': 'Wolfgang'}, {'term': 'Schwetz'}, {'term': ','}, {'term': 'Inhaber'}, {'annotation': {'label': 'PER', 'length': 3}, 'term': 'der'}, {'term': 'Schwetz'}, {'term': 'Consulting'}, {'term': 'und'}, {'term': 'Mitglied'}, {'term': 'des'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Expertenrates'}, {'term': ','}, {'term': 'betont'}, {'term': ':'}, {'term': '``'}, {'term': 'Ziel'}, {'term': 'unserer'}, {'term': 'Initiative'}, {'term': 'ist'}, {'term': 'eine'}, {'term': 'Qualitätssicherung'}, {'term': 'der'}, {'term': 'Praxistauglichkeit'}, {'term': 'von'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Softwarelösungen'}, {'term': '.'}],
        'target_output': [2, 3]
    },
    {
        'reference': [{'annotation': {'label': 'COM', 'length': 2}, 'term': 'Schwetz'}, {'term': 'Consulting'}, {'term': 'bescheinigt'}, {'annotation': {'label': 'COM', 'length': 1}, 'term': 'WICE'}, {'term': 'X'}, {'term': 'insgesamt'}, {'term': 'eine'}, {'term': 'überdurchschnittlich'}, {'term': 'gute'}, {'term': 'Bewertung'}, {'term': 'und'}, {'term': 'stellt'}, {'term': 'dabei'}, {'term': 'einige'}, {'term': 'Aspekte'}, {'term': 'besonders'}, {'term': 'heraus'}, {'term': '.'}],
        'annotation': [{'term': 'Schwetz'}, {'annotation': {'label': 'PER', 'length': 0}, 'term': 'Consulting'}, {'term': 'bescheinigt'}, {'term': 'WICE'}, {'term': 'X'}, {'term': 'insgesamt'}, {'term': 'eine'}, {'term': 'überdurchschnittlich'}, {'term': 'gute'}, {'term': 'Bewertung'}, {'term': 'und'}, {'term': 'stellt'}, {'term': 'dabei'}, {'term': 'einige'}, {'term': 'Aspekte'}, {'term': 'besonders'}, {'term': 'heraus'}, {'term': '.'}],
        'target_output': [3, 5]
    },
    {
        'reference': [{'term': 'Nähere'}, {'term': 'Informationen'}, {'term': 'zur'}, {'term': 'Integration'}, {'term': 'von'}, {'term': 'Social'}, {'term': 'Media'}, {'term': 'und'}, {'term': 'anderen'}, {'term': 'Aspekten'}, {'term': 'von'}, {'annotation': {'label': 'COM', 'length': 1}, 'term': 'WICE'}, {'term': 'X'}, {'term': 'sind'}, {'term': 'nachzulesen'}, {'term': 'auf'}, {'term': 'www.wice.de'}, {'term': '.'}],
        'annotation': [{'term': 'Nähere'}, {'term': 'Informationen'}, {'term': 'zur'}, {'term': 'Integration'}, {'annotation': {'label': 'COM', 'length': 2}, 'term': 'von'}, {'term': 'Social'}, {'term': 'Media'}, {'term': 'und'}, {'term': 'anderen'}, {'term': 'Aspekten'}, {'term': 'von'}, {'term': 'WICE'}, {'term': 'X'}, {'term': 'sind'}, {'term': 'nachzulesen'}, {'term': 'auf'}, {'term': 'www.wice.de'}, {'term': '.'}],
        'target_output': [4, 5]
    },
    {
        'reference': [{'annotation': {'label': 'COM', 'length': 1}, 'term': 'meinestadt.de'}, {'term': 'liefert'}, {'term': 'Internetnutzern'}, {'term': 'lokale'}, {'term': ','}, {'term': 'kulturelle'}, {'term': ','}, {'term': 'wirtschaftliche'}, {'term': 'und'}, {'term': 'touristische'}, {'term': 'Informationen'}, {'term': '.'}],
        'annotation': [{'term': 'meinestadt.de'}, {'annotation': {'label': 'PER', 'length': 1}, 'term': 'liefert'}, {'term': 'Internetnutzern'}, {'term': 'lokale'}, {'term': ','}, {'term': 'kulturelle'}, {'term': ','}, {'term': 'wirtschaftliche'}, {'term': 'und'}, {'term': 'touristische'}, {'term': 'Informationen'}, {'term': '.'}],
        'target_output': [5, 4]
    },
    {
        'reference': [{'annotation': {'label': 'PER', 'length': 2}, 'term': 'Wolfgang'}, {'term': 'Schwetz'}, {'term': ','}, {'term': 'Inhaber'}, {'term': 'der'}, {'annotation': {'label': 'COM', 'length': 2}, 'term': 'Schwetz'}, {'term': 'Consulting'}, {'term': 'und'}, {'term': 'Mitglied'}, {'term': 'des'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Expertenrates'}, {'term': ','}, {'term': 'betont'}, {'term': ':'}, {'term': '``'}, {'term': 'Ziel'}, {'term': 'unserer'}, {'term': 'Initiative'}, {'term': 'ist'}, {'term': 'eine'}, {'term': 'Qualitätssicherung'}, {'term': 'der'}, {'term': 'Praxistauglichkeit'}, {'term': 'von'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Softwarelösungen'}, {'term': '.'}],
        'annotation': [{'term': 'Wolfgang'}, {'term': 'Schwetz'}, {'term': ','}, {'term': 'Inhaber'}, {'term': 'der'}, {'term': 'Schwetz'}, {'term': 'Consulting'}, {'term': 'und'}, {'term': 'Mitglied'}, {'term': 'des'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Expertenrates'}, {'term': ','}, {'term': 'betont'}, {'term': ':'}, {'term': '``'}, {'term': 'Ziel'}, {'term': 'unserer'}, {'term': 'Initiative'}, {'term': 'ist'}, {'term': 'eine'}, {'term': 'Qualitätssicherung'}, {'term': 'der'}, {'term': 'Praxistauglichkeit'}, {'term': 'von'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Softwarelösungen'}, {'term': '.'}],
        'target_output': [5, 5]
    },
    {
        'reference': [{'term': 'Der'}, {'term': 'vollständige'}, {'term': 'Bericht'}, {'term': 'der'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Software'}, {'term': '-'}, {'term': 'Zertifizierung'}, {'term': 'steht'}, {'term': 'sowohl'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Webseite'}, {'term': 'der'}, {'annotation': {'label': 'COM', 'length': 2}, 'term': 'WICE'}, {'term': 'GmbH'}, {'term': 'unter'}, {'term': 'www.wice.de'}, {'term': 'als'}, {'term': 'auch'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Homepage'}, {'term': 'von'}, {'annotation': {'label': 'COM', 'length': 2}, 'term': 'schwetz'}, {'term': 'consulting'}, {'term': 'auf'}, {'term': 'www.schwetz.de'}, {'term': 'zum'}, {'term': 'Download'}, {'term': 'bereit'}, {'term': '.'}],
        'annotation': [{'term': 'Der'}, {'term': 'vollständige'}, {'term': 'Bericht'}, {'term': 'der'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Software'}, {'term': '-'}, {'term': 'Zertifizierung'}, {'term': 'steht'}, {'term': 'sowohl'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Webseite'}, {'term': 'der'}, {'annotation': {'label': 'COM', 'length': 2}, 'term': 'WICE'}, {'term': 'GmbH'}, {'term': 'unter'}, {'term': 'www.wice.de'}, {'term': 'als'}, {'term': 'auch'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Homepage'}, {'term': 'von'}, {'term': 'schwetz'}, {'term': 'consulting'}, {'term': 'auf'}, {'term': 'www.schwetz.de'}, {'term': 'zum'}, {'term': 'Download'}, {'term': 'bereit'}, {'term': '.'}],        'target_output': [0, 5]
    },
    {
        'reference': [{'term': 'Der'}, {'term': 'vollständige'}, {'term': 'Bericht'}, {'term': 'der'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Software'}, {'term': '-'}, {'term': 'Zertifizierung'}, {'term': 'steht'}, {'term': 'sowohl'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Webseite'}, {'term': 'der'}, {'annotation': {'label': 'COM', 'length': 1}, 'term': 'WICE'}, {'term': 'GmbH'}, {'term': 'unter', 'annotation': {'label': 'PER', 'length': 1}}, {'term': 'www.wice.de'}, {'term': 'als'}, {'term': 'auch'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Homepage'}, {'term': 'von'}, {'term': 'schwetz'}, {'term': 'consulting'}, {'term': 'auf'}, {'term': 'www.schwetz.de'}, {'term': 'zum'}, {'term': 'Download'}, {'term': 'bereit'}, {'term': '.'}],
        'annotation': [{'term': 'Der'}, {'term': 'vollständige'}, {'term': 'Bericht'}, {'term': 'der'}, {'term': 'CRM'}, {'term': '-'}, {'term': 'Software'}, {'term': '-'}, {'term': 'Zertifizierung'}, {'term': 'steht'}, {'term': 'sowohl'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Webseite'}, {'term': 'der'}, {'annotation': {'label': 'COM', 'length': 3}, 'term': 'WICE'}, {'term': 'GmbH'}, {'term': 'unter'}, {'term': 'www.wice.de'}, {'term': 'als'}, {'term': 'auch'}, {'term': 'auf'}, {'term': 'der'}, {'term': 'Homepage'}, {'term': 'von'}, {'term': 'schwetz'}, {'term': 'consulting'}, {'term': 'auf'}, {'term': 'www.schwetz.de'}, {'term': 'zum'}, {'term': 'Download'}, {'term': 'bereit'}, {'term': '.'}],
        'target_output': [1, 5]
    }
]

for index, test in enumerate(test_cases):
    analyzed_annotations = compare_annotations_in_sentences(test['reference'], test['annotation'])
    if analyzed_annotations == test['target_output']:
        print('✓ Test', index)
    else:
        print('✗ Test', index, '- should be', test['target_output'], 'but is', analyzed_annotations)
        break
