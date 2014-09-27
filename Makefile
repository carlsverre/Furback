NO_COLOR=\033[0m
INFO_COLOR=\033[32;01m
OK_COLOR=\033[31;32m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m

.PHONY: all
all: deps

.PHONY: deps
deps:
	@echo "$(INFO_COLOR)==> Checking/Installing dependencies$(NO_COLOR)"
	@source ./activate && pip install -Ur requirements.txt

.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -name "__pycache__" -print0 | xargs -0 rm -r
