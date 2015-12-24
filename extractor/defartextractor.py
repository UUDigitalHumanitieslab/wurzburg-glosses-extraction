import re

from .extractor import extract_forms
from .models import DefiniteArticle, FormAnalysis
from .regexes import PREP_FORMS


def create_definite_article(s):
    headword = ''
    return DefiniteArticle(headword, '')


def add_simple_forms(s, current_form_analysis, has_prep):
    forms = []
    if has_prep:
        common_meaning = 'with prep and following substantive'
    else:
        common_meaning = 'with following substantive'

    for match in PREP_FORMS.findall(s):
        if match[0].startswith('With neut. dem.'):
            # TODO: create new form analysis with alternative meaning
            common_meaning = 'with following dem. pron.'

        forms.extend(extract_forms(match[1]))

    current_form_analysis.set_forms(forms)