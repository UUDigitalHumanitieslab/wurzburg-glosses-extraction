from abc import ABCMeta, abstractmethod


class PartOfSpeech(object):
    """
    A PartOfSpeech is an abstract base class, so must be initiated.
    """
    __metaclass__ = ABCMeta

    def __init__(self, headword, definition, **kwargs):
        self.headword = headword
        self.definition = definition.strip() if definition else None
        self.additional = kwargs.get('additional', None)
        self.form_analyses = []

    def add_form_analysis(self, form_analysis):
        """
        Adds a FormAnalysis.
        """
        self.form_analyses.append(form_analysis)

    def to_csv(self):
        """
        Returns the PartOfSpeech as a list of Loci for output to .csv-format
        """
        result = []
        for fa in self.form_analyses:
            for f in fa.forms:
                for l in f.loci:
                    r = [self.headword, self.definition, self.additional]
                    r.extend(fa.get_grammatical_info())
                    r.extend([f.form, l.short_str(), str(l.nr_occurrences), l.alternative])
                    result.append(r)
        return result

    def get_csv_header(self):
        """
        Returns the header for the .csv-output
        """
        result = ['headword', 'definition', 'additional']
        result.extend(self.get_csv_form_analysis_header())
        result.extend(['form', 'locus', 'locus_amount', 'alternative'])
        return result

    @staticmethod
    @abstractmethod
    def get_csv_form_analysis_header():
        """
        Allows every PartOfSpeech to have a custom header on the FormAnalysis level.
        """
        return []

    def __str__(self):
        s = '{}: {}, add_info: {}, def: {}'.format(self.__class__.__name__, self.headword, self.additional, self.definition)
        for form_analysis in self.form_analyses:
            s += '\n\t{}'.format(form_analysis)
        return s


class Noun(PartOfSpeech):
    """
    In addition to a PartOfSpeech, a Noun has a common stem and gender for all FormAnalyses.
    """
    def __init__(self, headword, definition, **kwargs):
        self.common_stem = kwargs.get('common_stem', None)
        self.common_gender = kwargs.get('common_gender', None)
        super(Noun, self).__init__(headword, definition, **kwargs)

    def add_form_analysis(self, form_analysis):
        """
        Sets the common stem and gender before adding the FormAnalysis.
        """
        if self.common_stem:
            form_analysis.stem = self.common_stem
        if self.common_gender:
            form_analysis.gender = self.common_gender
        super(Noun, self).add_form_analysis(form_analysis)

    @staticmethod
    def get_csv_form_analysis_header():
        return ['gender', 'stem', 'case']


class Adjective(PartOfSpeech):
    """
    In addition to a PartOfSpeech, an Adjective has a common stem for all FormAnalyses.
    """
    def __init__(self, headword, definition, **kwargs):
        self.common_stem = kwargs.get('common_stem', None)
        super(Adjective, self).__init__(headword, definition, **kwargs)

    def add_form_analysis(self, form_analysis):
        """
        Sets the common stem before adding the FormAnalysis.
        """
        if self.common_stem:
            form_analysis.stem = self.common_stem
        super(Adjective, self).add_form_analysis(form_analysis)

    @staticmethod
    def get_csv_form_analysis_header():
        return ['stem', 'case']


class Adverb(PartOfSpeech):
    """
    An Adverb does not contain any additional information, just a headword and a definition.
    """
    @staticmethod
    def get_csv_form_analysis_header():
        return []


class Preposition(PartOfSpeech):
    """
    In addition to a PartOfSpeech, a Preposition has a common case for all FormAnalyses.
    """
    def __init__(self, headword, definition, **kwargs):
        self.common_case = kwargs.get('common_case', None)
        super(Preposition, self).__init__(headword, definition, **kwargs)

    def add_form_analysis(self, form_analysis):
        """
        Sets the common case before adding the FormAnalysis.
        """
        if self.common_case:
            form_analysis.case = self.common_case
        super(Preposition, self).add_form_analysis(form_analysis)

    @staticmethod
    def get_csv_form_analysis_header():
        return []


class Verb(PartOfSpeech):
    """
    A Verb has some extra attributes on FormAnalysis.
    """
    @staticmethod
    def get_csv_form_analysis_header():
        return ['voice', 'stem class', 'person', 'relative', 'pronominal object', 'empathic elements']


class DefiniteArticle(PartOfSpeech):
    """
    A DefiniteArticle does not contain any additional information, just a headword and a definition.
    """
    @staticmethod
    def get_csv_form_analysis_header():
        return ['case', 'person']


