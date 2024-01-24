import re
from copy import copy
import logging

from pydantic.error_wrappers import ValidationError
from typing import Union, Optional, Callable, Any

from FLD_task.schema import Deduction
from FLD_task.proof.utils import FACT_IDENT, FACTS_IDENT

logger = logging.getLogger(__name__)


_NUMBERD_VERSIONS = ['0.0', '0.1', '0.2', '0.3']


def load_deduction(dic: dict, force_version: str = None) -> Deduction:
    dic = copy(dic)
    if force_version is not None:
        version = force_version
    else:
        version = dic.get('version', None)
        version = version or '0.0'

    def map_to_new_field(old_name: str,
                         new_name: str,
                         convert_func: Optional[Callable[[Any], Any]] = None):
        if old_name in dic:
            old_val = dic.pop(old_name, None)
            if old_val is not None:
                old_val_conv = convert_func(old_val) if convert_func is not None else old_val
                if new_name in dic and dic[new_name] != old_val_conv:
                    raise ValueError('inconsistent')
                dic[new_name] = old_val_conv

    def rename_fact_ident(rep: str) -> str:
        return re.sub(r'sent([0-9]+)', f'{FACT_IDENT}\g<1>', rep)

    if version in _NUMBERD_VERSIONS:

        if version in ['0.0', '0.1', '0.2']:

            map_to_new_field('context', f'{FACTS_IDENT}', convert_func=rename_fact_ident)
            map_to_new_field('context_formula', f'{FACTS_IDENT}_formula', convert_func=rename_fact_ident)
            map_to_new_field('proofs', 'proofs', convert_func = lambda proofs: [rename_fact_ident(p) for p in proofs])
            map_to_new_field('proofs_formula', 'proofs_formula', convert_func = lambda proofs: [rename_fact_ident(p) for p in proofs])
            map_to_new_field('negative_proofs', 'negative_proofs', convert_func = lambda proofs: [rename_fact_ident(p) for p in proofs])
            map_to_new_field('negative_proofs_formula', 'negative_proofs_formula', convert_func = lambda proofs: [rename_fact_ident(p) for p in proofs])

            if version in ['0.0', '0.1']:
                if version == '0.0':
                    def convert_answer(ans: Union[bool, str]) -> str:
                        if ans is True:
                            return 'PROVED'
                        elif ans is False:
                            return 'DISPROVED'
                        elif ans == 'Unknown':
                            return 'UNKNOWN'
                        else:
                            raise ValueError(f'Unknown answer {ans}')

                    def convert_stance(stance: str) -> str:
                        if stance == 'PROOF':
                            return 'PROVED'
                        elif stance == 'DISPROOF':
                            return 'DISPROVED'
                        elif stance == 'UNKNOWN':
                            return 'UNKNOWN'
                        else:
                            raise ValueError(f'Unknown stance {stance}')
                elif version == '0.1':
                    convert_answer = None
                    convert_stance = None
                else:
                    raise ValueError()

                map_to_new_field('answer', 'world_assump_label', convert_func=convert_answer)
                map_to_new_field('negative_answer', 'negative_world_assump_label', convert_func=convert_answer)

                map_to_new_field('proof_stance', 'proof_label', convert_func=convert_stance)
                map_to_new_field('negative_proof_stance', 'negative_proof_label', convert_func=convert_stance)

            elif version == '0.2':
                pass

            else:
                raise Exception()

        elif version in ['0.3']:
            pass

        else:
            raise ValueError(f'Unknown version {version}')

    elif version in ['DeductionInstance', 'DeductionExampleInstance']:

        # Guess the original version before loaded as DeductionInstance
        version_guess_deduction = None
        for possible_versions in sorted(_NUMBERD_VERSIONS)[::-1]:
            try:
                version_guess_deduction = load_deduction(dic, force_version=possible_versions)
                break
            except ValidationError as e:
                # logger.info(f'Failed to load deduction as version {possible_versions} with the following error:\n{e}')
                pass
        if version_guess_deduction is None:
            raise ValueError('Failed to load deduction as any of the versions')
        else:
            # logger.info(f'Successfully loaded deduction as version {possible_versions}')
            dic = version_guess_deduction.dict()

    else:
        raise ValueError()

    dic['version'] = 'DeductionInstance'
    init_kwargs = {key: val for key, val in dic.items() if val is not None}

    deduction = Deduction.parse_obj(init_kwargs)
    return deduction

