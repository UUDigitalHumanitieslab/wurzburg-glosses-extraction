# -*- coding: utf-8 -*-

import unittest

from extractor.extractor import extract_loci, extract_forms, create_pos, extract_pos
from extractor.models import Locus, Noun, Adjective


class TestExtractor(unittest.TestCase):

    def test_extract_loci(self):
        s = '14d3, 7a, 11'
        loci = extract_loci(s)
        self.assertEqual(len(loci), 3)
        self.assertEqual(str(loci[0]), str(Locus(14, 'd', 3)))
        self.assertEqual(str(loci[1]), str(Locus(14, 'd', 7, 'a')))
        self.assertEqual(str(loci[2]), str(Locus(14, 'd', 11)))

        s = '11b6a, 7 (quatter), 8b (ter)'
        loci = extract_loci(s)
        self.assertEqual(len(loci), 3)
        self.assertEqual(str(loci[0]), str(Locus(11, 'b', 6, 'a')))
        self.assertEqual(str(loci[1]), str(Locus(11, 'b', 7, '', 'quatter')))
        self.assertEqual(str(loci[2]), str(Locus(11, 'b', 8, 'b', 'ter')))
        self.assertEqual(loci[2].nr_occurrences, 3)

        with self.assertRaises(ValueError):
            s = '11b6a, 7 (quatter), 8b (ters)'
            extract_loci(s)

        s = '30b2, 33b8 (= 33a15, ZCP XVII, 224), 34c3'
        loci = extract_loci(s)
        self.assertEqual(len(loci), 3)
        self.assertEqual(str(loci[0]), str(Locus(30, 'b', 2)))
        self.assertEqual(str(loci[1]), str(Locus(33, 'b', 8, '', '', '= 33a15, ZCP XVII, 224')))
        self.assertEqual(str(loci[2]), str(Locus(34, 'c', 3)))

    def test_extract_forms(self):
        s = 'andechor 13c26 (bis), dechur 12c43, 13c26 (ter), 33c10,'
        forms = extract_forms(s)
        self.assertEqual(len(forms), 2)
        self.assertEqual(forms[0].form, 'andechor')
        self.assertEqual(forms[1].form, 'dechur')

    def test_extract_pos(self):
        s = 'dochumacht i, Difficult, impossible,\'hardly possible\'.'
        noun = extract_pos(s, Adjective)
        self.assertEqual(noun.headword, 'dochumacht')
        self.assertEqual(noun.common_stem, 'i')
        self.assertIsNone(noun.additional)
        self.assertEqual(noun.definition, 'Difficult, impossible,\'hardly possible\'')

    def test_create_pos(self):
        s = 'díabul m. o, (without the art.) The Devil, Satan. Nsg. diabul 26a5, ' \
            '29b19, Asg. diabul 23d8, 26a23, 28b30, diabol 22d11, Gsg. diabuil 3b11.'
        noun = create_pos(s, Noun)
        self.assertEqual(noun.headword, 'díabul')
        self.assertEqual(noun.common_gender, 'm')
        self.assertEqual(noun.common_stem, 'o')
        self.assertEqual(noun.additional, 'without the art.')
        self.assertEqual(noun.definition, 'The Devil, Satan')

        self.assertEqual(len(noun.form_analyses), 3)
        self.assertEqual(noun.form_analyses[0].stem, 'o')
        self.assertEqual(noun.form_analyses[0].case, 'Nsg')
        self.assertEqual(noun.form_analyses[0].gender, 'm')
        self.assertEqual(noun.form_analyses[1].stem, 'o')
        self.assertEqual(noun.form_analyses[1].case, 'Asg')
        self.assertEqual(noun.form_analyses[1].gender, 'm')
        self.assertEqual(noun.form_analyses[2].stem, 'o')
        self.assertEqual(noun.form_analyses[2].case, 'Gsg')
        self.assertEqual(noun.form_analyses[2].gender, 'm')

        self.assertEqual(len(noun.form_analyses[1].forms), 2)
        self.assertEqual(noun.form_analyses[1].forms[1].form, 'diabol')
        self.assertEqual(str(noun.form_analyses[1].forms[0].loci[1]), str(Locus(26, 'a', 23)))