class FormAnalysis(object):
    def __init__(self, part_of_speech, **kwargs):
        """
        Specifies per PartOfSpeech which fields should be declared
        """
        if isinstance(part_of_speech, Noun):
            self.case = kwargs.get('case', None)
            self.gender = kwargs.get('gender', None)

        if isinstance(part_of_speech, Adjective):
            self.case = kwargs.get('case', None)

        if isinstance(part_of_speech, Verb):
            self.is_active = kwargs.get('is_active', None)
            self.stem = kwargs.get('stem', None)
            self.person = kwargs.get('person', None)
            self.relative = kwargs.get('relative', None)
            self.pronominal_object = kwargs.get('pronominal_object', None)
            self.empathic_elements = kwargs.get('empathic_elements', None)

        if isinstance(part_of_speech, Preposition):
            self.case = kwargs.get('case', None)
            self.classifier = kwargs.get('classifier', None)
            self.person = kwargs.get('person', None)
            self.number = kwargs.get('number', None)
            self.gender = kwargs.get('gender', None)
            self.empathic_elements = kwargs.get('empathic_elements', None)

        if isinstance(part_of_speech, DefiniteArticle):
            self.case = kwargs.get('case', None)
            self.person = kwargs.get('person', None)

        self.parent = part_of_speech
        self.forms = []

    def set_forms(self, forms):
        self.forms = forms

    def append_form(self, form):
        self.forms.append(form)

    def get_last_form(self):
        return self.forms[-1]

    def get_grammatical_info(self):
        if isinstance(self.parent, Noun):
            return [self.gender, self.stem if hasattr(self, 'stem') else None, self.case]
        elif isinstance(self.parent, Adjective):
            return [self.stem if hasattr(self, 'stem') else None, self.case]
        elif isinstance(self.parent, Verb):
            return ['active' if self.is_active else 'passive',
                    self.stem, self.person, self.relative,
                    self.pronominal_object, self.empathic_elements]
        elif isinstance(self.parent, Preposition):
            return [self.case, self.classifier, self.person,
                    self.number, self.gender, self.empathic_elements]
        elif isinstance(self.parent, DefiniteArticle):
            return [self.case, self.person]
        else:
            return []

    def __str__(self):
        if isinstance(self.parent, Noun):
            f = 'FormAnalysis: gender: {g}, stem: {s}, case: {c}'
            s = f.format(s=self.stem, c=self.case, g=self.gender)
        if isinstance(self.parent, Adjective):
            f = 'FormAnalysis: stem: {s}, case: {c}'
            s = f.format(s=self.stem, c=self.case)
        if isinstance(self.parent, Verb):
            f = 'FormAnalysis: stem: {s}, is_active: {v}, person: {p}, relative: {r}, po: {po}, ee: {ee}'
            s = f.format(s=self.stem, v=self.is_active, p=self.person, r=self.relative,
                         po=self.pronominal_object, ee=self.empathic_elements)
        if isinstance(self.parent, Adverb):
            s = 'FormAnalysis'
        if isinstance(self.parent, Preposition):
            f = 'FormAnalysis: case: {c}, classifier: {cl}, person: {p}, number: {n}, gender: {g}, ee: {ee}'
            s = f.format(c=self.case, cl=self.classifier, p=self.person,
                         n=self.number, g=self.gender, ee=self.empathic_elements)

        for form in self.forms:
            s += '\n\t\t{}'.format(form)
        return s


class Form(object):
    def __init__(self, form):
        self.form = form
        self.loci = []

    def set_loci(self, loci):
        self.loci = loci

    def append_loci(self, loci):
        self.loci.extend(loci)

    def get_last_locus(self):
        if not self.loci:
            return None
        return self.loci[-1]

    def __str__(self):
        s = 'Form: {}'.format(self.form)
        for loci in self.loci:
            s += '\n\t\t\t{}'.format(loci)
        return s


class Locus(object):
    OCCURRENCES_MAP = {'': 1, 'bis': 2, 'ter': 3, 'quater': 4, 'quatter': 4, 'quinquiens': 5}

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

    def short_str(self):
        return '{}{}{}{}'.format(self.page, self.column, self.number, self.subdivision)

    def __str__(self):
        return 'Locus: {}{}{}{} ({}), a: {}'.format(self.page, self.column, self.number, self.subdivision, self.nr_occurrences, self.alternative)
