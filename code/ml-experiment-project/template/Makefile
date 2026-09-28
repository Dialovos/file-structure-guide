CONFIG ?= configs/experiment/baseline.toml
SEED ?= 0

train:
	python -m project.train --config $(CONFIG) --seed $(SEED)

test:
	pytest -q
