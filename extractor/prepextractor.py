import copy
import re

from .extractor import extract_forms
from .models import Preposition, FormAnalysis
from .regexes import match_regex, PREP_HEADWORD, PREP_PARTS, PREP_FORMS, PREP_CLASSIFIER, PREP_PNG, PREP_EMPH_PRON

NO_CASE = '?'
ACC_CASE = 'accus.'
DAT_CASE = 'dat.'
GEN_CASE = 'gen.'
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
            if 'rel. pron.' in match or 'rel. part.' in match:
                add_simple_forms(match, prep, RELATIVE_CLASSIFIER)
            elif 'art.' in match:
                add_article_forms(match, prep)
            elif 'poss. pron.' in match or 'suffix. pron.' in match:
                pass #add_pron_form_analyses(match, prep)
            else:
                add_simple_forms(match, prep)

    return prep


def extract_preposition(s):
    common_case = NO_CASE

    if 'accus' in s or 'acc.' in s:
        common_case = ACC_CASE
    elif 'dat.' in s:
        common_case = DAT_CASE
    elif 'gen.' in s:
        common_case = GEN_CASE

    headword = PREP_HEADWORD.match(s).group(1)

    return Preposition(headword, '', common_case=common_case)


def add_simple_forms(s, current_prep, classifier=None):
    current_form_analysis = FormAnalysis(current_prep, classifier=classifier)

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
    """
    Adds FormAnalyses to the current Preposition from the listings
    that start with "With poss. pron." or "With suffix. pron."
    :param s: The listing
    :param current_prep: The current Preposition
    :return:
    """
    classifier, post_classifier = match_regex(s, PREP_CLASSIFIER)

    current_form_analysis = None
    current_ee = None
    splits = PREP_PNG.split(post_classifier)
    for n, match in enumerate(splits):
        if n == 0:
            pass
        elif n % 4 == 1:
            current_form_analysis = FormAnalysis(current_prep,
                                                 classifier=classifier,
                                                 person=splits[n],
                                                 number=splits[n + 1],
                                                 gender=splits[n + 2],
                                                 empathic_elements=current_ee)
            current_prep.add_form_analysis(current_form_analysis)
        elif n % 4 == 0:
            forms = extract_forms(match)

            for form in forms:
                emph_pron, post_emph_pron = match_regex(form.form, PREP_EMPH_PRON)
                # If we find an emph_pron and there is a form after that, copy the current FormAnalysis
                if emph_pron and post_emph_pron:
                    current_form_analysis = copy.deepcopy(current_form_analysis)
                    current_form_analysis.empathic_elements = emph_pron
                    current_form_analysis.set_forms([])
                    current_prep.add_form_analysis(current_form_analysis)
                    form.form = post_emph_pron
                    current_form_analysis.append_form(form)
                # If we find an emph_pron but there is no form after that, add it to the next FormAnalysis
                elif emph_pron:
                    current_ee = emph_pron
                # Otherwise, set the current_ee back to None and add the Form
                else:
                    current_ee = None
                    current_form_analysis.append_form(form)
