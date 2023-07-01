import re
from typing import List
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class StanceMarker(Enum):
    PROVED = '__PROVED__'
    DISPROVED = '__DISPROVED__'
    UNKNOWN = '__UNKNOWN__'


def get_stance_markers(text: str) -> List[StanceMarker]:
    markers = []
    for marker in [StanceMarker.PROVED,
                   StanceMarker.DISPROVED,
                   StanceMarker.UNKNOWN]:
        if re.search(f' *{marker.value}', text):
            markers.append(marker)
    return markers


def add_stance_markers(text: str, markers: List[StanceMarker]) -> str:
    for marker in markers:
        if not re.search(f' *{marker.value}', text):
            if text == '':
                text = marker.value
            else:
                text += ' ' + marker.value

    return text


def delete_stance_markers(text: str) -> str:
    for marker in [StanceMarker.PROVED, StanceMarker.DISPROVED, StanceMarker.UNKNOWN]:
        if re.search(f' *{marker.value}', text):
            text = re.sub(f' *{marker.value}', '', text)
    return text
