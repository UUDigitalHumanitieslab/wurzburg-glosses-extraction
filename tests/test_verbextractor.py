# -*- coding: utf-8 -*-

import unittest

from extractor.verbextractor import find_verb, find_stem_class, match_voice, match_regex, create_verb
from extractor.regexes import VERB_PERSON, VERB_RELATIVE, VERB_PRONOMINAL_OBJECT


class TestVerbExtractor(unittest.TestCase):
    def test_find_stem_class(self):
        s = '<b>do-gair </b>Perf. 3sg. <i>dorogart </i>21d2'
        stem, pre_stem, post_stem = find_stem_class(s)
        self.assertEqual(stem, 'Perf.')
        self.assertEqual(pre_stem, '<b>do-gair </b>')
        self.assertEqual(post_stem, '3sg. <i>dorogart </i>21d2')

        s = 'Perfect. Pres. Subj. 2sg. nitáirle 30d20'
        stem, pre_stem, post_stem = find_stem_class(s)
        self.assertEqual(stem, 'Perfect. Pres. Subj.')
        self.assertEqual(pre_stem, '')
        self.assertEqual(post_stem, '2sg. nitáirle 30d20')

        s = '<b>do-airbir </b>Pass.: Pres. Ind. (vel Pres. Subj.) 3sg. with infix. pron. 1sg. <i>nimtharberar</i>9c31'
        stem, pre_stem, post_stem = find_stem_class(s)
        self.assertEqual(stem, 'Pres. Ind. (vel Pres. Subj.)')
        self.assertEqual(pre_stem, '<b>do-airbir </b>Pass.:')
        self.assertEqual(post_stem, '3sg. with infix. pron. 1sg. <i>nimtharberar</i>9c31')

        s = 'Imperf. Ind. 3sg. doberthe 10d16'
        stem, pre_stem, post_stem = find_stem_class(s)
        self.assertEqual(stem, 'Imperf. Ind.')
        self.assertEqual(pre_stem, '')
        self.assertEqual(post_stem, '3sg. doberthe 10d16')

    def test_match_voice(self):
        s = '<b>do-airbir </b>Pass.:'
        headword, is_active = match_voice(s)
        self.assertEqual(headword, '<b>do-airbir </b>')
        self.assertFalse(is_active)

        s = '<b>do-gair </b>'
        headword, is_active = match_voice(s)
        self.assertEqual(headword, '<b>do-gair </b>')
        self.assertTrue(is_active)

    def test_match_person(self):
        s = '3sg. with infix. pron. 1sg. nimtharberar 9c31'
        person, post_person = match_regex(s, VERB_PERSON)
        self.assertEqual(person, '3sg.')
        self.assertEqual(post_person, 'with infix. pron. 1sg. nimtharberar 9c31')

    def test_match_relative(self):
        s = 'with rel. n donrograd 20d9'
        relative, post_relative = match_regex(s, VERB_RELATIVE)
        self.assertEqual(relative, 'with rel. n')
        self.assertEqual(post_relative, 'donrograd 20d9')

        s = 'with elision of rel. n donrograd 20d9'
        relative, post_relative = match_regex(s, VERB_RELATIVE)
        self.assertEqual(relative, 'with elision of rel. n')
        self.assertEqual(post_relative, 'donrograd 20d9')

    def test_match_pronominal_object(self):
        s = 'with infix. pron. 1sg. nimtharberar 9c31'
        po, post_po = match_regex(s, VERB_PRONOMINAL_OBJECT)
        self.assertEqual(po, 'with infix. pron. 1sg.')
        self.assertEqual(post_po, 'nimtharberar 9c31')

        s = 'with elision of infix. pron. 1sg. nimtharberar 9c31'
        po, post_po = match_regex(s, VERB_PRONOMINAL_OBJECT)
        self.assertEqual(po, 'with elision of infix. pron. 1sg.')
        self.assertEqual(post_po, 'nimtharberar 9c31')

        s = 'with anaph. pron. doecmallaside 9d5'
        po, post_po = match_regex(s, VERB_PRONOMINAL_OBJECT)
        self.assertEqual(po, 'with anaph. pron.')
        self.assertEqual(post_po, 'doecmallaside 9d5')

    def test_extract_headword(self):
        s = '<b>dlúmigid </b><i>Masses together</i>, <i>nucleates</i>. Pass. Perf. 3sg. rondlúmigedni 12a15.'
        verb, post_verb = find_verb(s)
        self.assertEqual(verb.headword, 'dlúmigid')
        self.assertEqual(verb.definition, 'Masses together, nucleates')
        self.assertEqual(post_verb, 'Pass. Perf. 3sg. rondlúmigedni 12a15.')

    def test_create_verb(self):
        s = '<b>do-gair </b>Perf. 3sg. <i>dorogart </i>21d2, with infix. pron. 3pl. <i>dodarogart </i>22c1; \
        Pass.: Perf. 3sg. <i>dorograd </i>10a22, <i>am</i>al <i>dorograd </i>10a12, with rel. n \
        <i>donrograd </i>20d9, with infix. pron. 2pl. <i>dobrograd </i>24c4.'
        verb = create_verb(s)
        self.assertEqual(verb.headword, 'do-gair')
        self.assertEqual(len(verb.form_analyses), 5)

        fa1 = verb.form_analyses[0]
        fa2 = verb.form_analyses[1]
        fa3 = verb.form_analyses[2]
        fa4 = verb.form_analyses[3]
        fa5 = verb.form_analyses[4]

        self.assertEqual(fa1.stem, 'Perf.')
        self.assertEqual(fa2.stem, 'Perf.')
        self.assertTrue(fa2.is_active)
        self.assertFalse(fa3.is_active)
        self.assertEqual(len(fa3.forms), 2)
        self.assertFalse(fa4.is_active)
        self.assertEqual(fa4.person, '3sg.')
        self.assertEqual(fa4.relative, 'with rel. n')
        self.assertIsNone(fa5.relative)
        self.assertEqual(fa5.pronominal_object, 'with infix. pron. 2pl.')

        s = '<b>do-airbir </b>Pass.: Pres. Ind. (vel Pres. Subj.) 3sg. with infix. ' \
            'pron. 1sg. <i>nimtharberar</i>9c31, 3pl. <i>doairbertar </i>22c10, with ' \
            'rel. n <i>donairber</i>(<i>ta</i>)<i>r </i>25c23, Imperat. (vel Pres. Ind.) ' \
            '3pl. <i>tairbertar </i>25c23.'
        verb = create_verb(s)
        self.assertEqual(verb.headword, 'do-airbir')
        self.assertEqual(len(verb.form_analyses), 4)

        fa1 = verb.form_analyses[0]
        fa2 = verb.form_analyses[1]
        fa3 = verb.form_analyses[2]
        fa4 = verb.form_analyses[3]
        self.assertEqual(fa1.stem, 'Pres. Ind. (vel Pres. Subj.)')
        self.assertEqual(fa2.stem, 'Pres. Ind. (vel Pres. Subj.)')
        self.assertEqual(fa3.stem, 'Pres. Ind. (vel Pres. Subj.)')
        self.assertEqual(fa4.stem, 'Imperat. (vel Pres. Ind.)')
