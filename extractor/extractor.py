import codecs
import re

from models import Locus

LOCI = re.compile(r'\s(\d+)([a-d]?)(\d*)([a-d]?)(?:\s\((\w+)\))?')


def extract_loci(s):
    """
    Extracts all loci from a string s.
    """
    loci = []
    prev_locus = None
    for n, match in enumerate(LOCI.findall(s)):
        page = match[0]
        column = match[1]
        number = match[2]
        subdivision = match[3]
        nr_occurrences = match[4]

        if not number:
            number = page
            subdivision = column
            page = prev_locus.page
            column = prev_locus.column

        locus = Locus(page, column, number, subdivision, nr_occurrences)

        prev_locus = locus
        print n, match, locus

    return loci

if __name__ == "__main__":
    with codecs.open('../data/test1.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            extract_loci(line)