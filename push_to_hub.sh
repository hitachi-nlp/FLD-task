#!/bin/bash





# XXX README!!! Before pushing to hub, be sure to checkout the version that match the remote repo,
# as the push script add some features to the dataset.

# TEST=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D3/trnsltn_adj_vrb_nn_rt=1-1-1/valid/valid.jsonl
# REPO="hitachi-nlp/FLD.v2"
# CONFIG_NAME="default"


# TEST=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230801.case_study_finalize.fix/dataset_name=20230729.case_study_finalize.D8/trnsltn_adj_vrb_nn_rt=1-1-1/valid/valid.jsonl
# REPO="hitachi-nlp/FLD.v2"
# CONFIG_NAME="star"








# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD"
# CONFIG_NAME="D1_minus"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD"
# CONFIG_NAME="D1"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD"
# CONFIG_NAME="D3"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.wordnet_repro_wo_proposition.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=False/trnsltn_vcb=wordnet/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD"
# CONFIG_NAME="D8"







 
# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_BCCWJ"
# CONFIG_NAME="D1_minus"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_BCCWJ"
# CONFIG_NAME="D1"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_BCCWJ"
# CONFIG_NAME="D3"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.BCCWJ.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=BCCWJ/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_BCCWJ"
# CONFIG_NAME="D8"








# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D1_wo_dist/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_punipuni_monster"
# CONFIG_NAME="D1_minus"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D1/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_punipuni_monster"
# CONFIG_NAME="D1"


# TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/test/test.jsonl
# TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/train/train.jsonl
# VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D3/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/valid/valid.jsonl
# REPO="hitachi-nlp/JFLD_punipuni_monster"
# CONFIG_NAME="D3"


TEST=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/test/test.jsonl
TRAIN=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/train/train.jsonl
VALID=./outputs.FLD/00.create_corpus/20230120.jpn.punipuni/dataset_name=20230120.jpn.punipuni.D8/cntxt_shffls_pr_instnc=1/knwldg_argmnt_fctr=1.0/smpl_all_stncs_pr_lgc=False/trnsltn_adj_vrb_nn_rt=1-1-1/trnsltn_n_trnstv_objct=True/trnsltn_vcb=punipuni/valid/valid.jsonl
REPO="hitachi-nlp/JFLD_punipuni_monster"
CONFIG_NAME="D8"








# ------------- push now! ------------
python ./push_to_hub.py\
    --train ${TRAIN}\
    --valid ${VALID}\
    --test ${TEST}\
    --repo-id ${REPO}\
    --config-name ${CONFIG_NAME}
