.PHONY: install format lint test sec

install:
	@poetry install
format:
	@isort .
	@blue .
lint:
	@blue . --check
	@isort . --check
	@prospector --with-tool pep257 --doc-warning
sec:
	@pip-audit