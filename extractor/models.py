class Locus:
    OCCURRENCES_MAP = {'': 1, 'bis': 2, 'ter': 3, 'quatter': 4}

    def __init__(self, page, column, number, subdivision, nr_occurrences):
        self.page = page
        self.column = column
        self.number = number
        self.subdivision = subdivision
        self.nr_occurrences = self.occurrences_to_int(nr_occurrences)

    def occurrences_to_int(self, nr_occurrences):
        if nr_occurrences in self.OCCURRENCES_MAP:
            return self.OCCURRENCES_MAP[nr_occurrences]
        else:
            raise ValueError('Unknown number of occurrences: {}'.format(nr_occurrences))

    def __str__(self):
        return 'LOCUS p: {}, c: {}, n: {}, s: {}, nr: {}'.format(self.page, self.column, self.number, self.subdivision, self.nr_occurrences)
