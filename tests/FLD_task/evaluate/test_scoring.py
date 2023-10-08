import math
import re
import logging

from FLD_task.evaluation import _compute_proof_score, _F_score


def _calc_score(gold: str, pred: str, *args, **kwargs) -> float:
    return _compute_proof_score(
        re.sub('  *', ' ', gold),
        re.sub('  *', ' ', pred),
        *args,
        **kwargs,
    )


def test_calc_score_on_toy_examples():
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',

            'fact4 & fact7 -> int5: this is wrong sentence A',
            'int5 & int8 -> int9: this is wrong sentence B',
        ]),

        zero_one=True,
    )
    assert math.isclose(score, 0.0)

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',

            'fact4 & fact7 -> int5: this is wrong sentence A',
            'int5 & int8 -> int9: this is wrong sentence B',
        ]),

        zero_one=True,
        allowed_additional_proof_steps=1,
    )
    assert math.isclose(score, 0.0)

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',

            'fact4 & fact7 -> int5: this is wrong sentence A',
            'int5 & int8 -> int9: this is wrong sentence B',
        ]),

        zero_one=True,
        allowed_additional_proof_steps=2,
    )
    assert math.isclose(score, 1.0)

    # prediction lacks steps
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int2 & int4 -> hypothesis;',
        ]),

        zero_one=True,
    )
    assert (score == 0.0)

    # prediction have irrelevant steps + zero_one=False
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',

            'fact4 & fact7 -> int5: this is wrong sentence A',
            'int5 & int8 -> int9: this is wrong sentence B',
        ]),

        zero_one=False,
    )
    assert (math.isclose(score, _F_score(5, 5, 2)[-1]))

    # prediction lacks steps + zero_one=False
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',

            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
        ]),

        zero_one=False,
    )
    assert (math.isclose(score, _F_score(5, 3, 0)[-1]))

    # prediction is perfect
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',
            'int2 & int4 -> hypothesis;',
        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    # The tree structure is corret. sntence content is wrong.
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',

            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',

            'int1 -> int4: this is a sentence D',
            'int3 -> int2: this is a sentence C',

            'int2 & int4 -> hypothesis;',
        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    # facts reordering of the previous example
    score = _calc_score(
        '; '.join([
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',

            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'int1 -> int4: this is a sentence D',
            'int3 -> int2: this is a sentence C',

            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',

            'int2 & int4 -> hypothesis;',
        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    # prediction is perfect
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',

            'int2 & int4 -> hypothesis',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',

            'int2 & int4 -> hypothesis',

        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'int2 & int4 -> hypothesis',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'int2 & int4 -> hypothesis',

        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'void -> assump2: fuga',
            '[assump2] & fact8 -> int6: fuga',

            'int2 & int4 -> hypothesis',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'void -> assump2: fuga',
            '[assump2] & fact8 -> int5: fuga',

            'int2 & int4 -> hypothesis',

        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'void -> assump2: fuga',
            '[assump2] & fact8 -> int6: fuga',

            'int2 & int4 -> hypothesis',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump2: hoge',
            '[assump2] & fact7 -> int5: hoge',

            'void -> assump1: fuga',
            '[assump1] & fact8 -> int6: fuga',

            'int2 & int4 -> hypothesis',

        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'void -> assump2: fuga',
            '[assump2] & fact8 -> int6: fuga',

            'int2 & int4 -> hypothesis',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact8 -> int6: fuga',

            'void -> assump2: fuga',
            '[assump2] & fact7 -> int5: hoge',

            'int2 & int4 -> hypothesis',

        ]),

        zero_one=True,
    )
    assert (math.isclose(score, 0.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact7 -> int5: hoge',

            'void -> assump2: fuga',
            '[assump2] & fact8 -> int6: fuga',

            'int2 & int4 -> hypothesis',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A',
            'fact2 & fact6 -> int3: this is a sentence B',
            'int1 -> int2: this is a sentence C',
            'int3 -> int4: this is a sentence D',

            'void -> assump1: hoge',
            '[assump1] & fact8 -> int6: fuga',

            'void -> assump2: fuga',
            '[assump2] & fact7 -> int5: hoge',

            'int2 & int4 -> hypothesis',

        ]),

        zero_one=False,
    )
    assert (math.isclose(score, _F_score(9, 7, 2)[-1]))

    score = _calc_score(
        '; '.join([
            'fact1 & fact2 -> hypothesis',
        ]),
        '; '.join([
            'fact1 -> int1: this is a sentence A',
            'fact2 -> int2: this is a sentence B',
            'int1 & int2 -> hypothesis'
        ]),
        zero_one=True,
        allow_reference_step=True,
        facts='fact1: this is a sentence A fact2: this is a sentence B'
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact2 -> hypothesis',
        ]),
        '; '.join([
            'fact1 -> int1: this is a sentence A',
            'fact2 -> int2: this is a sentence B',
            'int1 & int2 -> hypothesis'
        ]),
        zero_one=True,
        allow_reference_step=True,
        facts='fact1: this is a sentence A fact2: this is a sentence B'
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        '; '.join([
            'fact1 & fact2 -> int1: hoge',
            'int1 & fact3 -> hypothesis',
        ]),
        '; '.join([
            'fact1 -> int1: this is a sentence A',
            'int1 & fact2 -> int2: hoge',
            'int2 & fact3 -> hypothesis',
        ]),
        zero_one=True,
        allow_reference_step=True,
        facts='fact1: this is a sentence A'
    )
    assert (math.isclose(score, 1.0))


