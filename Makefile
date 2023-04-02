# Makefile

# Define variables
PYTHON = python3
PACK_DIR = src
SRC_FILES = $(wildcard $(PACK_DIR)/*.py)
MAIN_FILE = main.py

# Define targets
all: run GenDatabase apriori idea1 idea2

GenDatabase:
	$(PYTHON) src/GenDatabase.py

apriori:
	$(PYTHON) src/apriori.py $(DATABASE) $(MS)

idea1:
	$(PYTHON) src/idea1.py $(DATABASE) $(MS)

idea2:
	$(PYTHON) src/idea2.py $(DATABASE) $(MS) $(PART_SIZE)

make:
	$(PYTHON) setup.py build bdist_wheel
	pip install -r requirements.txt


clean:
	if exist "./build" rd /s /q build
	if exist "./dist" rd /s /q dist

.PHONY: make all clean
