from .models import Noun, Adjective, FormAnalysis, Form, Locus
from .regexes import remove_html_tags, SPLIT_EXAMPLES, POS_ANALYSIS, POS_DEFINITION, FORM_ANALYSES, LOCUS


def create_pos(s):
    """
    Creates a PartOfSpeech (of given class cls) from a string s.
    A PartOfSpeech consists of one or more FormAnalyses.
    """
    match = SPLIT_EXAMPLES.match(s)
    if match:
        s = match.group(1)

    pos = None
    current_form_analysis = None
    splits = FORM_ANALYSES.split(s)
    for n, match in enumerate(splits):
        if n == 0:
            pos = extract_pos(match)
            pass
        elif n % 3 == 1:
            current_form_analysis = FormAnalysis(pos, case=splits[n], gender=splits[n + 1])
            pos.add_form_analysis(current_form_analysis)
        elif n % 3 == 0:
            current_form_analysis.set_forms(extract_forms(match))

    return pos


def extract_pos(s):
    """
    Extracts a PartOfSpeech definition from a string s.
    """
    # Capture the headword, gender and stem
    match = POS_ANALYSIS.match(s)
    if not match:
        raise ValueError('This is not a Noun/Adjective')
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
        definition = remove_html_tags(match.group(2))

    cls = Noun if gender else Adjective
    return cls(headword, definition, additional=additional, common_stem=stem, common_gender=gender)


def extract_forms(s):
    """
    Extracts all Forms from a string s. A Form consists of a definition and one or more Loci.
    """
    forms = []
    while s:
        # Don't include references to other glosses
        if s.startswith('s.') or s.startswith('cf.'):
            break

        match = LOCUS.search(s)
        if match:
            f = s[:match.start(0)].strip()
            # Don't include examples if there's already forms listed
            if forms and f.startswith('.i.'):
                break
            else:
                form = Form(f)
                loci, s = extract_loci(s[match.start(0):])
                form.set_loci(loci)
                forms.append(form)
        else:
            print 'No loci for form "{}", is this correct?'.format(s)
            break

    return forms


def extract_loci(s, prev_locus=None):
    """
    Extracts all Loci from a string s.
    A locus can appear in several forms, e.g.: 1a12, 11b6a, 12c13, 15d, 16.
    In the last two cases, the Locus signifies only the number and subdivision,
    the page and column need to be fetched from the preceding Locus.
    """
    loci = []
    post_locus = ''
    for match in LOCUS.finditer(s):
        if post_locus and match.start(0) != post_locus:
            break

        page = match.group(1)
        column = match.group(2)
        number = match.group(3)
        subdivision = match.group(4)
        nr_occurrences = match.group(5) or ''
        alternative = match.group(6) or ''

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
        post_locus = match.end(0)

    return loci, s[post_locus:]
