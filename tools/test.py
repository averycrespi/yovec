from difflib import Differ
from pathlib import Path
import subprocess


cases = [p.with_suffix('') for p in Path('programs').glob('*.yovec')]
for case in cases:
    yovec = case.with_suffix('.yovec')
    yolol = case.with_suffix('.yolol')

    if not yolol.exists():
        print('Generating {} ...'.format(yolol))
        result = subprocess.run(['python3', 'yovec-cli.py', '-i', yovec, '-o', yolol])
        if result.returncode != 0:
            exit(1)

    print('Testing {} ...'.format(yovec))
    result = subprocess.run(['python3', 'yovec-cli.py', '-i', yovec], stdout=subprocess.PIPE)
    if result.returncode != 0:
        exit(1)
    output = result.stdout.decode('utf-8').strip()
    with open(yolol) as f:
        expected = f.read().strip()
    if output != expected:
        print('Test failed: output was different than expected\n')
        diff = list(Differ().compare(expected.splitlines(), output.splitlines()))
        print('\n'.join(diff))
        exit(1)

exit(0)
