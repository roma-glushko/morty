flake:
	flake8 ./morty ./examples

isort:
	isort ./morty ./examples

black:
	black ./morty ./examples

mypy:
	mypy ./morty ./examples

lint:
	make isort && make black && make flake  && make mypy

test:
	pytest ./tests

clean-exps:
	rm -rf ./examples/experiments/*

build:
	make build-frontend
	make build-lib

build-frontend:
	cd ./morty/dashboard/frontend/ && yarn build

build-lib:
	poetry-dynamic-versioning
	poetry build