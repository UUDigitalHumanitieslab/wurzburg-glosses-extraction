from flask import Blueprint, request, render_template

from extractor.verbextractor import create_verb

site = Blueprint('site', __name__)


@site.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home view. """
    if request.method == 'POST':
        s = request.form['gloss'].encode('utf-8')
        verb = create_verb(s)
        return render_template('results.html', results=verb.headword.decode('utf-8'))
    else:
        return render_template('home.html')
