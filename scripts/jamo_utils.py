# Defining dictionaries, lookup tables, constants

JAMO_DICT = {
        'initial': [chr(code) for code in range(0x1100, 0x1113)],
        'vowel': [chr(code) for code in range(0x1161, 0x1176)],
        'final': [chr(0x11FF)] + [chr(code) for code in range(0x11A8, 0x11C3)]  # add a 0x11FF (HANGUL JONGSEONG SSANGNIEUN) as the first index for syllables with no jongseong
    }

K1 = 44032
K2 = 588
K3 = 28

JAMO_TO_COMPAT_LOOKUP_CHOSEONG = {# initial
                                0x1100 : 0x3131, #'ㄱ'
                                0x1101 : 0x3132, #'ㄲ'
                                0x1102 : 0x3134, #'ㄴ'
                                0x1103 : 0x3137, #'ㄷ'
                                0x1104 : 0x3138, #'ㄸ'
                                0x1105 : 0x3139, #'ㄹ'
                                0x1106 : 0x3141, #'ㅁ'
                                0x1107 : 0x3142, #'ㅂ'
                                0x1108 : 0x3143, #'ㅃ'
                                0x1109 : 0x3145, #'ㅅ'
                                0x110A : 0x3146, #'ㅆ'
                                0x110B : 0x3147, #'ㅇ'
                                0x110C : 0x3148, #'ㅈ'
                                0x110D : 0x3149, #'ㅉ'
                                0x110E : 0x314A, #'ㅊ'
                                0x110F : 0x314B, #'ㅋ'
                                0x1110 : 0x314C, #'ㅌ'
                                0x1111 : 0x314D, #'ㅍ'
                                0x1112 : 0x314E #'ㅎ'
                                }   
                         # vowel
JAMO_TO_COMPAT_LOOKUP_JUNGSEONG = {0x1161 : 0x314F, #'ㅏ'
                                0x1162 : 0x3150, #'ㅐ'
                                0x1163 : 0x3151, #'ㅑ'
                                0x1164 : 0x3152, #'ㅒ'
                                0x1165 : 0x3153, #'ㅓ'
                                0x1166 : 0x3154, #'ㅔ'
                                0x1167 : 0x3155, #'ㅕ'
                                0x1168 : 0x3156, #'ㅖ'
                                0x1169 : 0x3157, #'ㅗ'
                                0x116A : 0x3158, #'ㅘ'
                                0x116B : 0x3159, #'ㅙ'
                                0x116C : 0x315A, #'ㅚ'
                                0x116D : 0x315B, #'ㅛ'
                                0x116E : 0x315C, #'ㅜ'
                                0x116F : 0x315D, #'ㅝ'
                                0x1170 : 0x315E, #'ㅞ'
                                0x1171 : 0x315F, #'ㅟ'
                                0x1172 : 0x3160, #'ㅠ'
                                0x1173 : 0x3161, #'ㅡ'
                                0x1174 : 0x3162, #'ㅢ'
                                0x1175 : 0x3163  #'ㅣ'
                                }
                         # final
JAMO_TO_COMPAT_LOOKUP_JONGSEONG = {0x11A8 : 0x3131, #'ㄱ'
                                0x11A9 : 0x3132, #'ㄲ'
                                0x11AA : 0x3133, #'ㄳ'
                                0x11AB : 0x3134, #'ㄴ'
                                0x11AC : 0x3135, #'ㄵ'
                                0x11AD : 0x3136, #'ㄶ'
                                0x11AE : 0x3137, #'ㄷ'
                                0x11AF : 0x3139, #'ㄹ'
                                0x11B0 : 0x313A, #'ㄺ'
                                0x11B1 : 0x313B, #'ㄻ'
                                0x11B2 : 0x313C, #'ㄼ'
                                0x11B3 : 0x313D, #'ㄽ'
                                0x11B4 : 0x313E, #'ㄾ'
                                0x11B5 : 0x313F, #'ㄿ'
                                0x11B6 : 0x3140, #'ㅀ'
                                0x11B7 : 0x3141, #'ㅁ'
                                0x11B8 : 0x3142, #'ㅂ'
                                0x11B9 : 0x3144, #'ㅄ'
                                0x11BA : 0x3145, #'ㅅ'
                                0x11BB : 0x3146, #'ㅆ'
                                0x11BC : 0x3147, #'ㅇ'
                                0x11BD : 0x3148, #'ㅈ'
                                0x11BE : 0x314A, #'ㅊ'
                                0x11BF : 0x314B, #'ㅋ'
                                0x11C0 : 0x314C, #'ㅌ'
                                0x11C1 : 0x314D, #'ㅍ'
                                0x11C2 : 0x314E  #'ㅎ'
                                }
                                # orphaned jamo flag
                                #0x115F : 0x3164 # hangul filler

