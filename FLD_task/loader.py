import re
from typing import Union, Optional, Callable, Any
from FLD_task.schema import Deduction
from FLD_task.proof.utils import FACT_IDENT, FACTS_IDENT


def load_deduction(dic: dict, force_version: str = None) -> Deduction:
    if force_version is not None:
        version = force_version
    else:
        version = dic.get('version', None)
        version = version or dic.get('__version__', None)  # back compatibility
        version = version or force_version
        # if force_version is not None and force_version != version:
        #     raise ValueError(f'the forced version {force_version} does not match the found version {version}')
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

    elif version in ['DeductionInstance', 'DeductionExampleInstance']:
        pass

    else:
        raise ValueError()

    dic['version'] = 'DeductionInstance'
    init_kwargs = {key: val for key, val in dic.items() if val is not None}

    # We could check the unnecessary fields,
    # but it could be useful if we ignore such fields when we are loading examples from 
    # modified jsons or something.
    # for key in init_kwargs:
    #     if key not in Deduction.schema()['properties']:
    #         raise Exception(f'key={key} not allowed for Deduction object')

    return Deduction.parse_obj(init_kwargs)
