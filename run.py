import codecs

from extractor.extractor import create_pos
from extractor.verbextractor import create_verb
from extractor.models import Noun, Adjective

if __name__ == "__main__":
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
    """
    with codecs.open('data/verbs.txt', 'rb') as in_file:
        for line in in_file:
            line = line.strip()
            #pos = create_verb(line)

            verb = None
            for n, l in enumerate(line.split('; ')):
                if n == 0:
                    verb = create_verb(l)
                else:
                    verb = create_verb(l, verb)
            #print verb
