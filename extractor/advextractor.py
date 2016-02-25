from .extractor import extract_forms
from .models import Adverb, FormAnalysis
from .regexes import remove_html_tags, ADV_HEADWORD


def create_adverb(s):
    match = ADV_HEADWORD.match(s)
    if match:
        headword = remove_html_tags(match.group(1))
        definition = remove_html_tags(match.group(2))
        post_definition = s[match.end(2) + 2:].lstrip()

        # Special case when no definition is given, but only forms/loci
        if not post_definition and definition[0].islower():
            post_definition = definition
            definition = ''

        adverb = Adverb(headword, definition)
        fa = FormAnalysis(adverb)
        fa.set_forms(extract_forms(post_definition))
        adverb.add_form_analysis(fa)
        return adverb
    else:
        raise ValueError('This is not an Adverb')