def test_calc_score_on_real_examples():
    # the actual gold and precisions from our dataset
    score = _calc_score(
        'fact3 & fact5 -> int1: a tempter that is chauvinistic and does not single results in a stagflation that substantiates; fact6 & fact1 -> int2: a tempter does not single and is chauvinistic; int1 & int2 -> int3: a stagflation substantiates; int3 -> hypothesis;',

        'fact6 & fact1 -> int1: a tempter does not single and is chauvinistic; fact5 & fact3 -> int2: a tempter that is not single and is chauvinistic leads to a stagflation that substantiates; int2 & int1 -> int3: a stagflation substantiates; int3 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact3 & fact2 -> int1: that that a irruption occurs is not the fact leads to a abidance; fact5 -> int2: if a abidance occurs, then it is wrong that either a kickoff occurs or a ricochet occurs or both; int1 & int2 -> int3: if it is wrong that a irruption occurs, then it is not the fact that either a kickoff occurs or a ricochet occurs or both; fact6 & fact1 -> int4: if it is not true that a layout occurs, then either a kickoff occurs or a ricochet occurs or both; int4 -> int5: if it is wrong that either a kickoff occurs or a ricochet occurs or both, then a layout occurs; int3 & int5 -> hypothesis;',

        'fact2 & fact3 -> int1: that that a irruption occurs is not true results in a abidance; fact5 -> int2: if a abidance occurs, then it is wrong that either a kickoff occurs or a ricochet occurs or both; int1 & int2 -> int3: if it is wrong that a irruption occurs, then it is not true that either a kickoff occurs or a ricochet occurs or both; fact6 & fact1 -> int4: that that a layout occurs is not true results in that either a kickoff occurs or a ricochet occurs or both; int4 -> int5: if it is wrong that either a kickoff occurs or a ricochet occurs or both, then a layout occurs; int5 & int3 -> hypothesis;',

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact6 & fact1 -> int1: if a telencephalon either finds or is serviceable or both, then it is wrong that a curbstone leaks; fact2 & fact3 -> int2: if it is wrong that a curbstone leaks, then it is wrong that a television smashes; int1 & int2 -> int3: if a telencephalon either finds or is serviceable or both, then it is not the fact that a television smashes; fact7 -> int4: a telencephalon finds; int4 -> int5: a telencephalon either finds or is serviceable or both; int3 & int5 -> hypothesis;',

        'fact7 -> int1: a telencephalon finds; int1 -> int2: a telencephalon either finds or is serviceable or both; fact1 & fact6 -> int3: if a telencephalon either finds or is serviceable or both, then it is not true that a curbstone leaks; fact2 & fact3 -> int4: if it is wrong that a curbstone leaks, then it is not the fact that a television smashes; int4 & int3 -> int5: a telencephalon that either finds or is serviceable or both leads to a television that does not smash; int5 & int2 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact8 & fact7 -> int1: if a conceptualization occurs, then it is not true that a flap and a return do not occur; fact3 & int1 -> int2: if a reduplication does not occur, then it is not true that a flap and a return do not occur; fact4 & fact5 -> int3: a confutation or a babysitting or both leads to that that a reduplication occurs is wrong; fact9 -> int4: either a confutation occurs or a babysitting occurs or both; int3 & int4 -> int5: it is not true that a reduplication occurs; int2 & int5 -> hypothesis;',

        'fact9 -> int1: either a confutation occurs or a babysitting occurs or both; fact8 & fact7 -> int2: if a conceptualization occurs, then it is not the fact that a flap and a return do not occur; fact4 & fact5 -> int3: a confutation or a babysitting or both causes that that a reduplication occurs is not the fact; fact3 & int1 -> int4: if either a confutation occurs or a babysitting occurs or both, then a conceptualization occurs; int3 & int4 -> int5: that either a confutation occurs or a babysitting occurs or both results in that a conceptualization occurs; int5 & int2 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 0.0))

    score = _calc_score(
        'fact9 -> int1: that that a overspill occurs is not true causes that that a Mills occurs is not true; fact3 & int1 -> int2: a psalmody and a coaching results in that that a Mills occurs is not the fact; fact1 & fact6 -> int3: a psalmody occurs; fact4 & fact2 -> int4: a coaching occurs; int3 & int4 -> int5: a psalmody and a coaching occurs; int2 & int5 -> hypothesis;',

        'fact6 & fact1 -> int1: a psalmody occurs; fact2 & fact4 -> int2: a coaching occurs; int2 & int1 -> int3: a psalmody and a coaching occurs; fact9 -> int4: if it is wrong that a overspill occurs, then it is not true that a Mills occurs; int4 & fact3 -> int5: that a psalmody and a coaching occurs causes that that a Mills occurs is not true; int3 & int5 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact7 & fact5 -> int1: a commemorative ketone leads to a semiterrestrial flail; int1 -> int2: a flail that is not semiterrestrial results in a ketone that is not commemorative; fact6 & fact3 -> int3: if a bacchante either behooves or blazes or both, then it is not true that a flail is semiterrestrial; fact1 -> int4: a bacchante either behooves or blazes or both; int3 & int4 -> int5: it is wrong that a flail is semiterrestrial; int2 & int5 -> hypothesis;',

        'fact1 -> int1: a bacchante either behooves or blazes or both; fact6 & fact3 -> int2: if a bacchante either behooves or blazes or both, then it is wrong that a flail is semiterrestrial; fact7 & fact5 -> int3: a commemorative ketone results in a flail that is semiterrestrial; int1 & int2 -> int4: it is not true that a flail is semiterrestrial; int3 -> int5: if it is wrong that a flail is semiterrestrial, then it is not true that a ketone is commemorative; int5 & int4 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact6 -> int1: that that a about-face occurs is wrong leads to that that a mercy occurs is wrong; fact4 & int1 -> int2: a plasmapheresis and a piss-up results in that that a mercy occurs is wrong; fact2 -> int3: a plasmapheresis occurs; fact5 -> int4: a piss-up occurs; int3 & int4 -> int5: a plasmapheresis and a piss-up occurs; int2 & int5 -> hypothesis;',

        'fact5 -> int1: a piss-up occurs; fact2 -> int2: a plasmapheresis occurs; int1 & int2 -> int3: a plasmapheresis and a piss-up occurs; fact6 -> int4: that that a about-face occurs is not true results in that that a mercy occurs is not true; int4 & fact4 -> int5: that a plasmapheresis and a piss-up occurs results in that that a mercy occurs is not true; int5 & int3 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact8 & fact7 -> int1: if a conceptualization occurs, then it is not true that a flap and a return do not occur; fact3 & int1 -> int2: if a reduplication does not occur, then it is not true that a flap and a return do not occur; fact4 & fact5 -> int3: a confutation or a babysitting or both leads to that that a reduplication occurs is wrong; fact9 -> int4: either a confutation occurs or a babysitting occurs or both; int3 & int4 -> int5: it is not true that a reduplication occurs; int2 & int5 -> hypothesis;',

        'fact9 -> int1: either a confutation occurs or a babysitting occurs or both; fact8 & fact7 -> int2: if a conceptualization occurs, then it is not the fact that a flap and a return do not occur; fact4 & fact5 -> int3: a confutation or a babysitting or both causes that that a reduplication occurs is not the fact; fact3 & int1 -> int4: if either a confutation occurs or a babysitting occurs or both, then a conceptualization occurs; int3 & int4 -> int5: that either a confutation occurs or a babysitting occurs or both results in that a conceptualization occurs; int5 & int2 -> hypothesis',

        zero_one=True,
    )
    assert (math.isclose(score, 0.0))

    score = _calc_score(
        'fact7 &  fact8          ->           int1:       that either a headway occurs or a spoil occurs or both leads to that a repossession occurs;'
        'fact5 &  fact9          ->           int2:       that a repossession occurs leads to that that a saraband occurs is not true;'
        ' int1 &   int2          ->           int3:       that either a headway occurs or a spoil occurs or both causes that that a saraband occurs is not true;'
        'fact2                   ->           int4:       a headway occurs;'
        ' int4                   ->           int5:       either a headway occurs or a spoil occurs or both;'
        ' int3 &   int5          ->     hypothesis;',

        'fact2                   ->           int1:       a headway occurs;'
        ' int1                   ->           int2:       either a headway occurs or a spoil occurs or both;'
        'fact5 &  fact9          ->           int3:       that a repossession occurs results in that that a saraband occurs is not true;'
        'fact7 &  fact8          ->           int4:       that either a headway occurs or a spoil occurs or both causes that a repossession occurs;'
        ' int3 &   int4          ->           int5:       that either a headway occurs or a spoil occurs or both results in that that a saraband occurs is not the fact;'
        ' int2 &   int5          ->     hypothesis;',

        # zero_one=True,
        zero_one=False,
    )
    assert (math.isclose(score, 1.0))

    score = _calc_score(
        'fact1                  ->           int1:       if the cubist grafts, the cubist will not letter and is bubaline;'
        'fact2 & fact3          ->           int2:       if a cubist designates intemperance it grafts;'
        'int1  & int2          ->     hypothesis;',

        'fact3                  ->           int1:       if the cubist designates intemperance, the cubist is tense;'
        'int1 & fact2          ->           int2:       if the cubist designates intemperance, the cubist grafts;'
        'int2 & fact1          ->     hypothesis;',

        zero_one=True,
        allow_reference_step=True,
        facts='fact1: if something grafts, it will not letter and is bubaline '
              'fact2: if a cubist is tense it grafts '
              'fact3: if a cubist designates intemperance it is tense '
              'fact4: if something grafts, it will not depart and is bubaline '
              'fact5: if a cubist is tense it reship '
              'fact6: if a cubist designates intemperance it is wieldy ',
    )
    assert (math.isclose(score, 0.0))


def _check_limitation():
    # The tree structure is corret. sntence content is wrong.
    score = _calc_score(
        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A ;',
            'fact2 & fact6 -> int3: this is a sentence B ;',
            'int1 -> int2: this is a sentence C ;',
            'int3 -> int4: this is a sentence D ;',
            'int2 & int4 -> hypothesis;',
        ]),

        '; '.join([
            'fact1 & fact5 -> int1: this is a sentence A ;',
            'fact2 & fact6 -> int3: this is a sentence B ;',
            'int1 -> int4: this is a sentence D ;',
            'int3 -> int2: this is a sentence C ;',
            'int2 & int4 -> hypothesis;',
        ]),

        zero_one=True,
    )
    assert (score >= 0.99)


if __name__ == '__main__':
    test_calc_score_on_toy_examples()
    test_calc_score_on_real_examples()
    # _check_limitation()
