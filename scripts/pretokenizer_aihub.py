from jamo_utils import decompose
from sacrebleu.tokenizers.tokenizer_intl import TokenizerV14International

from pathlib import Path

def remove_space(text: str):
    return text.replace(' ', '')
    
def remove_special_char(text: str):\
    return text.replace(chr(9603), ' ')

def main() -> None:  # pylint: disable=redefined-outer-name
    pre_tokenizer = TokenizerV14International() # space-separated punctuation
    raw_path = "../../data/aihub_en-ko/processed/data/raw/"
    dest_path = "../../data/aihub_en-ko/processed/data/spaced/"
    lang = "ko"
    
    for split in ["train","test","dev"]:

        with open(Path(raw_path, f"{split}.{lang}")) as f:
            text = f.readlines()
        for type in ["compat"]:
            for i in range(len(text)):
                # insert space between text and regex
                orig_text = pre_tokenizer(text[i])
                if type == "syllable":
                    text[i] = orig_text
                else:
                    jamos = decompose(orig_text, type)
                    text[i] = jamos
                    
                    # to check if lossless
                    
                    # recomposed_text = recompose(decompose(orig_text, type), type) 
                    # if orig_text == recomposed_text:
                    #     text[i] = jamos
                    # else:
                    #     print(f"error at line {i+1} of {split}.{lang} while decomposing into {type}")
                    #     print(f"original text: {orig_text}")
                    #     print(f"recomposed text: {recomposed_text}")
                    #     break
                
            with open(Path(dest_path, "compat_f", f"{split}.{lang}"), "x+") as f:
                f.writelines('\n'.join(text))
            print(f"compat_f {split}.{lang} completed with no errors") 
            

if __name__ == "__main__":
    main()
