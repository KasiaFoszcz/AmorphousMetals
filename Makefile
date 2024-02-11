POETRY_RUN := poetry run
DOCKER_COMPOSE := docker compose

DOCKER_COMPOSE_PULL := $(DOCKER_COMPOSE) pull
DOCKER_COMPOSE_RUN_ARGS := --rm -p 8501:8501
DOCKER_COMPOSE_RUN := $(DOCKER_COMPOSE) run $(DOCKER_COMPOSE_RUN_ARGS)

ENTRYPOINT := metale_amorficzne/streamlit.py
DOCKER_TAG := edge

run-local:
	$(POETRY_RUN) streamlit run $(ENTRYPOINT) \
		--server.runOnSave true \
		--server.enableStaticServing true \
		--server.headless true

DOCKER_SETUP := DOCKER_TAG=$(DOCKER_TAG) $(DOCKER_COMPOSE_PULL)

run-docker:
	$(DOCKER_SETUP) && $(DOCKER_COMPOSE_RUN) streamlit

run-docker-local:
	$(DOCKER_SETUP) && $(DOCKER_COMPOSE_RUN) streamlit-local

.PHONY: run-local run-docker run-docker-local
