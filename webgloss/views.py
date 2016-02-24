from flask import Blueprint, request, render_template

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
        if pos == 'noun' or pos == 'adjective':
            pos = create_pos(s)
        elif pos == 'verb':
            pos = create_verb(s)
        elif pos == 'adv':
            pos = create_adverb(s)
        elif pos == 'prep':
            pos = create_preposition(s)
        elif pos == 'art':
            pos = create_definite_article(s)
        return render_template('results.html', pos=pos)
    else:
        return render_template('home.html')
