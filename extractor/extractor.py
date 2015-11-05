import codecs
import re

from models import Noun, FormAnalysis, Form, Locus

NOUN = re.compile(r'(.*)\s([nmf])\.\s(.*?)[\.,]')
FORM_ANALYSIS = re.compile(r'([NVAGD](?:sg|pl|du)).\s')
FORM = re.compile(r'([^\W\d_]+)\s', re.U)
LOCI = re.compile(r'(\d+)([a-d]?)(\d*)([a-d]?)(?:\s\((\w+)\))?')


def create_noun(s):
    """
    Creates a Noun from a string s. A Noun consists of one or more FormAnalyses.
    """
    current_noun = None
    current_form = None
    for n, match in enumerate(FORM_ANALYSIS.split(s)):
        if n == 0:
            current_noun = extract_noun(match)
        elif n % 2 == 1:
            current_form = FormAnalysis(match)
            current_noun.add_form_analyses(current_form)
        else:
            current_form.set_forms(extract_forms(match))

    return current_noun


def extract_noun(s):
    """
    Extracts a single noun from a string s.
    """
    match = NOUN.match(s)
    title = match.group(1)
    gender = match.group(2)
    stem = match.group(3)
    return Noun(title, gender, stem, '', '')


def extract_forms(s):
    """
    Extracts all forms from a string s. A form consists of a definition and one or more Loci.
    """
    forms = []
    current_form = None
    for n, match in enumerate(FORM.split(s.decode('utf-8'))):
        if n == 0:
            pass  # first match is empty
        elif n % 2 == 1:
            current_form = Form(match)
        else:
            current_form.set_loci(extract_loci(match))
            forms.append(current_form)

    return forms


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
        loci.append(locus)

        prev_locus = locus
        #print n, match, locus

    return loci

if __name__ == "__main__":
    #with codecs.open('../data/test1.txt', 'rb') as in_file:
    #    for line in in_file:
    #        line = line.strip()
    #        extract_loci(line)
    with codecs.open('../data/dan.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            print create_noun(line)