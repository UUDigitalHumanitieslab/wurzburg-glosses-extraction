class PartOfSpeech(object):
    def __init__(self, headword, additional, definition, **kwargs):
        self.headword = headword
        self.additional = additional.strip() if additional else None
        self.definition = definition.strip() if definition else None
        self.form_analyses = []
        self.common_stem = kwargs.get('common_stem', None)
        self.common_gender = kwargs.get('common_gender', None)

    def add_form_analysis(self, form_analysis):
        """
        Adds a FormAnalysis, sets the common stem or gender.
        """
        if self.common_stem:
            form_analysis.stem = self.common_stem
        if self.common_gender:
            form_analysis.gender = self.common_gender
        self.form_analyses.append(form_analysis)

    def __str__(self):
        s = 'POS: {}, add_info: {}, def: {}'.format(self.headword, self.additional, self.definition)
        for form_analysis in self.form_analyses:
            s += '\n\t{}'.format(form_analysis)
        return s


class Noun(PartOfSpeech):
    """
    In addition to a PartOfSpeech, a Noun has a common stem and gender for all FormAnalyses.
    """


class Adjective(PartOfSpeech):
    """
    In addition to a PartOfSpeech, an Adjective has a common stem for all FormAnalyses.
    """


class Verb(PartOfSpeech):
    """
    A Verb does not contain any additional information, just a headword and a definition.
    """
    def __init__(self, headword, definition):
        super(Verb, self).__init__(headword, '', definition)


class FormAnalysis(object):
    def __init__(self, stem, case, gender, **kwargs):
        self.stem = stem
        self.case = case
        self.gender = gender

        self.is_active = kwargs.get('is_active', None)
        self.person = kwargs.get('person', None)
        self.relative = kwargs.get('relative', None)
        self.pronominal_object = kwargs.get('pronominal_object', None)
        self.empathic_elements = kwargs.get('empathic_elements', None)

        self.forms = []

    def set_forms(self, forms):
        self.forms = forms

    def append_form(self, form):
        self.forms.append(form)

    def get_last_form(self):
        return self.forms[-1]

    def __str__(self):
        f = 'FormAnalysis: stem: {}, case: {}, gender: {}, \
is_active: {}, person: {}, relative: {}, po: {}, ee: {}'
        s = f.format(self.stem, self.case, self.gender, self.is_active,
                     self.person, self.relative, self.pronominal_object, 
                     self.empathic_elements)
        for form in self.forms:
            s += '\n\t\t{}'.format(form)
        return s


class Form(object):
    def __init__(self, form):
        self.form = form
        self.loci = []

    def set_loci(self, loci):
        self.loci = loci

    def append_locus(self, locus):
        self.loci.append(locus)

    def get_last_locus(self):
        if not self.loci:
            return None
        return self.loci[-1]

    def __str__(self):
        s = 'Form: {}'.format(self.form.encode('utf-8'))
        for loci in self.loci:
            s += '\n\t\t\t{}'.format(loci)
        return s


class Locus(object):
    OCCURRENCES_MAP = {'': 1, 'bis': 2, 'ter': 3, 'quatter': 4}

    def __init__(self, page, column, number, subdivision='', nr_occurrences='', alternative=''):
        self.page = page
        self.column = column
        self.number = number
        self.subdivision = subdivision
        self.nr_occurrences = self.occurrences_to_int(nr_occurrences)
        self.alternative = alternative

    def occurrences_to_int(self, nr_occurrences):
        if nr_occurrences in self.OCCURRENCES_MAP:
            return self.OCCURRENCES_MAP[nr_occurrences]
        else:
            raise ValueError('Unknown number of occurrences: {}'.format(nr_occurrences))

    def __str__(self):
        return 'Locus: {}{}{}{} ({}), a: {}'.format(self.page, self.column, self.number, self.subdivision, self.nr_occurrences, self.alternative)
