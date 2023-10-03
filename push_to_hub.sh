#!/bin/bash



# -- FLD.v2 --
# TEST=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/valid/valid.jsonl
# REPO="hitachi-nlp/FLD.v2"


# -- FLD-star.v2 --
TEST=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/test/test.jsonl
TRAIN=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/train/train.jsonl
VALID=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/valid/valid.jsonl
REPO="hitachi-nlp/FLD-star.v2"


python ./push_to_hub.py\
    --train ${TRAIN}\
    --valid ${VALID}\
    --test ${TEST}\
    --repo-name ${REPO}
