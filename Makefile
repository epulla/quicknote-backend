WIN=$(if $(findstring MINGW,$(shell uname -s)),1,0) # returns 1 if OS is Windows
PYTHON_COMMAND=$(if $(filter $(WIN),0),python3,python)
PYTHON_ACTIVATE_ENV_DIR=$(if $(filter $(WIN),0),bin,Scripts)
REQUIREMENTS_FILE=$(if $(filter $(WIN),0),requirements.txt,requirements_win.txt)


start: ACTIVATE_ENV=1
start:
	if [ $(ACTIVATE_ENV) = 0 ] ; then \
		python main.py ; \
	else \
		source .venv/$(PYTHON_ACTIVATE_ENV_DIR)/activate ; \
		python main.py ; \
	fi

install:
	$(PYTHON_COMMAND) -m venv .venv ; \
	source .venv/$(PYTHON_ACTIVATE_ENV_DIR)/activate ; \
	pip install -U pip ; \
	pip install -r $(REQUIREMENTS_FILE) ; \
	deactivate

# Redis Commands Wrapper

start_redis:
	docker-compose -f redis.docker-compose.yaml up

