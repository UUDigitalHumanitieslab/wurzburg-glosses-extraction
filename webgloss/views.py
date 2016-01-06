from flask import Blueprint, request, render_template

from extractor.models import Noun, Adjective
from extractor.advextractor import create_adverb
from extractor.extractor import create_pos
from extractor.prepextractor import create_preposition
from extractor.defartextractor import create_definite_article
from extractor.verbextractor import create_verb

site = Blueprint('site', __name__)


@site.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home view. """
    if request.method == 'POST':
        pos = request.form['pos']
        s = request.form['gloss'].encode('utf-8')
        if pos == 'noun':
            pos = create_pos(s, Noun)
        if pos == 'adj':
            pos = create_pos(s, Adjective)
        if pos == 'verb':
            pos = create_verb(s)
        if pos == 'adv':
            pos = create_adverb(s)
        if pos == 'prep':
            pos = create_preposition(s)
        if pos == 'art':
            pos = create_definite_article(s)
        return render_template('results.html', pos=pos)
    else:
        return render_template('home.html')
