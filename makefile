
#
#	EXTERNAL DEPENDENCIES:
#		pyenv
#

PYTHON_VERSION = 3.8.8

.venv = .venv
.python-version = .python-version
requirements.txt = 3rdparty/python/requirements.txt

python = $(.venv)/bin/python
pip = $(.venv)/bin/pip

$(.python-version):
	pyenv install $(PYTHON_VERSION)
	echo $(PYTHON_VERSION) > $(.python-version)

$(.venv): $(.python-version)
	echo Setting up virtualenv with python $(PYTHON_VERSION)
	python -m venv $(.venv)

clean:
	rm $(.python-version)
	rm -rf $(.venv)

$(requirements.txt): $(.venv) requirements.in
	$(pip) install pip-tools
	$(.venv)/bin/pip-compile requirements.in -o $(requirements.txt)

setup: $(.venv) $(requirements.txt)
	$(pip) install --upgrade pip
	$(pip) install -r $(requirements.txt)

	echo Attaching .venv to Jupyter
	$(python) -m ipykernel install --name=$(.venv)

test:
	./pants test tests/unit::

start-api: setup
	./pants run src/api

start-web:
	npm --prefix web/lookalike-web start

start: start-web start-api