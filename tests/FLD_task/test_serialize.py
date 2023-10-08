from typing import Dict, Any, List, Optional, Set
from pprint import pprint

from FLD_task.serializer import (
    serialize,
    _splice_negative_proof,
    _random_splice,
    _rename_ints_with_offset,
    _rename_ints_ascending,
    _get_lowest_int_no,
)
from FLD_task.schema import Deduction, SerializedDeduction
from FLD_task import load_deduction


def test_serialize_example():

    def test_one_example(input_example: Deduction,
                         gold_examples: List[SerializedDeduction],
                         trial=10000,
                         **kwargs):

        print('\n\n\n')
        print(f'=================== _test_one_example() {kwargs} ==================')

        print('\n------------    input_example   ------------')
        pprint(input_example.dict())

        serialized_examples = [serialize(input_example, **kwargs)
                               for _ in range(trial)]

        def get_matched_gold(serialized_example: SerializedDeduction) -> Optional[SerializedDeduction]:
            for gold_example in gold_examples:
                if serialized_example.prompt == gold_example.prompt\
                        and serialized_example.partial_proof == gold_example.partial_proof\
                        and serialized_example.next_proof_step == gold_example.next_proof_step:
                    return gold_example
            return None

        generated_golds: Set[int] = set([])
        for serialized_example in serialized_examples:
            matched_gold = get_matched_gold(serialized_example)

            if matched_gold is None:
                for i_gold, gold_example in enumerate(gold_examples):
                    print('')
                    print(f'------------       gold-{i_gold}         ------------')
                    pprint(gold_example.dict())

                print('\n\n------------ serialized example not found in the golds ------------')
                pprint(serialized_example.dict())

                assert False
            else:
                generated_golds.add(id(matched_gold))

        not_generated_golds = [gold_example for gold_example in gold_examples
                               if id(gold_example) not in generated_golds]

        if len(not_generated_golds) > 0:
            print('\n\n------------------- not found golds ------------------')
            for generated_gold in not_generated_golds:
                pprint(generated_gold.dict())
            assert False

    def _load_deduction(*args, **kwargs) -> Deduction:
        return load_deduction(*args, **kwargs, force_version='DeductionInstance')

    hypothesis = 'this is the hypothesis'
    context = 'fact1: this is sentence1 fact2: this is sentence2 fact3: this is sentence3 fact4: this is sentence4 fact5: this is sentence5'
    proof = 'fact1 & fact2 -> int1: first conclusion; fact3 & int1 -> int2: second conclusion;'
    negative_proof = 'fact4 & fact5 -> int1: first negative conclusion; fact3 & int1 -> int2: second negative conclusion;'

    test_one_example(
        _load_deduction({
            'hypothesis': hypothesis,
            'context': context,

            'proofs': [proof],
            'world_assump_label': 'PROVED',

            'negative_proofs': [negative_proof],
        }),
        [
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': None,
                'next_proof_step': proof + ' __PROVED__',
            }),
        ],
        stepwise=False,
        sample_negative_proof=False,
    )

    test_one_example(
        _load_deduction({
            'hypothesis': hypothesis,
            'context': context,

            'proofs': [proof],
            'world_assump_label': 'PROVED',

            'negative_proofs': [negative_proof],
        }),
        [
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': None,
                'next_proof_step': 'fact1 & fact2 -> int1: first conclusion;',
            }),
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': 'fact1 & fact2 -> int1: first conclusion;',
                'next_proof_step': 'fact3 & int1 -> int2: second conclusion; __PROVED__',
            }),

        ],
        stepwise=True,
        sample_negative_proof=False,
    )

    test_one_example(
        _load_deduction({
            'hypothesis': hypothesis,
            'context': context,

            'proofs': [proof],
            'world_assump_label': 'PROVED',

            'negative_proofs': [negative_proof],
        }),
        [
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': None,
                'next_proof_step': 'fact4 & fact5 -> int1: first negative conclusion; fact3 & int1 -> int2: second negative conclusion; fact1 & fact2 -> int3: first conclusion; fact3 & int3 -> int4: second conclusion; __PROVED__'
            }),
        ],
        stepwise=False,
        sample_negative_proof=True,
    )

    test_one_example(
        _load_deduction({
            'hypothesis': hypothesis,
            'context': context,

            'proofs': [proof],
            'world_assump_label': 'PROVED',

            'negative_proofs': [negative_proof],
        }),
        [
            # p1
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': None,
                'next_proof_step': 'fact1 & fact2 -> int1: first conclusion;'
            }),

            # p1 p2
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact1 & fact2 -> int1: first conclusion;',
                'next_proof_step': 'fact3 & int1 -> int2: second conclusion; __PROVED__'
            }),

            # p1 n1
            # SerializedDeduction.parse_obj({
            #     'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
            #     'partial_proof':'fact1 & fact2 -> int1: first conclusion;',
            #     'next_proof_step': 'fact4 & fact5 -> int2: first negative conclusion;'
            # }),

            # p1 n1 p2
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': 'fact1 & fact2 -> int1: first conclusion; fact4 & fact5 -> int2: first negative conclusion;',
                'next_proof_step': 'fact3 & int1 -> int3: second conclusion; __PROVED__'
            }),

            # p1 n1 n2
            # SerializedDeduction.parse_obj({
            #     'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
            #     'partial_proof': 'fact1 & fact2 -> int1: first conclusion; fact4 & fact5 -> int2: first negative conclusion;',
            #     'next_proof_step': 'fact3 & int2 -> int3: second negative conclusion;'
            # }),

            # p1 n1 n2 p2
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact1 & fact2 -> int1: first conclusion; fact4 & fact5 -> int2: first negative conclusion; fact3 & int2 -> int3: second negative conclusion;',
                'next_proof_step': 'fact3 & int1 -> int4: second conclusion; __PROVED__'
            }),




            # n1
            # SerializedDeduction.parse_obj({
            #     'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
            #     'partial_proof': None,
            #     'next_proof_step': 'fact4 & fact5 -> int1: first negative conclusion;'
            # }),

            # n1 p1
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact4 & fact5 -> int1: first negative conclusion;',
                'next_proof_step': 'fact1 & fact2 -> int2: first conclusion;'
            }),

            # n1 p1 p2
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact4 & fact5 -> int1: first negative conclusion; fact1 & fact2 -> int2: first conclusion;',
                'next_proof_step': 'fact3 & int2 -> int3: second conclusion; __PROVED__'
            }),

            # n1 p1 n2
            # SerializedDeduction.parse_obj({
            #     'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = fact4 & fact5 -> int1: first negative conclusion; fact1 & fact2 -> int2: first conclusion;',
            #     'partial_proof': None,
            #     'next_proof_step': 'fact3 & int1 -> int3: second negative conclusion;'
            # }),

            # n1 p1 n2 p2
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact4 & fact5 -> int1: first negative conclusion; fact1 & fact2 -> int2: first conclusion; fact3 & int1 -> int3: second negative conclusion;',
                'next_proof_step': 'fact3 & int2 -> int4: second conclusion; __PROVED__'
            }),

            # n1 n2
            # SerializedDeduction.parse_obj({
            #     'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
            #     'partial_proof':'fact4 & fact5 -> int1: first negative conclusion;',
            #     'next_proof_step': 'fact3 & int1 -> int2: second negative conclusion;'
            # }),

            # n1 n2 p1
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact4 & fact5 -> int1: first negative conclusion; fact3 & int1 -> int2: second negative conclusion;',
                'next_proof_step': 'fact1 & fact2 -> int3: first conclusion;'
            }),

            # n1 n2 p1 p2
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof':'fact4 & fact5 -> int1: first negative conclusion; fact3 & int1 -> int2: second negative conclusion; fact1 & fact2 -> int3: first conclusion;',
                'next_proof_step': 'fact3 & int3 -> int4: second conclusion; __PROVED__'
            }),


        ],

        stepwise=True,
        sample_negative_proof=True,
    )

    test_one_example(
        _load_deduction({
            'hypothesis': hypothesis,
            'context': context,

            'proofs': [proof],
            'world_assump_label': 'UNKNOWN',

            'negative_proofs': [negative_proof],
        }),
        [
            SerializedDeduction.parse_obj({
                'prompt': f'$hypothesis$ = {hypothesis} ; $context$ = {context} ; $proof$ = ',
                'partial_proof': None,
                'next_proof_step': '__UNKNOWN__',
            }),
        ],
        stepwise=False,
        sample_negative_proof=False,
        include_max_subproof_for_unknown=False,
    )


