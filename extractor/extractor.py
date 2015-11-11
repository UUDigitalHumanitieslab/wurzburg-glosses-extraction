from .models import FormAnalysis, Form, Locus
from .regexes import POS_DEFINITION, POS_EXTRA_INFO, FORM_ANALYSES, FORMS, LOCI


def create_pos(s, cls):
    """
    Creates a PartOfSpeech (of given class cls) from a string s.
    A PartOfSpeech consists of one or more FormAnalyses.
    """
    current_adj = None
    current_form = None
    splits = FORM_ANALYSES.split(s)
    for n, match in enumerate(splits):
        if n == 0:
            current_adj = extract_pos(match, cls)
            pass
        elif n % 3 == 1:
            current_form = FormAnalysis(splits[n], splits[n + 1])
            current_adj.add_form_analyses(current_form)
        elif n % 3 == 0:
            current_form.set_forms(extract_forms(match))

    return current_adj


def extract_pos(s, cls):
    """
    Extracts a noun definition from a string s.
    """
    match = POS_DEFINITION.match(s)
    headword = match.group(1)
    gender = match.group(2)
    stem = match.group(3)
    additional = None
    definition = None

    unmatched = s[match.end():].strip()
    if unmatched:
        match = POS_EXTRA_INFO.match(unmatched)
        if POS_EXTRA_INFO.match(unmatched):
            additional = match.group(1)
            definition = match.group(2)

    return cls(headword, stem, additional, definition, gender=gender)


def extract_forms(s):
    """
    Extracts all Forms from a string s. A Form consists of a definition and one or more Loci.
    """
    forms = []
    current_form = None
    for n, match in enumerate(FORMS.split(s.decode('utf-8'))):
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
    Extracts all Loci from a string s.
    A locus can appear in several forms, e.g.: 1a12, 11b6a, 12c13, 15d, 16.
    In the last two cases, the Locus signifies only the number and subdivision,
    the page and column need to be fetched from the preceding Locus.
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

    return loci
