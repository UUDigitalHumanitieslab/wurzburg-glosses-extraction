import re

from .extractor import extract_forms
from .models import FormAnalysis
from .regexes import match_regex, PREP_CLASSIFIER, PREP_PNG

SINGULAR = 'sg'
ARTICLE_CLASSIFIER = 'def. art.'


def add_article_form_analyses(s, current_prep):
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
