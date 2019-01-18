# virtualenv and run application
run:
	. venv/bin/activate && \
	python3 api/main.py

venv:
	virtualenv -p /usr/bin/python3 venv/ && \
	make venv_install_reqs && \
	make venv_install_reqs_dev

venv_install_reqs:
	. venv/bin/activate && \
	pip install -r requirements.txt

venv_install_reqs_dev:
	. venv/bin/activate && pip install -r requirements_dev.txt

# tests and maintaining code
bandit:
	. venv/bin/activate && bandit -r api/*.py

black_all:
	. venv/bin/activate && black -l 119 -S api/ unittests/

test-unittests:
	. venv/bin/activate && \
	export PYTHONPATH=$PYTHONPATH:api/ && \
	python -m pytest api/ unittests/ -v -ra -s --cov --cov-report term-missing --pylama && \
	rm -r ".coverage" ".pytest_cache" "api/__pycache__" "unittests/__pycache__"
