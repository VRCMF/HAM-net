import pytorch_lightning
import logging
import sys
#sys.path.insert(1, '/../Turku-neural-parser-pipeline/tnparser/pipeline.py')
sys.path.insert(1, '../tools/Turku-neural-parser-pipeline')
import tnparser

from tnparser.pipeline import read_pipelines, Pipeline

# What pipelines do we have for the Finnish model?
available_pipelines=read_pipelines("/../Turku-neural-parser-pipeline/models_fi_tdt_dia/pipelines.yaml")               # {pipeline_name -> its steps}
# This is a dictionary, its keys are the pipelines
#print(list(available_pipelines.keys()))
# Instantiate one of the pipelines
p=Pipeline(available_pipelines["parse_plaintext"])

# COMMAND ----------

txt_in="Saavuin siis kaupunkiin kameraryhmäni kanssa jo ennen yhtätoista."
parsed=p.parse(txt_in)
print(parsed)

# COMMAND ----------

file_txt=""
def lemma_tokens(input_txt):
  origin = []
  lemma = []
  pos = []
  for sent in input_txt.split('.'):
      if len(sent) > 0:
        lemma_tmp = []
        pos_tmp = []
        orig_tmp = []
        parsed=p.parse(sent)
        for i in parsed.split('\n'):
          if len(i) != 0 and i[0] != '#':
            origi_i = i.split('\t')[1].lower()
            lemma_i = i.split('\t')[2]
            pos_tag = i.split('\t')[3]
            orig_tmp.append(origi_i.replace('#', ''))
            lemma_tmp.append(lemma_i.replace('#', ''))
            pos_tmp.append(pos_tag)
        origin.append(orig_tmp)
        lemma.append(lemma_tmp)
        pos.append(pos_tmp)
  # generate annotation mask
  mask = []
  for s_idx in range(len(pos)):
    sent_pos = pos[s_idx]
    sent = lemma[s_idx]
    mask_tmp = []
    print(sent_pos)
    for tok_idx in range(len(sent_pos)):
      if sent_pos[tok_idx] == 'NOUN' or sent_pos[tok_idx] == 'VERB':
        if sent[tok_idx] not in ['mm', 'cm', 'm']:
          mask_tmp.append('T')
        else:
          mask_tmp.append('F')
      else:
        mask_tmp.append('F')
    mask.append(mask_tmp)
    
  return origin, lemma, mask

# COMMAND ----------

ori, lem, mas = lemma_tokens(file_txt)
