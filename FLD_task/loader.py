from typing import Union, Optional
from FLD_task.schema import Deduction


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

        if dic.get('answer', None) is not None:
            dic['world_assump_label'] = convert_answer(dic['answer'])
        if dic.get('negative_answer', None) is not None:
            dic['negative_world_assump_label'] = convert_answer(dic['negative_answer'])

        def convert_stance(stance: str) -> str:
            if stance == 'PROOF':
                return 'PROVED'
            elif stance == 'DISPROOF':
                return 'DISPROVED'
            elif stance == 'UNKNOWN':
                return 'UNKNOWN'
            else:
                raise ValueError(f'Unknown stance {stance}')

        if dic.get('proof_stance', None) is not None:
            dic['proof_label'] = convert_stance(dic['proof_stance'])
        if dic.get('negative_proof_stance', None) is not None:
            dic['negative_proof_label'] = convert_stance(dic['negative_proof_stance'])

    elif version == '0.1':
        dic['world_assump_label'] = dic.get('answer', None)
        dic['negative_world_assump_label'] = dic.get('negative_answer', None)

        dic['proof_label'] = dic.get('proof_stance', None)
        dic['negative_proof_label'] = dic.get('negative_proof_stance', None)

    elif version == '0.2':
        pass

    elif version in ['DeductionInstance', 'DeductionExampleInstance']:
        pass

    else:
        raise ValueError()

    dic['version'] = 'DeductionInstance'
    ex = Deduction.parse_obj({key: val for key, val in dic.items() if val is not None})
    return ex
