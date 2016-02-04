# -*- coding: utf8 -*-
import codecs
import glob
import os

from bs4 import BeautifulSoup

FOOTNOTES = 'font-family: Times-Roman; font-size:10px'
BOLD = 'Times-Bold'
ITALIC = 'Times-Italic'
SUPERSCRIPT = ['font-family: Times-Roman; font-size:6px', 'font-family: Times-Roman; font-size:5px']
DEFAULT = ['font-family: Times-Roman; font-size:11px', 'font-family: PMKPJI+Times-Roman; font-size:11px']
STYLE_TO_CHAR = {'TTE29AACE8t00': (u'⊃', u'ɫ'),
                 'TTE2A03EA8t00': (u'⊃', u'ɫ'),
                 'TTE2A04708t00': (u'⊃', u'ɫ'),
                 'TTE2A09768t00': (u'ɫ', u'⊃'),
                 'TTE2A0BAA8t00': u'\u032f',
                 'TTE29B0E68t00': u'\u032f',
                 'TTE2A0E268t00': u'\u032f',
                 'TTE2A070A8t00': u'\u032f',
                 'TTE29ACF08t00': u'ā',
                 'TTE2A06528t00': u'ā',
                 'TTE2A0B288t00': u'ā',
                 'TTE2A06D68t00': u'\u0304',
                 'TTE2A03388t00': u' ',
                 'TTE29A57A8t00': u'α',
                 'TTE2A00BE8t00': u'ψ',
                 'TTE2A4F988t00': u'[',  # actually <..>
                 'TTE2A53EA8t00': u'[',
                 'TTE29F5C08t00': u'[literal greek, removed]',
                 'TTE2A05BE8t00': u'[literal greek, removed]',
                 'TTE29FAF88t00': u'[literal greek, removed]',
                 'Greek': u'[literal greek, removed]'}


def as_unicode(tag):
    return unicode(tag).strip('\t\r\n').replace('<br/>', '')


def fix_chars(tag):
    for s, char in STYLE_TO_CHAR.items():
        if s in tag['style']:
            if type(char) == tuple:
                return char[0] if tag.text == '(cid:0)' else char[1]
            else:
                return char
    return ''


def cleanhtml(soup, f, notes):
    superscript = None

    divs = enumerate(soup.body.find_all('div'))
    for n, div in divs:
        if div.text.startswith('Page'):
            pagenumber = div.text.strip()
            try:
                next(divs)
            except StopIteration:
                pass
            continue
        elif div.text.strip().isdigit() or div.text.strip() == '.':
            continue

        for m, span in enumerate(div.find_all('span')):
            style = span['style']
            if FOOTNOTES in style:
                notes.write(pagenumber + '\n')
                notes.write(span.text)
            elif BOLD in style:
                span.name = 'b'
                del span['style']
                f.write(as_unicode(span))
            elif ITALIC in style:
                span.name = 'i'
                del span['style']
                f.write(as_unicode(span))
            elif style in SUPERSCRIPT:
                superscript = span
                superscript.name = 'sup'
                del superscript['style']
            elif style not in DEFAULT:
                # Try to fix unicode characters
                c = fix_chars(span)
                if c:
                    f.write(c)
                else:
                    raise ValueError('Unknown span: ' + unicode(span))
            else:
                if superscript and span.find_all('br'):
                    # Try to place superscript at the end of a span
                    if ' .' in span.text:
                        f.write(span.text.replace(' .', as_unicode(superscript) + '.'))
                    else:
                        f.write(span.text)
                        f.write(as_unicode(superscript))
                    superscript = None
                else:
                    f.write(span.text)

        f.write('\n')


def process(filename):
    soup = BeautifulSoup(open(filename), 'html.parser')
    with codecs.open(os.path.splitext(filename)[0] + '.txt', 'wb', 'utf8') as f:
        with codecs.open(os.path.splitext(filename)[0] + '_footnotes.txt', 'wb', 'utf8') as notes:
            cleanhtml(soup, f, notes)

if __name__ == "__main__":
    for f in glob.glob('data/wurzburg/*.html'):
        print f
        process(f)
