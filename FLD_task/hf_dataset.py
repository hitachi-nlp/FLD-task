from typing import List, Dict, Any, Optional
from copy import deepcopy
from typing import Dict, List, Any

from FLD_task import Deduction, load_deduction, serialize


def serialize_transform(examples: Dict[str, List[Any]],
                        split: str,
                        proof_sampling: Optional[str] = 'stepwise',
                        sample_negative_proof=False) -> Dict[str, List[Any]]:
    """
    how to use:

        dataset.set_transform(
            lambda examples: transform(examples, 'train', ...)
        )
    """
    if split == 'train':
        if proof_sampling == 'stepwise':
            do_stepwise = True
        elif proof_sampling == 'all_at_once':
            do_stepwise = False
        else:
            raise ValueError()
        examples = _add_serials_train(
            examples,
            stepwise=do_stepwise,
            sample_negative_proof=sample_negative_proof,
        )
    elif split == 'eval':
        examples = _add_serials_eval(examples)
    else:
        raise ValueError()

    return examples


def _add_serials_train(batch_examples: Dict[str, List[Any]],
                       stepwise=False,
                       sample_negative_proof=False) -> Dict[str, List[Any]]:
    return _add_serials(batch_examples, stepwise, sample_negative_proof=sample_negative_proof)


def _add_serials_eval(batch_examples: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
    return _add_serials(batch_examples, False)


def _add_serials(batch_examples: Dict[str, List[Any]],
                 stepwise: bool,
                 sample_negative_proof=False) -> Dict[str, List[Any]]:
    keys = list(batch_examples.keys())
    n_examples = len(batch_examples[keys[0]])

    examples: List[Deduction] = []
    for i_example in range(0, n_examples):
        examples.append(
            load_deduction({
                key: batch_examples[key][i_example]
                for key in keys
            })
        )

    serialized_examples = [
        serialize(_example,
                  stepwise=stepwise,
                  sample_negative_proof=sample_negative_proof)
        for _example in examples
    ]

    preprocessed_batch_examples = deepcopy(batch_examples)
    preprocessed_batch_examples['context'] = [
        serialized_examples[i_example].input
        for i_example in range(0, len(examples))
    ]
    preprocessed_batch_examples['next_step'] = [
        serialized_examples[i_example].next_step
        for i_example in range(0, len(examples))
    ]

    for serial in serialized_examples:
        if len(serial.gold_proofs) >= 2:
            raise NotImplementedError()
    preprocessed_batch_examples['gold_proof'] = [
        serialized_examples[i_example].gold_proofs[0] if len(serialized_examples[i_example].gold_proofs) > 0 else None
        for i_example in range(0, len(examples))
    ]

    return preprocessed_batch_examples
