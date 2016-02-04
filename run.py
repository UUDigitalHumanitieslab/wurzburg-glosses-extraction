import codecs
import glob
import re

from extractor.extractor import create_pos
from extractor.verbextractor import create_verb, find_stem_class
from extractor.prepextractor import create_preposition
from extractor.advextractor import create_adverb
from extractor.models import Noun, Adjective

NEW_GLOSS = re.compile(r"""
^<b>                # matches <b> at the start of a line
[^(IV|V?I{0,3})]    # does not match a Roman numeral
""", re.X)

if __name__ == "__main__":
    for f in glob.glob('data/wurzburg/part2_lexicon_a.txt'):
        with codecs.open(f) as in_file:
            glosses = []
            current_gloss = ''
            prev_line_empty = False
            for line in in_file:
                line = line.strip().replace('&amp;', '&')  # truncate and fix XML escapes
                if line:
                    if NEW_GLOSS.match(line):
                        # We reached the start of a new gloss; append the previous to the list
                        glosses.append(current_gloss)
                        current_gloss = ''
                    current_gloss += line + ' '
            glosses.append(current_gloss)

            for gloss in glosses:
                stem, _, _ = find_stem_class(gloss)
                if stem and not gloss.startswith('<b>-') and not gloss.startswith('<b>pridchaid'):
                    print gloss
                    verb = create_verb(gloss)
                    print verb


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
