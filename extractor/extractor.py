from .models import FormAnalysis, Form, Locus
from .regexes import remove_html_tags, POS_ANALYSIS, POS_DEFINITION, FORM_ANALYSES, FORMS, LOCI


def create_pos(s, cls):
    """
    Creates a PartOfSpeech (of given class cls) from a string s.
    A PartOfSpeech consists of one or more FormAnalyses.
    """
    pos = None
    current_form_analysis = None
    splits = FORM_ANALYSES.split(s)
    for n, match in enumerate(splits):
        if n == 0:
            pos = extract_pos(match, cls)
            pass
        elif n % 3 == 1:
            current_form_analysis = FormAnalysis(pos, case=splits[n], gender=splits[n + 1])
            pos.add_form_analysis(current_form_analysis)
        elif n % 3 == 0:
            current_form_analysis.set_forms(extract_forms(match))

    return pos


def extract_pos(s, cls):
    """
    Extracts a PartOfSpeech definition from a string s.
    """
    # Capture the headword, gender and stem
    match = POS_ANALYSIS.match(s)
    headword = match.group(1).strip()
    gender = match.group(2)  # for Nouns
    stem = match.group(3)  # for both Adjectives and Nouns
    add_def = match.group(4).strip()
    additional = None
    definition = None

    if stem:
        stem = stem.strip()

    # If a start tag was stripped, place it back
    if add_def.startswith('i>'):
        add_def = '<' + add_def

    # Split the additional information from the definition
    match = POS_DEFINITION.match(add_def)
    if match:
        additional = match.group(1)
        definition = remove_html_tags(match.group(2).strip())

    return cls(headword, definition, additional=additional, common_stem=stem, common_gender=gender)


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
            loci = extract_loci(match)
            current_form.set_loci(loci)
            forms.append(current_form)

            if not loci:
                print 'No loci for form "{}", is this correct?'.format(current_form.form)

    return forms


def extract_loci(s, prev_locus=None):
    """
    Extracts all Loci from a string s.
    A locus can appear in several forms, e.g.: 1a12, 11b6a, 12c13, 15d, 16.
    In the last two cases, the Locus signifies only the number and subdivision,
    the page and column need to be fetched from the preceding Locus.
    """
    loci = []
    for n, match in enumerate(LOCI.findall(s)):
        page = match[0]
        column = match[1]
        number = match[2]
        subdivision = match[3]
        nr_occurrences = match[4]
        alternative = match[5]

        if not number:
            if prev_locus:
                number = page
                subdivision = column
                page = prev_locus.page
                column = prev_locus.column
            else:
                raise ValueError('Incorrect loci description: ' + s)

        locus = Locus(page, column, number, subdivision, nr_occurrences, alternative)
        loci.append(locus)

        prev_locus = locus

    return loci
