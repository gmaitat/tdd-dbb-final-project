# Makefile para Product Catalogue Microservice

.PHONY: install run test bdd lint help

help:
	@echo "Comandos disponibles:"
	@echo "  make install   - Instala todas las dependencias"
	@echo "  make run       - Inicia el servidor Flask"
	@echo "  make test      - Ejecuta pruebas unitarias con cobertura"
	@echo "  make bdd       - Ejecuta escenarios BDD con behave"
	@echo "  make lint      - Ejecuta flake8 linting"

install:
	pip install -r requirements.txt

run:
	python wsgi.py

test:
	python -m pytest tests/ -v --cov=service --cov-report=term-missing

bdd:
	behave features/products.feature

lint:
	flake8 service/ tests/ features/ --max-line-length=100
