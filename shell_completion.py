#!/usr/bin/python

import os
from pathlib import Path
home = str(Path.home())

SHELL = os.getenv('SHELL')

if SHELL == '/bin/bash':
    with open(home + '/.bashrc', 'a') as file:
        file.write('eval "$(_ONE_COMPLETE=source_bash one)"\n')
    os.system('. ' + home + '/.bashrc')
elif SHELL == "/bin/zsh":
    with open(home + '/.zshrc', 'a') as file:
        file.write('eval "$(_ONE_COMPLETE=source_zsh one)"\n')
    os.system('. ' + home + '/.zshrc')
else:
    print('Sorry we do not have support for your shell')
