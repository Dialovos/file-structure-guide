.PHONY: requirements data features train clean lint test help

PYTHON ?= python

help:
	@echo "Targets:"
	@echo "  requirements  install package + dev deps in editable mode"
	@echo "  data          download/build data/processed/ from data/raw/"
	@echo "  features      run feature engineering"
	@echo "  train         train and persist a model"
	@echo "  clean         remove caches + build artifacts"
	@echo "  lint          run ruff"
	@echo "  test          run pytest"

requirements:
	$(PYTHON) -m pip install -e ".[dev]"

data:
	$(PYTHON) -m project.data.make_dataset data/raw data/processed

features:
	$(PYTHON) -m project.features.build_features

train:
	$(PYTHON) -m project.models.train_model

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache

lint:
	ruff check src tests

test:
	pytest -q
