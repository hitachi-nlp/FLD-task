from setuptools import setup
from setuptools import find_packages

setup(
    name='FLD_task',
    version='0.0',
    description='A utility library for loading FLD datasets and computing metrics on them.',
    install_requires=[
        'nltk',
        'evaluate',
        'strsimpy',
        'rouge-score',
        'pydantic',
    ],
    packages=find_packages(),
    zip_safe=False,
)
