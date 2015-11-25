import re

POS_ANALYSIS = re.compile(r"""
    ([^\.,]*)               # matches anything but a space or dot, the headword
    \s(?:([nmf])\.\s)?      # matches the gender (optionally)
    ([^\.,]*)               # matches anything but a space or dot, the stem class
    [\.,]                   # matches the end of the definition
""", re.X)

POS_DEFINITION = re.compile(r"""
    (?:\((.*)\))            # matches the additional info between brackets (optionally)
    ?([^\(\)]*)\.           # matches the definition, not between brackets
""", re.X)

FORM_ANALYSES = re.compile(r"""
    ([NVAGD](?:sg|pl|du))\. # matches the grammatical label (e.g. Nsg. or Ddu.)
    \s(?:([nmf])\.\s)?      # matches the gender (optionally)
""", re.X)

FORMS = re.compile(r"""
    \s?                     # start with any whitespace (optionally)
    ([^\d,=]+)              # matches anything but a number, comma or dot, allowing unicode.
    (?![^\(]*\))            # requires the expression to not be between parentheses (negative lookahead)
    \s                      # end with any whitespace
""", re.X + re.U)

LOCI = re.compile(r"""
    (\d+)                   # matches the page
    ([a-d]?)                # matches the column (optionally)
    (\d*)                   # matches the number
    ([a-d]?)                # matches the subdivision (optionally)
    (?:\s\((\w+)\))?        # matches the nr_occurrences (optionally)
    (?:\s\((.*)\))?         # matches alternative locus between brackets (optionally)
""", re.X)

VERB_PERSON = re.compile(r'\s*([1-3](?:sg|pl))\.\s(.*)', re.X)
VERB_VOICE = re.compile(r'(.*)(?:\s?Pass\.:\s?)', re.X)
VERB_PRONOMINAL_OBJECT = re.compile(r"""
    ([^,]*?)                # matches anything but a comma (lazy)
    ((?:with)?\s            # matches "with" (optionally)
    (?:in|suf)fix\.\s       # matches infix/suffix
    pron\.\s                # matches "pron."
    [1-3](?:sg|pl)\.\s      # matches person and number
    (?:[nmf]\.\s)?)         # matches gender (optionally)
""", re.X)
VERB_STEM_CLASSES = ['Pres. Ind.', 'Imperf.', 'Fut.', 'Sec. Fut.', 'Pres. Subj.', 
    'Past Subj.', 'Pret.', 'Perf.', 'Perfect. Pres. Subj.', 'Perfect. Past Subj.', 'Imperat.']
VERB_ADDITIONAL_STEM = re.compile(r'\s*(\(.*?\))')