import re

POS_DEFINITION = re.compile(r"""
    ([^\.,]*)               # matches anything but a space or dot, the headword
    \s(?:([nmf])\.\s)?      # matches the gender (optionally)
    ([^\.,]*)               # matches anything but a space or dot, the stem class
    [\.,]                   # matches the end of the definition
""", re.X)

POS_EXTRA_INFO = re.compile(r"""
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