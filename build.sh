#!/bin/sh

pyinstaller --clean --hidden-import one.__main__ cli.py --onefile --noconsole -n one

sudo rm -rf /usr/local/bin/one

sudo mv ./dist/one /usr/local/bin/one

sudo chmod +x /usr/local/bin/one