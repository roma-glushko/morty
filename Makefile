flake:
	flake8 ./morty ./examples

isort:
	isort ./morty ./examples

black:
	black .

lint:
	make isort && make black && make flake