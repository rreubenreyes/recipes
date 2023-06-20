import unicodedata

_unicode_fraction_descriptors = {
    "ZERO": 0,
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
    "SIX": 6,
    "SEVEN": 7,
    "EIGHT": 8,
    "NINE": 9,
    "HALF": 2,
    "HALVES": 2,
    "THIRD": 3,
    "THIRDS": 3,
    "QUARTER": 4,
    "QUARTERS": 4,
    "FIFTH": 5,
    "FIFTHS": 5,
    "SIXTH": 6,
    "SIXTHS": 6,
    "SEVENTH": 7,
    "SEVENTH": 7,
    "EIGHTH": 8,
    "EIGHTHS": 8,
    "NINTH": 9,
    "NINTHS": 9,
}


def _replace_fraction(unicode_name):
    fraction_parts = unicode_name.split("FRACTION")[1].strip().split(" ")

    return "/".join([str(_unicode_fraction_descriptors[x]) for x in fraction_parts])


def _is_latin(string: str):
    end_of_latin_unicode_space = int("0x1EFF", 16)
    return ord(string) <= end_of_latin_unicode_space


def replace(string: str):
    if _is_latin(string):
        un = unicodedata.name(string)
        if "FRACTION" in un:
            return _replace_fraction(un)

        return string

    return ""


def replace_all(string: str):
    return "".join([replace(char) for char in string]).strip()
