import copy

from .extractor import extract_forms
from .models import Verb, FormAnalysis
from .regexes import VERB_STEM_CLASSES, VERB_ADDITIONAL_STEM, VERB_PERSON, VERB_VOICE, VERB_PRONOMINAL_OBJECT


def create_verb(s, current_verb=None, current_form_analysis=None):
    """
    Creates a Verb from a string s, recursively.
    """
    headword = None

    stem, pre_stem, post_stem = find_stem_class(s)
    # If we find a stem class, check whether there is a passive annotation
    if stem:
        headword, is_active = find_voice(pre_stem)
        if headword and current_verb:
            raise ValueError('New headword in ' + headword)
        elif headword: 
            current_verb = Verb(headword, '')

        # Start a new FormAnalysis when we find a stem class
        current_form_analysis = FormAnalysis(stem, None, None, is_active=is_active)
        current_verb.add_form_analysis(current_form_analysis)

    if current_verb:
        person, post_person = find_person(post_stem)

        # If person was set, this starts a new FormAnalysis
        if current_form_analysis.person:
            current_form_analysis = copy.deepcopy(current_form_analysis)
            current_verb.add_form_analysis(current_form_analysis)
        
        if person:
            current_form_analysis.person = person

        match = VERB_PRONOMINAL_OBJECT.match(post_person)
        if match:
            # If pronominal object was set, this starts a new FormAnalysis
            if current_form_analysis.pronominal_object:
                current_form_analysis = copy.deepcopy(current_form_analysis)
                current_verb.add_form_analysis(current_form_analysis)

            current_form_analysis.relative = match.group(1).strip()
            current_form_analysis.pronominal_object = match.group(2)
            post_po = post_person[match.end(2):]
        else:
            post_po = post_person

        for form in post_po.split(', '):
            try:
                if form.startswith('with'):
                    print 'TODO! ' + form
                current_form_analysis.set_forms(extract_forms(form))
            except ValueError:
                create_verb(form, current_verb, current_form_analysis)
    else: 
        raise ValueError('No current verb available for ' + s)

    return current_verb


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

def find_person(s):
    """
    Matches the person in a string s.
    """
    match = VERB_PERSON.match(s)
    if match: 
        person = match.group(1)
        post_person = match.group(2)
        return person, post_person
    else:
        return None, s
