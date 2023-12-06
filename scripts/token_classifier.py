from enum import Enum

class JAMO_TYPE(Enum):
    NONE = 0
    INITIAL = 1
    VOWEL = 2
    FINAL = 3
    FLOATING = 4
    OTHER = 5
    ERROR = 6
    
INIT = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
VOWEL = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
FINAL = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎㅥ"
CONSONANTS = set(INIT + FINAL)

ALL_JAMO = set(INIT + VOWEL + FINAL)

def _all_bad(token):
    return [JAMO_TYPE.ERROR for _ in token]

def token_classifier(token):

    # strip prefix and flag the token
    if token.startswith("__"):
        token = token[2:]
        prefixed = True
    else:
        prefixed = False

    # edge case where we just have one token and it is a consonant
    if len(token) == 1:
        if token in CONSONANTS:
            if token in FINAL and token not in INIT:
                # e.g. ㄺ
                return [JAMO_TYPE.FINAL]
            elif token in INIT and token not in FINAL:
                # e.g. ㄸ
                return [JAMO_TYPE.INITIAL]
            else:
                # if no prefix, is an initial consonant
                if not prefixed:
                    return [JAMO_TYPE.INITIAL]
                else:
                    return [JAMO_TYPE.FLOATING]

    # edge case with no jamo
    if all(t not in ALL_JAMO for t in token):
        return [JAMO_TYPE.OTHER for _ in token]

    known = [JAMO_TYPE.NONE if t not in VOWEL else JAMO_TYPE.VOWEL for t in token]
    v = -1 if JAMO_TYPE.VOWEL not in known else known.index(JAMO_TYPE.VOWEL)


    if v != -1:
        c = v+1
        cur = known[v]

        # start from the first vowel and move one-by-one to the right
        while c < len(known):
            if cur == JAMO_TYPE.VOWEL and token[c] in FINAL:
                known[c] = JAMO_TYPE.FINAL
            elif cur == JAMO_TYPE.FINAL:
                if token[c] in INIT:
                    known[c] = JAMO_TYPE.INITIAL
                elif token[c] not in ALL_JAMO:
                    known[c] = JAMO_TYPE.OTHER
                else:
                    return _all_bad(token)
            elif cur == JAMO_TYPE.INITIAL:
                if token[c] not in VOWEL:
                    return _all_bad(token)
                else:
                    known[c] = JAMO_TYPE.VOWEL
            elif cur == JAMO_TYPE.OTHER:
                if token[c] not in ALL_JAMO:
                    known[c] = JAMO_TYPE.OTHER
                elif token[c] in INIT:
                    known[c] = JAMO_TYPE.INITIAL
                else:
                    return _all_bad(token)

            cur = known[c]
            c += 1

        # now that everything to the right of the first vowel is done, reverse the process (and the state machine) and go to the left; i.e., v -> i -> f -> v -> i -> f...
        c = v - 1
        cur = known[v]
        while c >= 0:
            if cur == JAMO_TYPE.VOWEL and token[c] in INIT:
                known[c] = JAMO_TYPE.INITIAL
            elif cur == JAMO_TYPE.INITIAL:
                if token[c] in FINAL:
                    known[c] = JAMO_TYPE.FINAL
                elif token[c] not in ALL_JAMO:
                    known[c] = JAMO_TYPE.OTHER
                else:
                    return _all_bad(token)
            elif cur == JAMO_TYPE.FINAL and token[c] in VOWEL:
            # i don't actually think this case can be hit, cause then we must not have started at the leftmost vowel
                known[c] = JAMO_TYPE.VOWEL
            elif cur == JAMO_TYPE.OTHER:
                if token[c] not in ALL_JAMO:
                    known[c] = JAMO_TYPE.OTHER
                elif token[c] in FINAL:
                    known[c] = JAMO_TYPE.FINAL
                else:
                    return _all_bad(token)
            else:
                return _all_bad(token)

            cur = known[c]
            c -= 1
            
    else: # no vowels
        known = [JAMO_TYPE.OTHER if t not in CONSONANTS else JAMO_TYPE.FLOATING for t in token]
        num_cons = known.count(JAMO_TYPE.FLOATING)
        ## one consonant case
        if num_cons == 1:
            # 1) xyzㄱ -> init
            # 2) ㄱxyz -> final
            # 3) abcㄱxyz -> error

            i = known.index(JAMO_TYPE.FLOATING)

            if i == len(token) - 1:
                if token[i] in INIT:
                    known[i] = JAMO_TYPE.INITIAL
                else:
                    return _all_bad(token)
            elif i == 0:
                if token[i] in FINAL:
                    known[i] = JAMO_TYPE.FINAL
                else:
                    return _all_bad(token)
            else:
                return _all_bad(token)

        elif num_cons == 2:
            # 1) ㄱㄱ -> final init
            # 2) ㄱxyzㄱ -> final xyz init
            # 3) other -> error
            i, j = [idx for (idx, n) in enumerate(known) if n == JAMO_TYPE.FLOATING]
            if i != 0:
                return _all_bad(token)

            if len(token) == 2 and token[i] in FINAL and token[j] in INIT:
                return [JAMO_TYPE.FINAL, JAMO_TYPE.INITIAL]

            else:
                if token[i] not in FINAL:
                    return _all_bad(token)
                else:
                    known[i] = JAMO_TYPE.FINAL
                    if j != i+1:
                        if j != len(token) - 1 or token[j] not in INIT:
                            return _all_bad(token)
                        else:
                            if j == len(token) - 1 and token[j] in INIT:
                                known[j] = JAMO_TYPE.INITIAL
                            else:
                                return _all_bad(token)
                    else:
                        return _all_bad(token)
        else: # more than 2 consonants, but no vowels
            return _all_bad(token)
    
    return known


