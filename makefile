
#
#	EXTERNAL DEPENDENCIES:
#		pyenv
#

PYTHON_VERSION = 3.9.2

.venv = .venv
.python-version = .python-version

python = $(.venv)/bin/python
pip = $(.venv)/bin/pip

$(.python-version):
	pyenv install $(PYTHON_VERSION)
	echo $(PYTHON_VERSION) > $(.python-version)

$(.venv): $(.python-version)
	echo Setting up virtualenv with python $(PYTHON_VERSION)
	python -m venv $(.venv)

setup-dev: $(.venv) requirements-dev.txt
	$(pip) install --upgrade pip
	$(pip) install -r requirements-dev.txt

	echo Attaching .venv to Jupyter
	$(python) -m ipykernel install --name=$(.venv)

requirements.txt: $(.venv) requirements.in
	$(pip) install pip-tools
	$(.venv)/bin/pip-compile requirements.in 

setup: $(.venv) requirements.txt
	$(pip) install -r requirements.txt

test:
	# invoke pytest through python to ensure repo root dir is in PYTHONPATH
	$(python) -m pytest tests -v

start-api: setup
	FLASK_APP=src/api/app \
	FLASK_ENV=development \
	$(python) -m flask run