COMPAT_TO_JAMO_LOOKUP_CHOSEONG = {v:k for k,v in JAMO_TO_COMPAT_LOOKUP_CHOSEONG.items()}
COMPAT_TO_JAMO_LOOKUP_JUNGSEONG = {v:k for k,v in JAMO_TO_COMPAT_LOOKUP_JUNGSEONG.items()}
COMPAT_TO_JAMO_LOOKUP_JONGSEONG = {v:k for k,v in JAMO_TO_COMPAT_LOOKUP_JONGSEONG.items()}

# Functions

def decompose_non_compat(text):
    """decomposes Korean text into Hangul Jamo (Ux1100 ~ Ux11FF)

    Args:
        text (str): Korean text

    Returns:
        jamos (str): corresponding Hangul jamo sequence
    """
    
    jamos_list = []
    
    for syll in text:
        if 0xAC00 <= ord(syll) <= 0xD7A3:  # Check if it's a Hangul syllable
            # arithmetic to determine the index of the jamos
            syll_code = ord(syll) - K1
            initial = syll_code // K2
            vowel = (syll_code - (initial * K2)) // K3
            final = (syll_code - (K2 * initial)) - (K3 * vowel)
            
            jamos_list.append(JAMO_DICT['initial'][initial])
            jamos_list.append(JAMO_DICT['vowel'][vowel])
            jamos_list.append(JAMO_DICT['final'][final])
            
        elif 0x1100 <= ord(syll) <= 0x11FF: # check is it's an orphaned jamo
            jamos_list.append(chr(0x115F)) # add Choseong Filler as the signal token for orphaned jamo
            jamos_list.append(syll)
        
        else:
            jamos_list.append(syll)
            
    jamos = ''.join(jamos_list)
    
    return jamos

def jamos_to_syllable(buffer: list):
    # TODO sanity check
    # must be non-compat
    # buffer must be 3/3 filled
    syllable_code = ((JAMO_DICT['initial'].index(buffer[0]) * K2) +
                     (JAMO_DICT['vowel'].index(buffer[1]) * K3) +
                     JAMO_DICT['final'].index(buffer[2]) + K1
                    )
    return chr(syllable_code)

def recompose_non_compat(jamos):
    
    """recomposes a Hangul Jamo (Ux1100 ~ Ux11FF) sequence to Korean text
    
    Args:
        jamos (str): Hangul Jamo sequence

    Returns:
        text (str): corresponding human-readable Korean text
    """
    
    text = ""
    buffer = ['','','']
    orphaned_jamo = False
    
    for jamo in jamos:
        if orphaned_jamo:
            text += jamo
            orphaned_jamo = False # reset flag for orphaned jamo
        elif jamo in JAMO_DICT['initial']:
            buffer[0] = jamo
        elif jamo in JAMO_DICT['vowel']:
            buffer[1] = jamo
        elif jamo in JAMO_DICT['final']:
            buffer[2]= jamo
            
            syll = jamos_to_syllable(buffer)
            text += syll
            buffer = ['','','']
            
        elif ord(jamo) == 0x115F: # flag for orphaned jamo in next iteration
            orphaned_jamo = True
        else:
            text += jamo # non-jamo characters
    
    return text

def non_compat_to_compat(jamos):
    
    """converts a Hangul Jamo (Ux1100 ~ Ux11FF) sequence to a Hangul Compatibility Jamo (Ux3131 ~ Ux318E) sequence

    Args:
        jamos (str): Hangul Jamo sequence

    Returns:
        compat_jamos (str): corresponding Hangul Compatibility Jamo sequence
    """

    compat_jamos = "" 
    
    for char in jamos:
        if 0x1100 <= ord(char) <= 0x1112: # check if it's a choseong
            compat_jamo = chr(JAMO_TO_COMPAT_LOOKUP_CHOSEONG[ord(char)])
            compat_jamos += compat_jamo
        elif 0x1161 <= ord(char) <= 0x1175: # check if it's a jungseong
            compat_jamo = chr(JAMO_TO_COMPAT_LOOKUP_JUNGSEONG[ord(char)])
            compat_jamos += compat_jamo
        elif 0x11A8 <= ord(char) <= 0x11C2: # check if it's a jongseong
            compat_jamo = chr(JAMO_TO_COMPAT_LOOKUP_JONGSEONG[ord(char)])
            compat_jamos += compat_jamo
        elif ord(char) == 0x115F: # check for orphaned jamo
            compat_jamos += chr(0x3164) # substitute for filler
        elif ord(char) == 0x11FF: # check for SSANGNIEUN (indicates a <nil> jongseong)
            compat_jamos += chr(0x3165) # substitute for SSANGNIEUN chr(0x3165)
        else: # non-jamo characters
            compat_jamos += char
        
    return compat_jamos

