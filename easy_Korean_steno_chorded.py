import re

LONGEST_KEY = 1

# list of keys for consonants and vowels
starting_consonants = {
    "regular": {
        # consonants
        "K": 0,  # ㄱ
        "TKPW": 0,  # ㄱ
        "TPH": 2,  # ㄴ
        "TK": 3,  # ㄷ
        "R": 5,  # ㄹ
        "HR": 5,  # ㄹ
        "PH": 6,  # ㅁ
        "PW": 7,  # ㅂ
        "S": 9,  # ㅅ
        "W": 11,  # ㅇ
        "SKWR": 12,  # ㅈ
        "KH": 14,  # ㅊ
        "KP": 15,  # ㅋ
        "T": 16,  # ㅌ
        "P": 17,  # ㅍ
        "H": 18,  # ㅎ
        # extra
        "TH": 4,  # ㄸ
        "": 11,  # ㅇ
    },
    "tense": {
        # tense consonants (add *)
        "K": 1,  # ㄲ
        "TKPW": 1,  # ㄲ
        "TK": 4,  # ㄸ
        "PW": 8,  # ㅃ
        "SKWR": 13,  # ㅉ
        "S": 10,  # ㅆ
    },
    "special": {
        # adds "y" to vowels
        "KW": 0,  # ㄱ
        "TKPWR": 0,  # ㄱ
        "TPWH": 2,  # ㄴ
        "TKW": 3,  # ㄷ
        "WR": 5,  # ㄹ
        "WHR": 5,  # ㄹ
        "KPWHR": 6,  # ㅁ
        "KPWR": 7,  # ㅂ
        "SH": 9,  # ㅅ
        "KWR": 11,  # ㅇ
        "SKW": 12,  # ㅈ
        "KWH": 14,  # ㅊ
        "KPW": 15,  # ㅋ
        "TKWR": 16,  # ㅌ
        "KPR": 17,  # ㅍ
        "WH": 18,  # ㅎ
        "STKPWHR": 0,  # empty
    },
}
vowels = {
    # vowels
    "A": 0,  # ㅏ
    "U": 4,  # ㅓ
    "O": 8,  # ㅗ
    "AO": 13,  # ㅜ
    "AOU": 18,  # ㅡ
    "AU": 18,  # ㅡ
    "EU": 20,  # ㅣ
    # complex vowels
    "AEU": 1,  # ㅐ
    "AE": 5,  # ㅔ
    # extra/compound
    "E": 19,  # ㅢ
    "OEU": 11,  # ㅚ
    "AOU": 14,  # ㅝ
    "OU": 9,  # ㅘ
    "AOEU": 16,  # ㅟ
    "": 0,  # empty
}
y_vowels = {
    # "y" vowels
    "A": 2,  # ㅑ
    "U": 6,  # ㅕ
    "O": 12,  # ㅛ
    "OE": 12,  # ㅛ
    "AOU": 17,  # ㅠ
    "AO": 17,  # ㅠ
    "AEU": 3,  # ㅒ
    "AE": 7,  # ㅖ
    "EU": 20,  # ㅣ
    "": 0,  # empty
}
ending_consonants = {
    # consonants
    "G": 1,  # ㄱ
    "PB": 4,  # ㄴ
    "D": 7,  # ㄷ
    "R": 8,  # ㄹ
    "L": 8,  # ㄹ
    "PL": 16,  # ㅁ
    "B": 17,  # ㅂ
    "S": 19,  # ㅅ
    "PBG": 21,  # ㅇ
    "PBLG": 22,  # ㅈ
    "FP": 23,  # ㅊ
    "BG": 24,  # ㅋ
    "T": 25,  # ㅌ
    "P": 26,  # ㅍ
    "F": 27,  # ㅎ
    # tense consonants (add -R)
    "RG": 0,  # ㄲ
    "RD": 0,  # ㄸ
    "RB": 0,  # ㅃ
    "RPBLG": 0,  # ㅉ
    "RS": 0,  # ㅆ
    "Z": 0,  # ㅆ
    "": 0,  # empty
}


def lookup(chord):
    stroke = chord[0]
    if len(chord) != 1:
        raise KeyError
    assert len(chord) <= LONGEST_KEY

    # backspacing
    if stroke == "*":
        return "{#left}{#right}{#backspace}"

    # the regex decomposes a stroke into the following groups/variables:
    # start consonants               #STKPWHR
    # vowel 1                                 AO
    # stress start consonants                    */-
    # vowel 2                                        EU
    # end consonants                                    FRPBLGTSDZ
    match = re.fullmatch(r"([#STKPWHR]*)([AO]*)([*-]?)([EU]*)([FRPBLGTSDZ]*)", stroke)

    if match is None:
        raise KeyError
    (
        start_consonant,
        vowel1,
        stress,
        vowel2,
        end_consonant,
    ) = match.groups()

    # get start consonant
    add_y = False
    # detect stress
    if stress == "*" and start_consonant in starting_consonants["tense"]:
        start_final = starting_consonants["tense"][start_consonant]
    elif start_consonant in starting_consonants["regular"]:
        start_final = starting_consonants["regular"][start_consonant]
    elif start_consonant in starting_consonants["special"]:
        add_y = True
        start_final = starting_consonants["special"][start_consonant]
    else:
        raise KeyError

    # get vowel
    vowel = vowel1 + vowel2
    if vowel not in vowels and vowel not in y_vowels:
        raise KeyError
    if start_consonant in starting_consonants["special"] and not vowel:
        raise KeyError
    if add_y:
        vowel_final = y_vowels[vowel]
    else:
        vowel_final = vowels[vowel]

    # only vowel output using *
    if stress == "*" and start_consonant == 0:
        start_final = 0

    # get end consonant
    if end_consonant not in ending_consonants:
        raise KeyError
    # only end output
    if end_consonant == 0 and start_consonant == 0:
        start_final = 0
    end_final = ending_consonants[end_consonant]

    # combine output
    hangul_offset = 44032
    initial = start_final * 588
    medial = vowel_final * 28
    final = end_final
    code_point = hangul_offset + initial + medial + final
    return "{^}" + chr(code_point) + "{^}"
