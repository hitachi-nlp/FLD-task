#!/bin/bash

# XXX README!!! Before pushing to hub, be sure to checkout the version that match the remote repo,
# as the push script add some features to the dataset.

# -- FLD.v2 --
# TEST=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/valid/valid.jsonl
# REPO="hitachi-nlp/FLD.v2"
# CONFIG_NAME="default"


# -- FLD-star.v2 --
TEST=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/test/test.jsonl
TRAIN=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/train/train.jsonl
VALID=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/valid/valid.jsonl
REPO="hitachi-nlp/FLD.v2"
CONFIG_NAME="star"


python ./push_to_hub.py\
    --train ${TRAIN}\
    --valid ${VALID}\
    --test ${TEST}\
    --repo-id ${REPO}\
    --config-name ${CONFIG_NAME}
