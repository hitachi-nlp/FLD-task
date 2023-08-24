from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Deduction(BaseModel):
    hypothesis: str
    context: str

    hypothesis_formula: Optional[str] = None
    context_formula: Optional[str] = None

    proofs: Optional[List[str]] = []
    proof_label: Optional[str] = None
    proofs_formula: Optional[List[str]] = []

    world_assump_label: Optional[str] = None
    original_tree_depth: Optional[int] = None
    depth: Optional[int] = None
    num_formula_distractors: Optional[int] = None
    num_translation_distractors: Optional[int] = None
    num_all_distractors: Optional[int] = None

    negative_hypothesis: Optional[str] = None
    negative_hypothesis_formula: Optional[str] = None
    negative_original_tree_depth: Optional[int] = None
    negative_proofs: Optional[List[str]] = []
    negative_proof_label: Optional[str] = None
    negative_world_assump_label: Optional[str] = None

    version: Optional[str] = None


class SerializedDeduction(BaseModel):
    input: str
    next_step: Optional[str] = None
    gold_proofs: Optional[List[str]] = []


class AnswerLabel(Enum):
    PROVED = 'PROVED'
    DISPROVED = 'DISPROVED'
    UNKNOWN = 'UNKNOWN'


class ProofStanceLabel(Enum):
    PROVED = 'PROVED'
    DISPROVED = 'DISPROVED'
    UNKNOWN = 'UNKNOWN'
