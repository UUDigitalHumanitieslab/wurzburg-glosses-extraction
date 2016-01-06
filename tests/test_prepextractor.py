# -*- coding: utf-8 -*-

import unittest

from extractor.models import Preposition, Locus
from extractor.prepextractor import add_simple_forms, add_article_forms, add_pron_form_analyses


class TestPrepExtractor(unittest.TestCase):

    def test_add_simple_form_analyses(self):
        s = 'With subst.s, pronom.s, and vn.s. Before (a) Vowels a, e and graphic h: coadam 17b29, \
co euam 17b29, cohóir 18d10. (b) Cons.s (1) b: co burpi 17c23. (2) t, c: cotecht 9d32, cotíchtin 25d1, \
co crist 2a21, cocenn 23a19. (3) l, m, n, r: colaa 5b4, collaa 5b4, comoidim 17d19, conuie 4b29, \
conech 26b25, ressurectionem christo 24a11. (4) f: cofer 9d31, 32, coforcenn 14c14.'
        prep = Preposition('', '', common_case='acc')
        add_simple_forms(s, prep)
        self.assertEqual(len(prep.form_analyses[0].forms), 16)

    def test_add_article_forms(self):
        s = 'With the art. and subst.: f. cossin noin 2a21, 22, cosin noin 2a21, n. cossalaasa 23a17.'
        prep = Preposition('', '', common_case='acc')
        add_article_forms(s, prep)
        self.assertEqual(len(prep.form_analyses), 2)
        self.assertEqual(prep.form_analyses[0].case, 'acc')
        self.assertEqual(prep.form_analyses[0].classifier, 'def. art.')
        self.assertEqual(prep.form_analyses[0].gender, 'f')
        self.assertEqual(prep.form_analyses[0].forms[0].form, 'cossin noin')
        self.assertEqual(str(prep.form_analyses[0].forms[0].loci[1]), str(Locus(2, 'a', 22)))
        self.assertEqual(prep.form_analyses[1].gender, 'n')

    def test_add_pron_form_analyses(self):
        s = 'With suffix. pron. 3sg. m. etir 28b3, 1pl. etronn 15a32, etrunn 31a11, \
with emph. pron. 1pl. etrunni 12b12, 2pl. etruib 24c22, 27b18, 21 (bis), 3pl. etarru 7d10, 27d19, ettarru 33b18.'
        prep = Preposition('', '', common_case='acc')
        add_pron_form_analyses(s, prep)
        self.assertEqual(len(prep.form_analyses), 5)
        self.assertEqual(prep.form_analyses[0].case, 'acc')
        self.assertEqual(prep.form_analyses[0].classifier, 'suffix. pron.')
        self.assertEqual(prep.form_analyses[0].gender, 'm.')
        self.assertEqual(prep.form_analyses[1].person, '1')
        self.assertEqual(prep.form_analyses[1].number, 'pl')
        self.assertEqual(prep.form_analyses[2].classifier, 'emph. pron.')
        self.assertEqual(prep.form_analyses[2].person, '1')
        self.assertEqual(prep.form_analyses[2].number, 'pl')
        self.assertEqual(prep.form_analyses[3].person, '2')
        self.assertEqual(prep.form_analyses[3].number, 'pl')
        self.assertEqual(prep.form_analyses[4].person, '3')
        self.assertEqual(prep.form_analyses[4].number, 'pl')
        self.assertIsNone(prep.form_analyses[4].gender)

        s = 'With suffix. pron. 3sg. n. occo, occa, oca: occo 3c24, 4a26, 5a26, 6a14, 22, 6d3, \
7c4, 8d15, occa: occa 3c25, 8a11, 9d22, 11b4, 24a20, 26d8, 18, 29d6, oca: oca 33d7.'
        prep = Preposition('', '', common_case='acc')
        add_pron_form_analyses(s, prep)
        self.assertEqual(len(prep.form_analyses), 1)
        self.assertEqual(prep.form_analyses[0].case, 'acc')
        self.assertEqual(prep.form_analyses[0].classifier, 'suffix. pron.')
        self.assertEqual(prep.form_analyses[0].person, '3')
        self.assertEqual(prep.form_analyses[0].number, 'sg')
        self.assertEqual(prep.form_analyses[0].gender, 'n.')
        self.assertEqual(len(prep.form_analyses[0].forms[0].loci), 8)

        s = 'With suffix. pron.s: 1sg. with emph. pron. 1sg. cuccumsa 7c7, 2sg. cucut 32a17, \
25, 3sg. m. cuci 15c23, with emph. pron. 3sg. cucisom 9d14, f. cuicce 9d5, n. cucci \
24c17, 25a27, cuci 19b8, 1pl. cucunn 21a3, 2pl. cuccuib 7b1, 9a23, cucuib 14c40, \
32a27, with emph. pron. 2pl. cucuibsi 1a8, 14a8, 14, 17a11, 24b14, 26c2, cucuib si \
24c17, 3pl. cuccu 5a3, 27c24, with emph. pron. 3pl. cuccusom 14d30.'
        prep = Preposition('', '', common_case='acc')
        #add_pron_form_analyses(s, prep)
