
PYTHON_VERSION = 3.9.2

.venv = .venv
.python-version = .python-version

$(.python-version):
	pyenv install $(PYTHON_VERSION)
	echo $(PYTHON_VERSION) > $(.python-version)

$(.venv): $(.python-version)
	python -m venv $(.venv)

setup: $(.venv)
	echo Setting up virtualenv with python $(PYTHON_VERSION)