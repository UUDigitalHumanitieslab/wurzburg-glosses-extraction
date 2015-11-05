class PartOfSpeech(object):
    def __init__(self, headword, stem, additional, definition):
        self.headword = headword
        self.stem = stem
        self.additional = additional
        self.definition = definition
        self.form_analyses = []

    def add_form_analyses(self, form_analyses):
        self.form_analyses.append(form_analyses)


class Noun(PartOfSpeech):
    """
    In addition to a PartOfSpeech, a Noun has a gender.
    """
    def __init__(self, headword, gender, stem, additional, definition):
        super(Noun, self).__init__(headword, stem, additional, definition)
        self.gender = gender

    def __str__(self):
        s = 'Noun: {}, gender: {}, stem: {}'.format(self.headword, self.gender, self.stem)
        for form_analysis in self.form_analyses:
            s += '\n\t{}'.format(form_analysis)
        return s


class Adjective(PartOfSpeech):
    pass


class Verb(PartOfSpeech):
    def __init__(self, headword, definition, voice, stem, person, relative, pronominal):
        super(Noun, self).__init__(headword, stem, '', definition)
        self.voice = voice
        self.person = person
        self.relative = relative
        self.pronominal = pronominal


class FormAnalysis(object):
    def __init__(self, case, gender):
        self.case = case
        self.gender = gender
        self.forms = []

    def set_forms(self, forms):
        self.forms = forms

    def __str__(self):
        s = 'FormAnalysis: case: {}, gender: {}'.format(self.case, self.gender)
        for form in self.forms:
            s += '\n\t\t{}'.format(form)
        return s


class Form(object):
    def __init__(self, form):
        self.form = form
        self.loci = []

    def set_loci(self, loci):
        self.loci = loci

    def __str__(self):
        s = 'Form: {}'.format(self.form.encode('utf-8'))
        for loci in self.loci:
            s += '\n\t\t\t{}'.format(loci)
        return s


class Locus(object):
    OCCURRENCES_MAP = {'': 1, 'bis': 2, 'ter': 3, 'quatter': 4}

    def __init__(self, page, column, number, subdivision, nr_occurrences):
        self.page = page
        self.column = column
        self.number = number
        self.subdivision = subdivision
        self.nr_occurrences = self.occurrences_to_int(nr_occurrences)

    def occurrences_to_int(self, nr_occurrences):
        if nr_occurrences in self.OCCURRENCES_MAP:
            return self.OCCURRENCES_MAP[nr_occurrences]
        else:
            raise ValueError('Unknown number of occurrences: {}'.format(nr_occurrences))

    def __str__(self):
        return 'Locus: page: {}, column: {}, number: {}, subdivision: {}, nr_occurrences: {}'.format(self.page, self.column, self.number, self.subdivision, self.nr_occurrences)
