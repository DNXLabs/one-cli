all: .venv install


.venv:
	virtualenv -p /usr/bin/python3 .venv


install: .venv
	.venv/bin/pip install --editable .


clean:
	rm -rf .venv
	rm -rf build
	rm -rf dist
	rm -rf one_cli.egg-info
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf one.spec
	find -iname "*.pyc" -delete


run: install
	.venv/bin/python cli.py $(filter-out $@,$(MAKECMDGOALS))


build: .venv
	.venv/bin/pip install -U PyInstaller
	.venv/bin/pyinstaller --clean --hidden-import one.__main__ cli.py --onefile --noconsole -n one


.requirements-test-lint:
	.venv/bin/pip install -r requirements-test.txt


test: .venv .requirements-test-lint
	.venv/bin/pytest -v tests/


flake8: .venv .requirements-test-lint
	.venv/bin/flake8 . --count --max-complexity=10 --max-line-length=127 --statistics --exclude .venv