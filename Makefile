PYTHON ?= python3

.PHONY: help new task show check research-units sections impact assemble test

help:
	@$(PYTHON) scripts/help.py

new:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/new_product.py "$(PRODUCT)" --title "$(TITLE)"

task:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(OPERATION)" || (echo "Thiếu OPERATION=<name>" && exit 1)
	@$(PYTHON) scripts/task.py create "products/$(PRODUCT)" "$(OPERATION)" $(if $(SECTION),--section "$(SECTION)") $(if $(UNIT),--unit "$(UNIT)")

show:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/task.py show "products/$(PRODUCT)"

check:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/validate.py "products/$(PRODUCT)"

research-units:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/materialize_research.py "products/$(PRODUCT)"

sections:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/materialize_sections.py "products/$(PRODUCT)"

impact:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(CLAIM)$(SECTION)" || (echo "Cần CLAIM=<id> hoặc SECTION=<id>" && exit 1)
	@$(PYTHON) scripts/impact.py "products/$(PRODUCT)" $(if $(CLAIM),--claim "$(CLAIM)",--section "$(SECTION)")

assemble:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/assemble.py "products/$(PRODUCT)"

test:
	@$(PYTHON) -m unittest discover -s tests -v

