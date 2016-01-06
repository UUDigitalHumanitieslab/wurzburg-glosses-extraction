import re

from .extractor import extract_forms
from .models import Preposition, FormAnalysis
from .regexes import match_regex, PREP_HEADWORD, PREP_PARTS, PREP_FORMS, PREP_CLASSIFIER, PREP_PNG

ACC_CASE = 'accus.'
DAT_CASE = 'dat.'
SINGULAR = 'sg'
RELATIVE_CLASSIFIER = 'rel. pron.'
ARTICLE_CLASSIFIER = 'def. art.'


def create_preposition(s):
    """
    Creates a PartOfSpeech (of given class cls) from a string s.
    A PartOfSpeech consists of one or more FormAnalyses.
    """
    prep = None
    splits = PREP_PARTS.split(s)
    for n, match in enumerate(splits):
        if n == 0:
            prep = extract_preposition(match)
            pass
        else:
            print n, match
            if 'subst.' in match:
                pass  # add_simple_forms(match, prep)
            elif 'rel. pron.' in match:
                add_simple_forms(match, prep, RELATIVE_CLASSIFIER)
            elif 'art.' in match:
                pass  # add_article_forms(match, prep)
            elif 'poss. pron.' in match or 'suffix. pron.' in match:
                if n == 5:
                    add_pron_form_analyses(match, prep)

    return prep


def extract_preposition(s):
    if 'accus.' in s or 'acc.' in s:
        common_case = ACC_CASE
    elif 'dat.' in s:
        common_case = DAT_CASE

    headword = PREP_HEADWORD.match(s).group(1)

    return Preposition(headword, '', common_case=common_case)


def add_simple_forms(s, current_prep, classifier):
    if classifier:
        current_form_analysis = FormAnalysis(current_prep)
    else:
        current_form_analysis = FormAnalysis(current_prep, classifier=RELATIVE_CLASSIFIER)

    current_prep.add_form_analysis(current_form_analysis)

    forms = []
    for match in PREP_FORMS.findall(s):
        forms.extend(extract_forms(match[1]))

    current_form_analysis.set_forms(forms)


def add_article_forms(s, current_prep):
    current_form_analysis = None
    current_number = SINGULAR
    for n, match in enumerate(re.split(r"""([mfn])\.\s""", s)):
        if n == 0:
            pass
        elif n % 2 == 1:
            current_form_analysis = FormAnalysis(current_prep,
                                                 classifier=ARTICLE_CLASSIFIER,
                                                 number=current_number,
                                                 gender=match)
            current_prep.add_form_analysis(current_form_analysis)
        else:
            current_form_analysis.set_forms(extract_forms(match))


def add_pron_form_analyses(s, current_prep):
    classifier, post_classifier = match_regex(s, PREP_CLASSIFIER)

    current_form_analysis = None
    splits = PREP_PNG.split(post_classifier)
    for n, match in enumerate(splits):
        if n == 0:
            pass
        elif n % 4 == 1:
            current_form_analysis = FormAnalysis(current_prep,
                                                 classifier=classifier,
                                                 person=splits[n],
                                                 number=splits[n + 1],
                                                 gender=splits[n + 2])
            current_prep.add_form_analysis(current_form_analysis)
        elif n % 4 == 0:
            forms = extract_forms(match)

            classifier_match = PREP_CLASSIFIER.match(forms[-1].form)
            if classifier_match:
                forms.pop()
                current_form_analysis.set_forms(forms)
                classifier = classifier_match.group(1)
            else:
                current_form_analysis.set_forms(forms)
