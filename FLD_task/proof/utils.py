from enum import Enum
import re
import random
import unicodedata
from typing import List, Dict, OrderedDict, Tuple, Optional, Union
import logging

from .stance import delete_stance_markers, get_stance_markers
logger = logging.getLogger(__name__)

SENT_IDENT = 'sent'
VOID_IDENT = 'void'
INT_IDENT = 'int'
HYPOTHESIS_IDENT = 'hypothesis'
ASSUMP_IDENT = 'assump'


class InvalidProof(Exception):
    pass


class InvalidProofStep(Exception):
    pass


def normalize_proof(proof_text: str) -> str:
    proof_text = re.sub('\n+', ' ', proof_text)
    proof_text = re.sub(r'\s+', ' ', proof_text)
    proof_text = re.sub(r'\s+$', '', re.sub(r'^\s+', '', proof_text))
    return proof_text


def prettify_proof_text(proof_text: str, indent=0) -> str:
    proof_text = normalize_proof(proof_text)
    stance_markers = get_stance_markers(proof_text)
    proof_text = delete_stance_markers(proof_text)

    proof_text = re.sub(' *; *$', '', proof_text)
    pretty_lines = []
    if re.match(r'\S+', proof_text):
        proof_lines = re.split(r' *; *', proof_text)
    else:
        proof_lines = []
    for line in proof_lines:
        if line.find(' -> ') < 0:
            logger.info('Could not prettify the proof since the following line have no " -> ": "%s"', line)
            return proof_text

        implication_fields = line.split(' -> ')
        if len(implication_fields) > 2:
            logger.info('Could not prettify the proof since the following line have more than two " -> ": "%s"', line)
            return proof_text

        premises_text, concl_text = line.split(' -> ')

        premises = premises_text.split(' & ')
        pretty_premise_texts = []
        for premise_text in sorted(premises):
            pretty_premise_texts.append(f'{premise_text:>8}')
        pretty_premises_text = ''.join(pretty_premise_texts)

        if concl_text.find(': ') >= 0:
            concl_fields = concl_text.split(': ')
            if len(concl_fields) > 2:
                logger.info('Could not prettify the proof since the following line have more than two ": ": "%s"', line)
                return proof_text
            concl_sent_id, concl_sentence = concl_fields
            pretty_concl_text = f'{concl_sent_id:>10}:       {concl_sentence}'
        else:
            pretty_concl_text = f'{concl_text:>10}'

        # pretty_line = ' ' * indent_level + f'{pretty_premises_text:<25} ->     {pretty_concl_text}'
        pretty_line = f'{pretty_premises_text:<25} ->     {pretty_concl_text}'
        pretty_lines.append(pretty_line)

    stance_markers_text = f'=>    stance markers = {str([mk.value for mk in stance_markers])}'
    pretty_lines.append(' ' * 50 + stance_markers_text)

    pretty = ' ' * indent + ('\n' + ' ' * indent).join(pretty_lines)
    return pretty


def prettify_context_text(context_text: str, indent: int = 0) -> str:
    sentences = re.sub('sent([0-9]+)', '\nsent\g<1>', context_text).strip('\n').split('\n')
    sentences = sorted(sentences, key = lambda sentence: int(re.sub(r'^sent([0-9]+).*', r'\g<1>', sentence)))
    pretty = ' ' * indent + ('\n' + ' ' * indent).join(sentences)
    return pretty


class NodeType(Enum):
    sent = 'sentence'
    int = 'internal'
    assump = 'assumption'
    assump_deletion = 'assumption_deletion'
    void = 'void'
    hypothesis = 'hypothesis'


def get_node_type(rep: str) -> Optional[NodeType]:
    if rep.strip().startswith('sent'):
        return NodeType.sent
    elif rep.strip().startswith('int'):
        return NodeType.int
    elif rep.strip().startswith('assump'):
        return NodeType.assump
    elif rep.strip().startswith('[assump'):
        return NodeType.assump_deletion
    elif rep.strip().startswith('void'):
        return NodeType.void
    elif rep.strip().startswith('hypothesis'):
        return NodeType.hypothesis
    else:
        return None


def extract_ident(rep: str, allow_sentence=False) -> Optional[str]:
    if allow_sentence:
        m = re.match(r"(?P<ident>(sent\d+[: ]|int\d+[: ]|assump\d+[: ]|\[assump\d+\][: ]|void[: ]|hypothesis[; ]))", rep)
    else:
        m = re.fullmatch(r"(?P<ident>(sent\d+[: ]|int\d+[: ]|assump\d+[: ]|\[assump\d+\][: ]|void[: ]|hypothesis[; ]))", rep)
    if m is None:
        return None
    return m["ident"][:-1]


def extract_idents(rep: str) -> List[str]:
    idents = []
    for ident in re.findall(r'(sent\d+[: ]|int\d+[: ]|assump\d+[: ]|\[assump\d+\][: ]|void[: ]|hypothesis[; ])', rep):
        idents.append(ident[:-1])
    return idents


