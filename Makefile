PYTHON ?= python3

.PHONY: help new task run show brief check research-units sections impact human-outline human-section assemble test

help:
	@$(PYTHON) scripts/help.py

new:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/new_product.py "$(PRODUCT)" --title "$(TITLE)"

task:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(OPERATION)" || (echo "Thiếu OPERATION=<name>" && exit 1)
	@$(PYTHON) scripts/task.py create "products/$(PRODUCT)" "$(OPERATION)" $(if $(SECTION),--section "$(SECTION)") $(if $(UNIT),--unit "$(UNIT)") $(if $(RUNTIME),--runtime "$(RUNTIME)")

run:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(TASK)" || (echo "Thiếu TASK=<task-id>" && exit 1)
	@$(PYTHON) scripts/outline_runtime.py run "products/$(PRODUCT)" "$(TASK)" $(if $(DSH),--executable "$(DSH)")

show:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/task.py show "products/$(PRODUCT)"

brief:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/task.py brief "products/$(PRODUCT)" $(TASK)

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

human-outline:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(REQUEST)" || (echo "Thiếu REQUEST=..." && exit 1)
	@test -n "$(PATHS)" || (echo "Thiếu PATHS='outline.json ...'" && exit 1)
	@$(PYTHON) scripts/approval.py human-amend-outline "products/$(PRODUCT)" --request "$(REQUEST)" $(foreach path,$(PATHS),--path "$(path)")

human-section:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(SECTION)" || (echo "Thiếu SECTION=P##" && exit 1)
	@test -n "$(REQUEST)" || (echo "Thiếu REQUEST=..." && exit 1)
	@test -n "$(PATHS)" || (echo "Thiếu PATHS='draft.md ...'" && exit 1)
	@$(PYTHON) scripts/approval.py human-amend-section "products/$(PRODUCT)" "$(SECTION)" --request "$(REQUEST)" $(foreach path,$(PATHS),--path "$(path)")

assemble:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/assemble.py "products/$(PRODUCT)"

test:
	@$(PYTHON) -m unittest discover -s tests -v