def test_splice_negative_proof():
    proof = 'fact1 -> int1: hoge; fact2 & int1 -> int2: fuga;'
    negative_proof = 'fact3 -> int1: negative hoge; fact2 & int1 -> int2: negative fuga;'

    for _ in range(0, 100):
        spliced_proof = _splice_negative_proof(
            proof,
            negative_proof,
        )
        assert spliced_proof in [
            'fact1 -> int1: hoge; fact3 -> int2: negative hoge; fact2 & int2 -> int3: negative fuga; fact2 & int1 -> int4: fuga;',
            'fact3 -> int1: negative hoge; fact1 -> int2: hoge; fact2 & int1 -> int3: negative fuga; fact2 & int2 -> int4: fuga;',
            'fact3 -> int1: negative hoge; fact2 & int1 -> int2: negative fuga; fact1 -> int3: hoge; fact2 & int3 -> int4: fuga;',
        ]


def test_random_splice():

    these = ['a', 'b',]
    those = ['A', 'B',]
    golds = [
        ['a', 'b', 'A', 'B'],
        ['a', 'A', 'b', 'B'],
        ['a', 'A', 'B', 'b'],
        ['A', 'a', 'b', 'B'],
        ['A', 'a', 'B', 'b'],
        ['A', 'B', 'a', 'b'],
    ]

    def is_same(these, those) -> bool:
        if len(these) != len(those):
            return False
        return all(this == that for this, that in zip(these, those))

    for _ in range(0, 1000):
        spliced = _random_splice(these, those)
        assert any(is_same(spliced, gold) for gold in golds)


