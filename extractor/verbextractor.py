import copy
import re

from .extractor import extract_forms, extract_loci
from .models import Verb, FormAnalysis
from .regexes import remove_html_tags, SPLIT_EXAMPLES, VERB_HEADWORD, VERB_ADDITIONAL_STEM, VERB_PERSON, \
    VERB_CONJUNCTION, VERB_RELATIVE, VERB_VOICE, VERB_PRONOMINAL_OBJECT, VERB_EMPHATIC_ELEMENTS, LOCUS, match_regex


VERB_STEM_CLASSES = ['Pres. Ind.', 'Imperf.', 'Imperf. Ind.', 'Fut.', 'Sec. Fut.', 'Pres. Subj.',
                     'Past Subj.', 'Pret.', 'Perf.', 'Pret. & Perf.', 'Perfect. Pres. Subj.',
                     'Perfect. Past Subj.', 'Imperat.']


def create_verb(s):
    """
    Creates a Verb from a string s.
    First splits the active and passive voices, then splits every form.
    TODO: deal with double forms ("or")
    TODO: deal with "with cia and infix. pron. 3sg. n." (maybe allow for \w+\sand between "with" and "infix"?)
    """
    current_verb = None
    match = SPLIT_EXAMPLES.match(s)
    if match:
        s = match.group(1)

    current_verb, post_verb = find_verb(s)
    for i, fa in enumerate(split_by(post_verb, ';')):   # Active and passive FormAnalyses are split by a semi-colon
        current_form_analysis = None
        for j, f in enumerate(split_by(fa, ',')):       # Forms are separated by a comma
            current_form_analysis, is_new = create_form_analysis(f, current_verb, current_form_analysis)
            if is_new:
                current_verb.add_form_analysis(current_form_analysis)
    return current_verb


def find_verb(s):
    stem, pre_stem, post_stem = find_stem_class(s)

    if stem:
        # If we find a stem class, check whether there is a passive annotation
        verb_string, _ = match_voice(pre_stem)

        # Extract headword and definition
        definition = None
        match = VERB_HEADWORD.match(verb_string)
        if match:
            headword = remove_html_tags(match.group(1))
            if match.group(2):
                definition = remove_html_tags(match.group(2))
        else:
            headword = verb_string

        # Create the verb
        verb = Verb(headword, definition)
        post_verb = s[len(verb_string):].lstrip()
        return verb, post_verb
    else:
        raise ValueError('No stem class found, this is not a verb: ' + s)


def create_form_analysis(s, current_verb, current_form_analysis=None):
    """
    Creates or appends a FormAnalysis from a string s, recursively.
    """
    is_new = False

    stem, pre_stem, post_stem = find_stem_class(s)
    if stem:
        # If we're starting off, check whether there is a passive annotation
        if not current_form_analysis:
            _, is_active = match_voice(pre_stem)
        # Otherwise, retrieve the voice from the current FormAnalysis
        else:
            is_active = current_form_analysis.is_active

        # Start a new FormAnalysis when we find a stem class
        current_form_analysis = FormAnalysis(current_verb, is_active=is_active, stem=stem)
        is_new = True
    elif not current_form_analysis:
        raise ValueError('No stem class found in: ' + s)

    person, post_person = match_regex(post_stem, VERB_PERSON)
    if person:
        # Create a new FormAnalysis if this is not already a fresh instance.
        if not is_new:
            current_form_analysis = copy.deepcopy(current_form_analysis)
            current_form_analysis.set_forms([])
            current_form_analysis.relative = None
            current_form_analysis.pronominal_object = None
            is_new = True
        current_form_analysis.person = person

    # Match conjunction elements, but disregard
    conjunction, post_conjunction = match_regex(post_person, VERB_CONJUNCTION)

    relative, post_relative = match_regex(post_conjunction, VERB_RELATIVE)
    if relative:
        # Create a new FormAnalysis if this is not already a fresh instance.
        if not is_new:
            current_form_analysis = copy.deepcopy(current_form_analysis)
            current_form_analysis.set_forms([])
            current_form_analysis.pronominal_object = None
            is_new = True
        current_form_analysis.relative = relative

    pronominal_object, post_po = match_regex(post_relative, VERB_PRONOMINAL_OBJECT)
    if pronominal_object:
        # Create a new FormAnalysis if this is not already a fresh instance.
        if not is_new:
            current_form_analysis = copy.deepcopy(current_form_analysis)
            current_form_analysis.set_forms([])
            # TODO: relative should not be emptied when po is preceded by 'and'.
            current_form_analysis.relative = None
            is_new = True
        current_form_analysis.pronominal_object = pronominal_object

    empathic_elements, post_ee = match_regex(post_po, VERB_EMPHATIC_ELEMENTS)
    if empathic_elements:
        # Create a new FormAnalysis if this is not already a fresh instance.
        if not is_new:
            current_form_analysis = copy.deepcopy(current_form_analysis)
            current_form_analysis.set_forms([])
            is_new = True
        current_form_analysis.empathic_elements = empathic_elements

    if LOCUS.match(post_ee):
        last_form = current_form_analysis.get_last_form()
        prev_locus = last_form.get_last_locus()
        try:
            last_form.append_locus(extract_loci(post_ee, prev_locus)[0])
        except ValueError:
            print 'Error extracting loci of: {}'.format(post_ee)
    else:
        try:
            current_form_analysis.append_form(extract_forms(post_ee)[0])
        except ValueError, IndexError:
            print 'Error extracting forms of: {}'.format(post_ee)
    return current_form_analysis, is_new


def find_stem_class(s):
    """
    Finds the first (and longest) occurrence of a verb stem class in a string s.
    """
    stem = None
    min_index = len(s)
    max_length = 0
    for stem_class in VERB_STEM_CLASSES:
        found = s.find(stem_class)
        if found != -1 and found <= min_index and len(stem_class) > max_length:
            stem = stem_class
            min_index = found
            max_length = len(stem_class)

    # If we didn't find any stem class, return the complete string.
    if min_index == len(s):
        return None, None, s

    # Set the pre and post stem variables
    pre_stem = s[:min_index].rstrip()
    post_stem = s[min_index + len(stem):].lstrip()

    # Check whether there is additional information on the stem in the post_stem.
    match = VERB_ADDITIONAL_STEM.match(post_stem)
    if match:
        stem += ' ' + match.group(1)
        post_stem = post_stem[match.end(1):].lstrip()

    return stem, pre_stem, post_stem


def match_voice(s):
    """
    Matches the voice of the string s and splits the headword off the front.
    """
    match = VERB_VOICE.match(s)
    if match:
        headword = match.group(1)
        is_active = False
    else:
        headword = s
        is_active = True

    return headword.strip(), is_active


def split_by(s, split):
    return re.split(split + '\s(?![^\(]*\))', s)
