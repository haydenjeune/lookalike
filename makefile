
#
#	EXTERNAL DEPENDENCIES:
#		pyenv
#

PYTHON_VERSION = 3.8.12

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
	touch $(.venv)

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

build: build-api build-index build-worker

build-api: $(.venv)
	./pants package src/api

build-worker: $(.venv)
	./pants package src/worker

build-index: $(.venv)
	./pants package src/index

start-api: $(.venv)
	./pants run src/api

start-web: 
	npm --prefix web/lookalike-web start

start-worker: $(.venv)
	./pants run src/worker

start-index: $(.venv)
	./pants run src/index

lint: setup infrastructure/aws/template.yaml
	$(.venv)/bin/cfn-lint infrastructure/aws/template.yaml

deploy-cfn:
# TODO: deploy cfn template 
	stackit up --template infrastructure/aws/template.yaml --stack-name lookalike --region ap-southeast-2

generate-grpc:
	$(python) -m grpc_tools.protoc -I src/protos --python_out=src/index/generated --grpc_python_out=src/index/generated src/index/index.proto

build-env:
	docker build -f  infrastructure/docker/build-env.Dockerfile -t build-env .

build-api-linux: build-env
	docker run --rm -v $(shell pwd):/code --workdir /code build-env:latest "./pants package src/api"

build-index-linux: build-env
	docker run --rm -v $(shell pwd):/code --workdir /code build-env:latest "./pants package src/index"

publish-demo: build-api-linux build-index-linux
	./scripts/publish-demo-image.sh