def test_rename_ints_with_offset():
    assert _rename_ints_with_offset('fact1 -> int1: hoge; fact2 -> int2: fuga;', 3) == 'fact1 -> int3: hoge; fact2 -> int4: fuga;'
    assert _rename_ints_with_offset('fact1 -> int2: hoge; fact2 -> int1: fuga;', 3) == 'fact1 -> int4: hoge; fact2 -> int3: fuga;'
    assert _rename_ints_with_offset('fact1 -> int1: hoge; fact2 -> int2: fuga; fact3 -> int10: piyo;', 3) == 'fact1 -> int3: hoge; fact2 -> int4: fuga; fact3 -> int12: piyo;'
    assert _rename_ints_with_offset('fact1 -> int1: hoge; fact2 -> int2: fuga; fact3 & int1 -> int10: piyo;', 3) == 'fact1 -> int3: hoge; fact2 -> int4: fuga; fact3 & int3 -> int12: piyo;'


def test_rename_ints_ascending():
    print(_rename_ints_ascending('fact1 -> int100: hoge; int100 & int2 -> int7: fuga;'))
    assert _rename_ints_ascending('fact1 -> int100: hoge; int100 & int2 -> int7: fuga;') == 'fact1 -> int1: hoge; int1 & int2 -> int3: fuga;'


def test_get_lowest_int_no():
    assert _get_lowest_int_no('int2: hoge int3: fuga') == 2
    assert _get_lowest_int_no('') == 1


if __name__ == '__main__':
    test_serialize_example()
    test_rename_ints_with_offset()
    test_rename_ints_ascending()
    test_splice_negative_proof()
    test_get_lowest_int_no()
    test_random_splice()
