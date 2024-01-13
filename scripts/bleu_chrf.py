import jamo_utils
from sacrebleu import BLEU, CHRF

filename = "models/compat_f_test_big_6551_en6k/predictions.test"
ref_file = "../../data/aihub_en-ko/processed/data/spaced/compat_f/test.ko"

vocab_type = "compat" # "syllable" or "positional" or "compat"

hyps = []
invalid_ids = []
invalid_count = 0
with open(filename) as file:
    for line in file:
        if vocab_type == "syllable":
            tmp = jamo_utils.decompose_compat(line.rstrip())
            
        elif vocab_type == "positional":
            try:
                _ = jamo_utils.recompose_positional(line.rstrip())
            except:
                invalid_count += 1
                
            tmp = jamo_utils.positional_to_compat(line.rstrip())
            
        elif vocab_type == "compat":
            try:
                _ = jamo_utils.recompose_compat(line.rstrip())
            except:
                invalid_count += 1
                
            tmp = line.rstrip()
        # try:
        #     tmp = jamo_utils.decompose_compat(line.rstrip())
        # except:
        #     tmp = line.rstrip()
        #     print(len(hyps))
        #     invalid_ids.append(len(hyps))
        #     invalid_count+=1
        # print(tmp)
        hyps.append(tmp)  
        
refs = []
with open(ref_file) as file:
    for line in file:
        refs.append(line.rstrip())
        # if len(refs) == 5:
        #     break

# new_hyps = [hyps[i] for i in invalid_ids]
# new_refs = [refs[i] for i in invalid_ids]

        
print("invalid: ",invalid_count)

# bleu
bleu = BLEU(tokenize="none", lowercase=True)
bleu_score = bleu.corpus_score(hypotheses=hyps, references=[refs]).score
print("bleu: ", bleu_score)

# sacrebleu signature
print(bleu.get_signature())

# chrf
chrf = CHRF(lowercase=True, char_order=18)
chrf_score = chrf.corpus_score(hypotheses=hyps, references=[refs]).score
print("chrf: ",chrf_score)

# sacrebleu signature
print(chrf.get_signature())