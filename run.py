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
            verb = create_verb(line)
            print verb
