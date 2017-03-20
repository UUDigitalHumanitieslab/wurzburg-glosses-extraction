# -*- coding: utf-8 -*-

import unittest

from extractor.extractor import extract_loci, extract_forms, create_pos, extract_pos
from extractor.models import Locus, Noun, Adjective


class TestExtractor(unittest.TestCase):

    def test_extract_loci(self):
        s = '14d3, 7a, 11'
        loci, post_loci = extract_loci(s)
        self.assertEqual(len(loci), 3)
        self.assertEqual(str(loci[0]), str(Locus(14, 'd', 3)))
        self.assertEqual(str(loci[1]), str(Locus(14, 'd', 7, 'a')))
        self.assertEqual(str(loci[2]), str(Locus(14, 'd', 11)))

        s = '11b6a, 7 (quatter), 8b (ter)'
        loci, post_loci = extract_loci(s)
        self.assertEqual(len(loci), 3)
        self.assertEqual(str(loci[0]), str(Locus(11, 'b', 6, 'a')))
        self.assertEqual(str(loci[1]), str(Locus(11, 'b', 7, nr_occurrences='quatter')))
        self.assertEqual(str(loci[2]), str(Locus(11, 'b', 8, 'b', nr_occurrences='ter')))
        self.assertEqual(loci[2].nr_occurrences, 3)

        with self.assertRaises(ValueError):
            s = '11b6a, 7 (quatter), 8b (ters)'
            extract_loci(s)

        s = '30b2, 33b8 (= 33a15, ZCP XVII, 224), 34c3'
        loci, post_loci = extract_loci(s)
        self.assertEqual(len(loci), 3)
        self.assertEqual(str(loci[0]), str(Locus(30, 'b', 2)))
        self.assertEqual(str(loci[1]), str(Locus(33, 'b', 8, alternative='= 33a15, ZCP XVII, 224')))
        self.assertEqual(str(loci[2]), str(Locus(34, 'c', 3)))

        s = '5a17, 8a5 (bis; second ex. MS <i>aimm</i>), 9c29, 26a5 (bis)'
        loci, post_loci = extract_loci(s)
        self.assertEqual(len(loci), 4)
        self.assertEqual(str(loci[0]), str(Locus(5, 'a', 17)))
        self.assertEqual(str(loci[1]), str(Locus(8, 'a', 5, alternative='bis; second ex. MS <i>aimm</i>')))
        self.assertEqual(str(loci[2]), str(Locus(9, 'c', 29)))
        self.assertEqual(str(loci[3]), str(Locus(26, 'a', 5, nr_occurrences='bis')))

    def test_extract_forms(self):
        s = 'andechor 13c26 (bis), dechur 12c43, 13c26 (ter), 33c10'
        forms = extract_forms(s)
        self.assertEqual(len(forms), 2)
        self.assertEqual(forms[0].form, 'andechor')
        self.assertEqual(forms[1].form, 'dechur')

    def test_extract_pos(self):
        s = '<b>dochumacht </b>i? <i>Difficult</i>, <i>impossible</i>, \'<i>hardly possible</i>\'.'
        noun = extract_pos(s)
        self.assertEqual(noun.headword, 'dochumacht')
        self.assertEqual(noun.common_stem, 'i?')
        self.assertIsNone(noun.additional)
        self.assertEqual(noun.definition, 'Difficult, impossible, \'hardly possible')

    def test_create_pos(self):
        s = '<b>díabul </b>m. o, (without the art.) <i>The Devil</i>, <i>Satan</i>. Nsg. <i>diabul </i>26a5, ' \
            '29b19, Asg. diabul 23d8, 26a23, 28b30, <i>diab</i>ol 22d11, Gsg. ' \
            '<i>diab</i>uil 3b11'
        noun = create_pos(s)
        self.assertTrue(isinstance(noun, Noun))
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
        self.assertEqual(noun.form_analyses[1].forms[1].form, '<i>diab</i>ol')
        self.assertEqual(str(noun.form_analyses[1].forms[0].loci[1]), str(Locus(26, 'a', 23)))

        s = '<b>debuith </b>f. i (vn. of di-taa), <i>Discord</i>, <i>strife</i>, <i>quarrel</i>, <i>disputation</i>. ' \
            'Nsg. <i>debuith </i>10a8, 28b25, <i>debuid </i>31d19, Asg. <i>debuid </i>30b26, Dpl. <i>debthib </i>6b6'
        noun = create_pos(s)
        self.assertTrue(isinstance(noun, Noun))
        self.assertEqual(noun.additional, 'vn. of di-taa')
        self.assertEqual(noun.form_analyses[0].stem, 'i')

        s = '<b>abgitir </b>m. f. ? i, originally <i>The letters of the alphabet</i>, Lat. abecedarium. Nsg. ' \
            '<i>abgitir crabaith </i>33c13, Apl. <i>apgitri </i>19d12, Dpl. <i>apgitrib </i>19d5.'
        noun = create_pos(s)
        self.assertTrue(isinstance(noun, Noun))
        self.assertEqual(noun.headword, 'abgitir')
        self.assertEqual(noun.definition, '? i, originally The letters of the alphabet, Lat. abecedarium.')

        s = '<b>abstanit </b>f. (Lat. abstinentia), <i>Abstinence </i>(from food or drink). Nsg. <i>abstanit </i>' \
            '6b17, 6c15'
        adjective = create_pos(s)
        # self.assertTrue(isinstance(adjective, Adjective))
