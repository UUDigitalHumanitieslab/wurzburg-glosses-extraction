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

VERB_STEM_CLASSES = ['Pres. Ind.', 'Imperf.', 'Imperf. Ind.', 'Fut.', 'Sec. Fut.', 'Pres. Subj.',
                     'Past Subj.', 'Pret.', 'Perf.', 'Perfect. Pres. Subj.',
                     'Perfect. Past Subj.', 'Imperat.']

VERB_ADDITIONAL_STEM = re.compile(r"""
    (\(.*?\))               # matches anything between brackets (lazily)
""", re.X)

VERB_PERSON = re.compile(r"""
    ([1-3](?:sg|pl)\.)      # matches the person
""", re.X)

VERB_VOICE = re.compile(r"""
    (.*)                    # matches anything
    (?:\s?Pass\.:?\s?)      # matches 'Pass.:' (optionally)
""", re.X)

VERB_CONJUNCTION = re.compile(r"""
    (with\sconjn\.\s        # matches 'with conjn. '
    (?:and\sneg\.\s)?)      # matches 'and neg. ' optionally
""", re.X)

VERB_RELATIVE = re.compile(r"""
    ([^,]*                  # matches anything but a comma
    rel\.(?:\sn)?)          # matches 'rel.', possibly followed by ' n'
""", re.X)

VERB_PRONOMINAL_OBJECT = re.compile(r"""
    (?:and\s)?              # matches "and" (optionally)
    ((?:with\s)?            # matches "with" (optionally)
    (?:elision\sof\s)?      # matches "elision of" (optionally)
    (?:in|suf)fix\.\s       # matches infix/suffix
    pron\.\s                # matches "pron."
    [1-3](?:sg|pl)\.        # matches person and number
    (?:\s[nmf]\.)?)         # matches gender (optionally)
""", re.X)

VERB_EMPHATIC_ELEMENTS = re.compile(r"""
    (?:and\s)?              # matches "and" (optionally)
    ((?:with\s)?            # matches "with" (optionally)
    emph\.\s                # matches "emph."
    pron\.\s                # matches "pron."
    [1-3](?:sg|pl)\.        # matches person and number
    (?:\s[nmf]\.)?)         # matches gender (optionally)
""", re.X)
