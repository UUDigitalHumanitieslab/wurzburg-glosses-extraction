import re

from .extractor import extract_forms
from .models import DefiniteArticle, FormAnalysis
from .regexes import PREP_FORMS

MEANING_SUBST = 'with following substantive'
MEANING_PREP_SUBST = 'with prep and following substantive'
MEANING_DEM_PRON = 'with following dem. pron.'


def create_definite_article(s):
    headword = ''
    return DefiniteArticle(headword, '')


def add_simple_forms(s, current_form_analysis, has_prep):
    forms = []
    if has_prep:
        common_meaning = MEANING_PREP_SUBST
    else:
        common_meaning = MEANING_SUBST

    for match in PREP_FORMS.findall(s):
        if match[0].startswith('With neut. dem.'):
            # TODO: create new form analysis with alternative meaning
            common_meaning = MEANING_DEM_PRON
        else:
            common_meaning = MEANING_PREP_SUBST

        forms.extend(extract_forms(match[1]))

    current_form_analysis.set_forms(forms)