# _ENUM_MAP =   {"I": JAMO_TYPE.INITIAL, "V": JAMO_TYPE.VOWEL, "F": JAMO_TYPE.FINAL, "O" : JAMO_TYPE.OTHER}

# def _convert_test_case(test_case, expected):
#     if expected == "ERROR":
#         return [JAMO_TYPE.ERROR for _ in test_case]

#     elif expected == "FLOAT":
#         if len(test_case) == 1:
#             return [JAMO_TYPE.FLOATING]
#         else:
#             raise ValueError("bad test case")

#     elif len(test_case) != len(expected):
#         raise ValueError("bad test case")

#     else:
#         return [_ENUM_MAP[t] for t in expected]

# samples = [("ㅎㅏㄴㄱㅜㄱ", "IVFIVF"),
#           ("ㅏㄴㄱㅜㄱㅎ", "VFIVFI"),
#           ("ㅏㄴㄱㅜㄱ", "VFIVF"),
#           ("ㄴㄱㅜㄱㅇㅓ", "FIVFIV"),
#           ("ㄴㄱㅜㄱ", "FIVF"),
#           ("ㄴㄱ", "FI"),
#           ("ㄴ",  "I"), # should be definitely an I, accounting for lack of "__" prefix
#           ("ㄸ", "I"),
#           ("ㄿ", "F"),
#           ("ㅏ", "V"),
#           ("a", "O"),
#           ("aㄱㄱ", "ERROR"), 
#           ("ㄱㄱa", "ERROR"),
#           ("ㄱabcㄱ", "FOOOI"),
#           ("ㄸabcㄸ", "ERROR"),
#           ("ㄸabcㄷ", "ERROR"), # (ㄸ can't be 받침)
#           ("ㄷabcㄸ", "FOOOI"), # (ㄷ can be 받침)
#           ("ㄸㄷ", "ERROR"),  # (ㄸ can't be 받침)
#           ("ㄷㄸ", "FI"),
#           ("ㄷㄷ", "FI"),
#           ("ㄸㄸ", "ERROR"), # (ㄸ can't be 받침)
#           ("ㄴㄴabc", "ERROR"),
#           ("abc", "OOO"),
#           ("ㄱㄱㄱ", "ERROR"),
#           ("__ㄱ", "FLOAT"),
#           ("ㄱ", "I"),
#           ("abcㄱㅏㄱabcㅎㅏㄴㄱㅜ", "OOOIVFOOOIVFIV")
#           ]

# for (token, expected) in samples:
#     print(token, token_classifier(token))