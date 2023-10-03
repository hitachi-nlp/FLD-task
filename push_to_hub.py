#!/usr/bin/env python
import tempfile
import json

import click
from datasets import load_dataset
from FLD_task import load_deduction, serialize


@click.command()
@click.option('--train', type=str, default=None)
@click.option('--valid', type=str, default=None)
@click.option('--test', type=str, default=None)
@click.option('--repo-name')
@click.option('--no-serial', is_flag=True)
@click.option('--extension', type=str, default='json')
@click.option('--use-auth-token', is_flag=True)
def main(train,
         valid,
         test,
         repo_name,
         no_serial,
         extension,
         use_auth_token):

    split_paths = {
        'train': train,
        'validation': valid,
        'test': test,
    }
    processed_split_paths = {}

    for split, path in list(split_paths.items()):
        tmp_path = tempfile.mktemp()
        with open(tmp_path, 'w') as f_out:
            for line in open(path):
                example = load_deduction(json.loads(line.rstrip('\n')))
                serial = serialize(example, stepwise=False, include_max_subproof_for_unknown=False)
                if not no_serial:
                    example.prompt_serial = serial.prompt
                    example.proof_serial = serial.proof
                if serial.proof != serial.next_proof_step: 
                    raise Exception()
                f_out.write(json.dumps(example.dict()))
        processed_split_paths[split] = tmp_path

    datasets = load_dataset(
        extension,
        data_files=processed_split_paths,
        cache_dir=False,
        use_auth_token=use_auth_token,
    )

    datasets.push_to_hub(repo_name)


if __name__ == '__main__':
    main()