def decompose_compat(text):
    
    """_summary_
    
    Args:
        text (str): Korean text 

    Returns:
        compat_jamos (str): corresponding Hangul Compatibility Jamo sequence
    """
    
    # get jamo seq from decompose(), and apply jamo_to_compat()
    jamos = decompose_non_compat(text)
    compat_jamos = non_compat_to_compat(jamos)
    return compat_jamos

def recompose_compat(compat_jamos: str):
    
    """Recomposes a human-readable Korean text from a Hangul Compatibility Jamo (Ux3131 ~ Ux318E) sequence

    Args:
        compat_jamos (str): Hangul Compatibility Jamo sequence

    Returns:
        text (str): corresponding Korean text
    """
    # state machine
    # orphaned jamo flag is 0x3164
    state = 0
    buffer = ['','','']
    text = ""
    
    compat_jamos = compat_jamos.replace(chr(0x3165), "")
    
    for c in range(len(compat_jamos)):
        if state == 0: # buffer is empty
            if ord(compat_jamos[c]) in list(COMPAT_TO_JAMO_LOOKUP_CHOSEONG.keys()):
                buffer[0] = chr(COMPAT_TO_JAMO_LOOKUP_CHOSEONG[ord(compat_jamos[c])])
                state = 1
            elif ord(compat_jamos[c]) == 0x3164: # orphaned jamo flag
                state = 3
            else:
                text += compat_jamos[c]
        elif state == 1: # 1/3 filled
            buffer[1] = chr(COMPAT_TO_JAMO_LOOKUP_JUNGSEONG[ord(compat_jamos[c])])
            if c+1 == len(compat_jamos): # end of text
                buffer[2] = chr(0x11FF) # SSANGNIEUN
                syll = jamos_to_syllable(buffer) # compose syllable
                text += syll # add syllable to text
            state = 2
        elif state == 2: # 2/3 filled
            if c+1 == len(compat_jamos): # end of text
                buffer[2] = chr(COMPAT_TO_JAMO_LOOKUP_JONGSEONG[ord(compat_jamos[c])])
                syll = jamos_to_syllable(buffer) # compose syllable
                text += syll # add syllable to text
            elif ord(compat_jamos[c]) in list(COMPAT_TO_JAMO_LOOKUP_CHOSEONG.keys()) and ord(compat_jamos[c+1]) in list(COMPAT_TO_JAMO_LOOKUP_JUNGSEONG.keys()): # if next char in line is a jungseong, then the current jaeum is a choseong
                buffer[2] = chr(0x11FF) # SSANGNIEUN
                syll = jamos_to_syllable(buffer) # compose syllable
                text += syll # add syllable to text
                buffer = ['','',''] # reset buffer
                buffer[0] = chr(COMPAT_TO_JAMO_LOOKUP_CHOSEONG[ord(compat_jamos[c])])
                state = 1
            elif ord(compat_jamos[c]) in list(COMPAT_TO_JAMO_LOOKUP_JONGSEONG.keys()):
                buffer[2] = chr(COMPAT_TO_JAMO_LOOKUP_JONGSEONG[ord(compat_jamos[c])])
                syll = jamos_to_syllable(buffer) # compose syllable
                text += syll # add syllable to text
                buffer = ['','',''] # reset buffer  
                state = 0
            elif ord(compat_jamos[c]) == 0x3164: # orphaned jamo flag
                buffer[2] = chr(0x11FF) # SSANGNIEUN
                syll = jamos_to_syllable(buffer) # compose syllable
                text += syll # add syllable to text
                buffer = ['','',''] # reset buffer
                state = 3
            else: # non korean
                buffer[2] = chr(0x11FF) # SSANGNIEUN
                syll = jamos_to_syllable(buffer) # compose syllable
                text += syll # add syllable to text
                buffer = ['','',''] # reset buffer
                text += compat_jamos[c]
                state = 0
        elif state == 3: # orphaned jamo
            text += compat_jamos[c]
            state = 0
            
    return text

def decompose(text, type):
    if type == "non-compat":
        return decompose_non_compat(text)
    elif type == "compat":
        return decompose_compat(text)
    else:
        raise Exception("arg 'type' should be either 'non-compat' or 'compat'")

def recompose(jamos, type):
    if type == "non-compat":
        return recompose_non_compat(jamos)
    elif type == "compat":
        return recompose_compat(jamos)
    else:
        raise Exception("arg 'type' should be either 'non-compat' or 'compat'")
    
