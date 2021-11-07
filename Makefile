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
	cd ./morty/dashboard/frontend/ && yarn build
	poetry-dynamic-versioning
	poetry build