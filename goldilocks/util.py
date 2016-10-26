import re

FORMAT_BED = "bed"
FORMAT_CIRCOS = "circos"
FORMAT_MELT = "melt"
FORMAT_TABLE = "table"

SORT_MIN = "min"
SORT_MAX = "max"
SORT_MEAN = "mean"
SORT_MEDIAN = "median"
SORT_NONE = "none"


def parse_si_bp(option):
    SI_STEPS = {
        'K': 1000,                  # strictly speaking should be k...
        'M': 1000000,
        'G': 1000000000,
        'T': 1000000000000,
    }

    option = str(option).upper().strip().replace(' ', '').replace('BP', '')

    # I'd rather not use RE for this...
    try:
        bases = re.findall('-?\d+', option)[0]
        option = option.replace(bases, '')
    except IndexError:
        raise ValueError()

    bases = int(bases)
    for char in option:
        if char in SI_STEPS:
            bases *= SI_STEPS[char]
    return bases
