
#
#	EXTERNAL DEPENDENCIES:
#		pyenv
#		jupyterlab
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
	python -m venv $(.venv)

requirements.txt: $(.venv) requirements.in
	$(pip) install pip-tools
	$(.venv)/bin/pip-compile requirements.in 

setup: $(.venv) requirements.txt
	echo Setting up virtualenv with python $(PYTHON_VERSION)
	$(pip) install --upgrade pip
	$(pip) install -r requirements.txt

	echo Attaching .venv to Jupyter
	$(pip) install ipykernel
	$(python) -m ipykernel install --user --name=$(.venv)
