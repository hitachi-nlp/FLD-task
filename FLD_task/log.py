from typing import Optional, List, Dict, Any
from pprint import pformat

from .proof.utils import prettify_context_text, prettify_proof_text


def log_example(context: Optional[str] = None,
                hypothesis: Optional[str] = None,
                gold_proofs: Optional[List[str]] = None,
                pred_proof: Optional[str] = None,
                metrics: Optional[Dict[str, Any]] = None,
                logger=None):
    gold_proofs = gold_proofs or []

    if logger is not None:
        def log(msg: str, level='info') -> None:
            if level == 'info':
                logger.info(msg)
            elif level == 'warning':
                logger.warning(msg)
            else:
                raise ValueError()
    else:
        def log(msg: str, level='info') -> None:
            if level == 'info':
                print(msg)
            elif level == 'warning':
                print('[!]', msg)
            else:
                raise ValueError()
    log('\n\n\n=========================================== example ===========================================')

    if context is not None:
        log('\n-------------- context        ----------------')
        try:
            log(prettify_context_text(context))
        except Exception as e:
            log('could not prettify context due to the following error:' + '\n' + str(e), level='warning')
            log(context)

    if hypothesis is not None:
        log('\n-------------- hypothesis     ----------------')
        log(hypothesis)

    if len(gold_proofs) > 0:
        for gold_proof in gold_proofs:
            log('\n-------------- gold proof     ----------------')
            try:
                log(prettify_proof_text(gold_proof))
            except Exception as e:
                log('could not prettify context due to the following error:' + str(e), level='warning')
                log(gold_proof)

    if pred_proof is not None:
        log('\n-------------- pred proof     ----------------')
        log(pred_proof)

    if metrics is not None:
        log('\n-------------- metrics        ----------------')
        log(pformat(metrics))
