import re

from .extractor import extract_forms
from .models import FormAnalysis
from .regexes import PREP_PNG

SINGULAR = 'sg'


def add_article_form_analyses(s, current_prep):
    current_form_analysis = None
    current_number = SINGULAR
    for n, match in enumerate(re.split(r"""([mfn])\.\s""", s)):
        if n == 0:
            classifier = match
        elif n % 2 == 1:
            current_form_analysis = FormAnalysis(current_prep, classifier=classifier, number=current_number, gender=match)
            current_prep.add_form_analysis(current_form_analysis)
        else:
            current_form_analysis.set_forms(extract_forms(match))


def add_pron_form_analyses(s, current_prep):
    current_form_analysis = None
    match = PREP_PNG.match(s)
