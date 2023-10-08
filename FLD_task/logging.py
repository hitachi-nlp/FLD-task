from typing import Optional, List, Dict, Any
from pprint import pformat

from .proof.utils import prettify_facts_text, prettify_proof_text


def log_example(facts: Optional[str] = None,
                hypothesis: Optional[str] = None,
                gold_proofs: Optional[List[str]] = None,
                pred_proof: Optional[str] = None,
                metrics: Optional[Dict[str, Any]] = None,
                logger=None):
    gold_proofs = gold_proofs or []
    log_info_lines: List[str] = []
    log_warn_lines: List[str] = []

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

    log_info_lines.append('\n\n\n=========================================== example ===========================================')

    if facts is not None:
        log_info_lines.append('\n-------------- facts        ----------------')
        try:
            log_info_lines.append(prettify_facts_text(facts))
        except Exception as e:
            log_warn_lines.append('[!] could not prettify the above facts due to the following error:' + '\n' + str(e))
            log_info_lines.append(facts)

    if hypothesis is not None:
        log_info_lines.append('\n-------------- hypothesis     ----------------')
        log_info_lines.append(hypothesis)

    if len(gold_proofs) > 0:
        for gold_proof in gold_proofs:
            log_info_lines.append('\n-------------- gold proof     ----------------')
            try:
                log_info_lines.append(prettify_proof_text(gold_proof))
            except Exception as e:
                log_info_lines.append('[!] could not prettify the gold proof due to the following error:' + str(e))
                log_info_lines.append(gold_proof)

    if pred_proof is not None:
        log_info_lines.append('\n-------------- pred proof     ----------------')
        try:
            log_info_lines.append(prettify_proof_text(pred_proof))
        except Exception as e:
            log_info_lines.append('[!] could not prettify the pred proof due to the following error:' + str(e))
            log_info_lines.append(pred_proof)

    if metrics is not None:
        log_info_lines.append('\n-------------- metrics        ----------------')
        log_info_lines.append(pformat(metrics))

    if len(log_info_lines) > 0:
        log('\n'.join(log_info_lines))
    if len(log_warn_lines) > 0:
        log('\n'.join(log_warn_lines), level='warning')
