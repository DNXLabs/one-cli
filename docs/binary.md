## Generate Binary

```bash
pip install pyinstaller
pyinstaller --clean --hidden-import one.__main__ cli.py --onefile --noconsole -n one
```