def extract_ident_sent(rep: str) -> Optional[Tuple[str, str]]:
    ident_sents = extract_ident_sents(rep)
    if len(ident_sents) == 0:
        return None
    elif len(ident_sents) == 1:
        return list(ident_sents.items())[0]
    else:
        raise ValueError(f'Multiple idents / sentence found in "{rep}"')


def extract_ident_sents(rep: str) -> Dict[str, str]:
    ident_sents: Dict[str, str] = {}

    ident_matches = [m for m in re.finditer(r"(sent\d*: |int\d*: |assump\d*: )", rep)]
    is_proof_rep = rep.find(' -> ') >= 0

    for i_match, match in enumerate(ident_matches):
        if is_proof_rep:
            end = match.end() + rep[match.end():].find(';')
        else:
            if len(ident_matches) > i_match + 1:
                next_match = ident_matches[i_match + 1]
                end = next_match.start()
            else:
                end = len(rep)

        ident = match.group()[:-2]  # strip ":"
        sent = rep[match.end():end]
        # ident_sents[ident] = re.sub(' *;* *$', '', re.sub('^ *', '', sent))
        ident_sents[ident] = sent.rstrip(' ')

    return ident_sents


def extract_steps(proof: str) -> List[str]:
    steps = re.sub(' *; *$', '', proof).split(';')
    return [step.strip(' ') for step in steps]


def extract_premise_concl(step: str) -> Tuple[str, str]:
    return step.split(' -> ')
            

def extract_premises_concl(step: str) -> Tuple[List[str], str]:
    premise, concl = extract_premise_concl(step)
    premises = premise.split(' & ')
    return premises, concl


def get_lowest_vacant_int_id(text: str) -> Optional[int]:
    idents = extract_idents(text)
    int_idents = [ident for ident in idents
                  if re.match(f'^{INT_IDENT}[0-9]+$', ident)]
    int_idxs = [int(int_id[len(INT_IDENT):]) for int_id in int_idents]

    return max(int_idxs) + 1 if len(int_idxs) > 0 else 1


def is_valid_premise(rep: str) -> bool:
    return re.fullmatch(r"(sent\d+|int\d+|assump\d+|\[assump\d+\]|void)", rep)


def normalize(text: str) -> str:
    """
    Deal with unicode-related artifacts.
    """
    return unicodedata.normalize("NFD", text)


def normalize_sentence(text: str, no_lower=True) -> str:
    """
    Convert sentences to lowercase and remove the trailing period.
    """
    text = normalize(text)
    if not no_lower:
        text = text.lower()
    text = text.strip()
    if text.endswith("."):
        text = text[:-1].strip()
    return text


def extract_context(ctx: str, no_lower=True) -> OrderedDict[str, str]:
    """
    Extract supporting facts from string to dict.
    """
    return OrderedDict(
        {
            ident.strip(): normalize_sentence(sent, no_lower=no_lower)
            for ident, sent in re.findall(
                r"(?P<ident>sent\d+): (?P<sent>.+?) (?=sent\d+)", ctx + " sent999"
            )
        }
    )


def extract_assumptions(proof_text: str, no_lower=True) -> OrderedDict[str, str]:
    assumptions = OrderedDict()
    for m_begin in re.finditer(r'-> *assump\d+', proof_text):
        begin = m_begin.span()[0]
        assump_text = re.sub(r' *-> *', '', proof_text[begin:].split(';')[0])
        ident, sent = re.split(r':  *', assump_text)
        assumptions[ident.strip()] = normalize_sentence(sent, no_lower=no_lower)
    return assumptions


def rename_idents(proof: str, assert_on_duplicated_ident=True) -> str:
    """
    Rename the `int\d+` and `assump\d+` identifiers in a proof so that they increase from 1.
    """
    renamed_proof = proof
    renamed_proof = _rename_idents(renamed_proof, 'int', assert_on_duplicated_ident=assert_on_duplicated_ident)
    renamed_proof = _rename_idents(renamed_proof, 'assump', assert_on_duplicated_ident=assert_on_duplicated_ident)
    return renamed_proof


def _rename_idents(proof: str, ident_prefix: str, assert_on_duplicated_ident=True) -> str:
    from src.prover.proof import InvalidProof
    proof_org = proof

    # print('=============== _rename_idents() ==============')
    # print('proof:', proof)
    # print('ident_prefix:', ident_prefix)

    assert "HOGEFUGAPIYO" not in proof
    mapping: Dict[str, str] = dict()

    while True:
        # print('------------- while ------------')
        m = re.search(f"{ident_prefix}\d+", proof)
        if m is None:
            break
        s = m.group()
        if assert_on_duplicated_ident:
            assert s not in mapping
        else:
            if s in mapping:
                raise InvalidProof(f'Identifier "{s}" might be duplicated in "{proof_org}"')
        # try:
        #     assert s not in mapping
        # except:
        #     from pprint import pprint
        #     print('proof:', proof)
        #     print('s:', s)
        #     print('mapping:')
        #     pprint(mapping)
        #     raise
        dst = f"HOGEFUGAPIYO{1 + len(mapping)}"
        mapping[s] = dst
        proof = proof.replace(f"{s}:", f"{dst}:").replace(f"{s} ", f"{dst} ")

    return proof.replace("HOGEFUGAPIYO", ident_prefix)
