flake:
	flake8 ./morty ./examples

isort:
	isort ./morty ./examples

black:
	black .

mypy:
	mypy ./morty ./examples

lint:
	make isort && make black && make flake  && make mypy

test:
	pytest ./tests

clean-exps:
	rm -rf ./examples/experiments/*


build:
	cd ./morty/experiment/dashboard/frontend/ && yarn build
	poetry build