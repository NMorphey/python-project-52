# Task manager (WIP)

### About
**Task manager** is a web application for scheduling tasks. It is as a pet-project, that was created as the final task of the [programming course](https://hexlet.io/programs/python) i was taking. You can try it by using the link below or deploying and running it on any hosting (check guide below). The main tool used for develompent is Django framework (v. 5) for Python.

### Tests and linter status, CodeClimate:
[![Actions Status](https://github.com/NMorphey/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/NMorphey/python-project-52/actions) [![CI](https://github.com/NMorphey/python-project-52/actions/workflows/CI.yml/badge.svg)](https://github.com/NMorphey/python-project-52/actions/workflows/CI.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/6e000bb9682bd74c7db9/maintainability)](https://codeclimate.com/github/NMorphey/python-project-52/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/6e000bb9682bd74c7db9/test_coverage)](https://codeclimate.com/github/NMorphey/python-project-52/test_coverage)

### Deployed
https://taskmanager-ny6t.onrender.com  

### About
*This is an educational project. It's on the final stage of of creation, but some changes (e.g. refactoring, minor pages redesigns) still can be applied.*

### How to deploy or run locally
#### Package can be installed with following command:
>
> pip install --user git+https://github.com/NMorphey/python-project-52.git  
>
#### Required:
* Python (3.11+)
* Poetry (1.8+)
#### Environment
There are several env variables you may need to set:
* SECRET_KEY (mandatory)
* ACCESS_TOKEN (if you want to use Rollbar's error tracking - [see more](https://docs.rollbar.com/docs/django))
* DATABASE_URL (if you want to use DB other than SQLite - highly recommended)
#### settings.py
Project's settings are configured for deploying on [Render.com](https://render.com/). If you  are planning to host it somewhere else, make sure to edit following:
* `DEBUG` constant;
* `DATABASES` constant's 'dedault' field (if required to).
#### Commands
Use:
* `make build` to configure the environment and install dependencies;
* `make start` to run server. Whilist runned locally, it can be accessed on `127.0.0.1:8000/`.
