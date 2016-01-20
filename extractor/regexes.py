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

VERB_HEADWORD = re.compile(r"""
    (.*)\s([A-Z].*)         # splits on a capital letter
""", re.X)

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
    (?:and\s)?                      # matches "and" (optionally)
    ((?:with\s)?                    # matches "with" (optionally)
    (?:elision\sof\s)?              # matches "elision of" (optionally)
    (?:(?:in|suf)fix|anaph)\.\s     # matches "infix/suffix." or "anaph."
    pron\.\s                        # matches "pron."
    (?:[1-3](?:sg|pl)\.\s)?         # matches person and number (optionally)
    (?:[nmf]\.)?)                   # matches gender (optionally)
""", re.X)

VERB_EMPHATIC_ELEMENTS = re.compile(r"""
    (?:and\s)?              # matches "and" (optionally)
    ((?:with\s)?            # matches "with" (optionally)
    emph\.\s                # matches "emph."
    pron\.\s                # matches "pron."
    [1-3](?:sg|pl)\.\s      # matches person and number
    (?:[nmf]\.)?)           # matches gender (optionally)
""", re.X)

ADV_HEADWORD = re.compile(r"""
    (.*?)                   # matches anything (lazily)
    \sAdv\.\s               # matches "Adv."
    (?:of\splace\s)?        # matches "of space" (optionally)
    (?:\(.*?\))?            # matches anything between parentheses
    (?:[,;]\s)?             # matches "[;,]" (optionally)
    ((lit\.\s)?             # matches "lit." (optionally)
    .*?)\.                  # matches anything (lazily) before a dot
""", re.X)

PREP_HEADWORD = re.compile(r"""
    (?:\d\s)?               # matches an optional number
    (.*?)                   # matches anything (lazily)
    (?:\s\(.*?\))?          # matches anything between brackets, optionally
    \sPrep\.                # matches 'Prep.'
""", re.X)

PREP_PARTS = re.compile(r"""
    \s[A-Z]\.\s             # matches a capital letter
""", re.X)

PREP_FORMS = re.compile(r"""
    (.*?)                   # matches anything, lazily
    :\s                     # matches ": "
    (.*?)                   # matches anything, lazily
    (?:\s\([0-9a-z]\)\s     # matches a digit or letter between parentheses
    |$)                     # matches the end of the string
""", re.X)

PREP_CLASSIFIER = re.compile(r"""
    [wW]ith\s               # matches "With" or "with"
    ((?:suffix|poss)\.\s    # matches "suffix" or "poss"
    pron\.)                 # matches "pron."
""", re.X)

PREP_PNG = re.compile(r"""
    (?:[:;]\s)?             # matches "[:;] " (optionally)
    ([1-3])(sg|pl)\.\s      # matches person and number
    ([nmf]\.)?              # matches gender (optionally)
""", re.X)

PREP_EMPH_PRON = re.compile(r"""
    ((?:with\s)?            # matches "with" (optionally)
    emph\.\s                # matches "emph."
    pron\.)                 # matches "pron."
""", re.X)


def match_regex(s, regex):
    """
    Matches the given regex in a string s, and returns the match and the remainder, lstripped.
    If no match is found, the complete string s is returned.
    """
    match = regex.match(s)
    if match:
        matched_s = match.group(1).rstrip()
        post_match = s[match.end(1):].lstrip()
        return matched_s, post_match
    else:
        return None, s
