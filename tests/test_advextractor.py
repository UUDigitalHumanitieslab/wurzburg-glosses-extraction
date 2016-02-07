# -*- coding: utf-8 -*-

import unittest

from extractor.advextractor import create_adverb
from extractor.models import Locus


class TestAdvExtractor(unittest.TestCase):

    def test_create_adverb(self):
        s = '<b>amae</b>, <b>amæ </b>Adv. <i>Verily</i>, <i>truly</i>, <i>surely. ' \
            'amae </i>10d2, 13a21; <i>amæ </i>13a20.'
        adv = create_adverb(s)
        self.assertEqual(adv.headword, 'amae, amæ')
        self.assertEqual(adv.definition, 'Verily, truly, surely')
        self.assertEqual(len(adv.form_analyses[0].forms), 2)
        self.assertEqual(adv.form_analyses[0].forms[0].form, 'amae </i>')
        self.assertEqual(str(adv.form_analyses[0].forms[0].loci[1]), str(Locus(13, 'a', 21)))

        s = '<b>anúas </b>Adv. of place (stressed on the second syllable), lit. ' \
            '<i>From above</i>, <i>down. anúas </i>10d2, 14d6, 15a22, 16d7, 23c23.'
        adv = create_adverb(s)
        self.assertEqual(adv.headword, 'anúas')
        self.assertEqual(adv.definition, 'lit. From above, down')
        self.assertEqual(len(adv.form_analyses[0].forms), 1)
        self.assertEqual(str(adv.form_analyses[0].forms[0].loci[2]), str(Locus(15, 'a', 22)))

        s = '<b>bëos </b>Adv. <i>beos </i>8c8, 9b20, 10a25, 12d32, 14a1, 14c1, 15a34, 30b15, 33d7.'
        adv = create_adverb(s)
        self.assertEqual(adv.headword, 'bëos')
        self.assertIsNone(adv.definition)
        self.assertEqual(len(adv.form_analyses[0].forms), 1)
        self.assertEqual(adv.form_analyses[0].forms[0].form, 'beos')
        self.assertEqual(str(adv.form_analyses[0].forms[0].loci[3]), str(Locus(12, 'd', 32)))

        s = '<b>cedacht </b>Adv. (stressed on second syll.) <i>Yet</i>, <i>still</i>.'
        adv = create_adverb(s)
        self.assertEqual(adv.headword, 'cedacht')
        self.assertEqual(adv.definition, 'Yet, still')
        self.assertEqual(len(adv.form_analyses[0].forms), 0)

