# -*- coding: utf-8 -*-

import unittest

from extractor.models import Preposition, Locus
from extractor.prepextractor import add_article_form_analyses, add_pron_form_analyses


class TestPrepExtractor(unittest.TestCase):

    def test_add_article_form_analyses(self):
        s = 'With the art. and subst.: f. cossin noin 2a21, 22, cosin noin 2a21, n. cossalaasa 23a17.'
        prep = Preposition('', '', common_case='acc')
        add_article_form_analyses(s, prep)
        self.assertEqual(len(prep.form_analyses), 2)
        self.assertEqual(prep.form_analyses[0].case, 'acc')
        self.assertEqual(prep.form_analyses[0].classifier, 'With the art. and subst.: ')
        self.assertEqual(prep.form_analyses[0].gender, 'f')
        self.assertEqual(prep.form_analyses[0].forms[0].form, 'cossin noin')
        self.assertEqual(str(prep.form_analyses[0].forms[0].loci[1]), str(Locus(2, 'a', 22)))
        self.assertEqual(prep.form_analyses[1].gender, 'n')

    def test_add_pron_form_analyses(self):
        s = 'With suffix. pron. 3sg. m. etir 28b3, 1pl. etronn 15a32, etrunn 31a11, \
with emph. pron. 1pl. etrunni 12b12, 2pl. etruib 24c22, 27b18, 21 (bis), 3pl. etarru 7d10, 27d19, ettarru 33b18.'
        prep = Preposition('', '', common_case='acc')
        add_pron_form_analyses(s, prep)

        s = 'With suffix. pron. 3sg. n. occo, occa, oca: occo 3c24, 4a26, 5a26, 6a14, 22, 6d3, \
7c4, 8d15, occa: occa 3c25, 8a11, 9d22, 11b4, 24a20, 26d8, 18, 29d6, oca: oca 33d7.'
