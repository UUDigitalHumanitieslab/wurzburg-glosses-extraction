import copy

from .extractor import extract_forms, extract_loci
from .models import Verb, FormAnalysis
from .regexes import VERB_STEM_CLASSES, VERB_ADDITIONAL_STEM, VERB_PERSON, \
    VERB_RELATIVE, VERB_VOICE, VERB_PRONOMINAL_OBJECT, LOCI


def create_verb(s):
    current_verb = None
    for i, fa in enumerate(s.split('; ')):            # Active and passive FormAnalyses are split by a semi-colon
        current_form_analysis = None
        for j, f in enumerate(fa.split(', ')):        # Forms are separated by a comma
            if i == 0 and j == 0:
                current_verb = find_verb(f)
            current_form_analysis, is_new = create_form_analysis(f, current_form_analysis)
            if is_new:
                current_verb.add_form_analysis(current_form_analysis)
    return current_verb


def find_verb(s):
    stem, pre_stem, post_stem = find_stem_class(s)

    # If we find a stem class, check whether there is a passive annotation
    if stem:
        headword, _ = match_voice(pre_stem)
        verb = Verb(headword, '')
        return verb
    else:
        raise ValueError('No stem class found, this is not a verb: ' + s)


def create_form_analysis(s, current_form_analysis=None):
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
        current_form_analysis = FormAnalysis(stem, None, None, is_active=is_active)
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

    relative, post_relative = match_regex(post_person, VERB_RELATIVE)
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

    if LOCI.match(post_po):
        last_form = current_form_analysis.get_last_form()
        prev_locus = last_form.get_last_locus()
        last_form.append_locus(extract_loci(post_po, prev_locus)[0])
    else:
        current_form_analysis.append_form(extract_forms(post_po)[0])
    return current_form_analysis, is_new


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

    # If we didn't find any stem class, return the complete string.
    if index == len(s):
        return None, None, s

    # Set the pre and post stem variables
    pre_stem = s[:index].rstrip()
    post_stem = s[index + len(stem):].lstrip()

    # Check whether there is additional information on the stem in the post_stem.
    match = VERB_ADDITIONAL_STEM.match(post_stem)
    if match:
        stem += ' ' + match.group(1)
        post_stem = post_stem[match.end(1):].lstrip()

    return stem, pre_stem, post_stem


def match_voice(s):
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


def match_regex(s, regex):
    """
    Matches the given regex in a string s, and returns the match and the remainder, lstripped.
    If no match is found, the complete string s is returned.
    """
    match = regex.match(s)
    if match:
        matched_s = match.group(1)
        post_match = s[match.end(1):].lstrip()
        return matched_s, post_match
    else:
        return None, s
