import copy

from .extractor import extract_forms
from .models import Verb, FormAnalysis
from .regexes import VERB_STEM_CLASSES, VERB_ADDITIONAL_STEM, VERB_PERSON, VERB_RELATIVE, VERB_VOICE, VERB_PRONOMINAL_OBJECT


def create_verb(s):
    current_verb = None
    for i, fa in enumerate(s.split('; ')):            # Active and passive FormAnalyses are split by a semi-colon
        current_form_analysis = None
        for j, f in enumerate(fa.split(', ')):        # Forms are separated by a comma
            if i == 0 and j == 0:
                current_verb = find_verb(f)
            current_form_analysis = create_form_analysis(f, current_form_analysis)
            current_verb.add_form_analysis(current_form_analysis)
    return current_verb


def find_verb(s):
    stem, pre_stem, post_stem = find_stem_class(s)

    # If we find a stem class, check whether there is a passive annotation
    if stem:
        headword, is_active = find_voice(pre_stem)
        verb = Verb(headword, '')
        return verb
    else:
        raise ValueError('No stem class found, this is not a verb: ' + s)


def create_form_analysis(s, current_form_analysis=None):
    """
    Creates or appends a FormAnalysis from a string s, recursively.
    """
    stem, pre_stem, post_stem = find_stem_class(s)

    # If we find a stem class, check whether there is a passive annotation
    if stem:
        _, is_active = find_voice(pre_stem)

        # Start a new FormAnalysis when we find a stem class
        current_form_analysis = FormAnalysis(stem, None, None, is_active=is_active)

    person, post_person = find_regex(post_stem, VERB_PERSON)

    # If person was set, this starts a new FormAnalysis
    if current_form_analysis.person:
        current_form_analysis = copy.deepcopy(current_form_analysis)
        current_form_analysis.set_forms([])

    if person:
        current_form_analysis.person = person

    relative, post_relative = find_regex(post_person, VERB_RELATIVE)

    # If relative was set, this starts a new FormAnalysis
    if current_form_analysis.relative:
        current_form_analysis = copy.deepcopy(current_form_analysis)
        current_form_analysis.set_forms([])

    if relative:
        current_form_analysis.relative = relative

    pronominal_object, post_po = find_regex(post_relative, VERB_PRONOMINAL_OBJECT)

    # If pronominal object was set, this starts a new FormAnalysis
    if current_form_analysis.pronominal_object:
        current_form_analysis = copy.deepcopy(current_form_analysis)
        current_form_analysis.set_forms([])

    if pronominal_object:
        current_form_analysis.pronominal_object = pronominal_object

    current_form_analysis.append_form(extract_forms(post_po)[0])
    return current_form_analysis


def find_stem_class(s):
    """
    Finds the first occurrence of a verb stem class in a string.
    """
    stem = None
    index = len(s)
    for stem_class in VERB_STEM_CLASSES: 
        found = s.find(stem_class)
        if found != -1 and found < index:
            stem = stem_class
            index = found

    if index == len(s):
        return None, None, s

    pre_stem = s[:index]
    post_stem = s[index + len(stem):]

    match = VERB_ADDITIONAL_STEM.match(post_stem)
    if match:
        stem += ' ' + match.group(1)
        post_stem = post_stem[match.end(1):]

    return stem, pre_stem, post_stem


def find_voice(s):
    """
    Matches the voice of the string and splits the headword off the front.
    """
    match = VERB_VOICE.match(s)
    if match:
        headword = match.group(1)
        is_active = False
    else:
        headword = s
        is_active = True

    return headword.strip(), is_active


def find_regex(s, regex):
    """
    Matches the given regex in a string s, and returns the match and the remainder.
    """
    match = regex.match(s)
    if match:
        matched_s = match.group(1)
        post_match = s[match.end(1):].lstrip()
        return matched_s, post_match
    else:
        return None, s
