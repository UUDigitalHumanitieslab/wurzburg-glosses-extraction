import unittest

from extractor.extractor import extract_loci
from extractor.models import Locus


class TestExtractor(unittest.TestCase):

    def test_extract_loci(self):
        s = ' 14d3, 7a, 11'
        loci = extract_loci(s)
        self.assertEqual(str(loci[0]), str(Locus(14, 'd', 3, '', '')))
        self.assertEqual(str(loci[1]), str(Locus(14, 'd', 7, 'a', '')))
        self.assertEqual(str(loci[2]), str(Locus(14, 'd', 11, '', '')))

        s = ' 11b6a, 7 (quatter), 8b (ter)'
        loci = extract_loci(s)
        self.assertEqual(str(loci[0]), str(Locus(11, 'b', 6, 'a', '')))
        self.assertEqual(str(loci[1]), str(Locus(11, 'b', 7, '', 'quatter')))
        self.assertEqual(str(loci[2]), str(Locus(11, 'b', 8, 'b', 'ter')))
        self.assertEqual(loci[2].nr_occurrences, 3)

        with self.assertRaises(ValueError):
            s = ' 11b6a, 7 (quatter), 8b (ters)'
            extract_loci(s)
