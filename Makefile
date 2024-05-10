start:
	python3 -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

install:
	poetry install

build:
	./build.sh

lint:
	poetry run flake8 task_manager
