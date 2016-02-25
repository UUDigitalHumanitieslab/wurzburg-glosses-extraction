import codecs
import glob
import re
import os

from extractor.extractor import create_pos
from extractor.verbextractor import create_verb, find_stem_class
from extractor.regexes import FORM_ANALYSES
from extractor.prepextractor import create_preposition
from extractor.advextractor import create_adverb
from extractor.models import Noun, Adjective
import csv

NEW_GLOSS = re.compile(r"""
^<b>                # matches <b> at the start of a line
[^([A-Z|IV|V?I{0,3})]    # does not match a Roman numeral
""", re.X)


def to_csv(posses, filename):
    if posses:
        with open(filename, 'wb') as out_csv:
            out_csv.write(u'\uFEFF'.encode('utf-8'))  # the UTF-8 BOM to hint Excel we are using that...
            csv_writer = csv.writer(out_csv, delimiter=';')

            csv_writer.writerow(posses[0].get_csv_header())
            for pos in posses:
                csv_writer.writerows(pos.to_csv())


def get_csv_name(filename, kind):
    return os.path.dirname(filename) + os.path.sep + kind + '_' + os.path.basename(filename)[-5:].replace('txt', 'csv')


def extract_glosses(filename):
    glosses = []
    current_gloss = ''
    with codecs.open(filename) as in_file:
        for line in in_file:
            line = line.strip().replace('&amp;', '&')  # truncate and fix XML escapes
            if line:
                if NEW_GLOSS.match(line):
                    # We reached the start of a new gloss; append the previous to the list
                    glosses.append(current_gloss)
                    current_gloss = ''
                current_gloss += line + ' '
    glosses.append(current_gloss)

    return glosses

if __name__ == "__main__":
    for f in glob.glob('data/wurzburg/part2_lexicon_[a-d].txt'):
        nouns = []
        adjectives = []
        verbs = []
        adverbs = []
        prepositions = []

        for gloss in extract_glosses(f):
            # Check for prepositions
            if 'Prep.' in gloss:
                """
                print gloss
                try:
                    prepositions.append(create_preposition(gloss))
                except ValueError as e:
                    print e
                except IndexError as e:
                    print e
                """
                continue

            if 'Def. art.' in gloss:
                continue

            if 'Adj.' in gloss:
                continue

            if 'Infix. pron.' in gloss:
                continue

            if 'Substantive Verb.' in gloss:
                continue

            # Check for predicates
            if 'Predic.' in gloss:
                continue

            # Check for deponentia
            if '(depon.)' in gloss:
                continue

            if FORM_ANALYSES.search(gloss):
                print gloss
                try:
                    pos = create_pos(gloss)
                    if isinstance(pos, Noun):
                        nouns.append(pos)
                    elif isinstance(pos, Adjective):
                        adjectives.append(pos)
                except ValueError as e:
                    print e

            # Check for verbs
            stem, _, _ = find_stem_class(gloss)
            if stem:
                print gloss
                try:
                    verb = create_verb(gloss)
                    verbs.append(verb)
                except ValueError as e:
                    print e
                continue

            # print gloss

        to_csv(nouns, get_csv_name(f, 'nouns'))
        to_csv(adjectives, get_csv_name(f, 'adjectives'))
        to_csv(verbs, get_csv_name(f, 'verbs'))
        to_csv(adverbs, get_csv_name(f, 'adverbs'))
        to_csv(prepositions, get_csv_name(f, 'prepositions'))


    """
    with codecs.open('data/nouns.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            pos = create_pos(line, Noun)
            print pos
    with codecs.open('data/adjectives.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            pos = create_pos(line, Adjective)
            print pos
    with codecs.open('data/verbs.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            line = line.replace('&amp;', '&')  # fix XML escapes
            verb = create_verb(line)
            print verb
    with codecs.open('data/eter.txt', 'rb') as in_file:
        s = ''
        for line in in_file:
            if line.startswith('I.'):  # stop at meanings
                break
            line = line.strip()
            line = line.replace('&amp;', '&')  # fix XML escapes
            if not line.isdigit():  # skip page numbers
                s += line + ' '
            is_page = False

        print s
        prep = create_preposition(s)
        print prep
    with codecs.open('data/adverbs.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            line = line.replace('&amp;', '&')  # fix XML escapes
            adverb = create_adverb(line)
            print adverb
    """
