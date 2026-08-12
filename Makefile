PYTHON ?= python3

.PHONY: help new check impact assemble test

help:
	@$(PYTHON) scripts/help.py

new:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/new_product.py "$(PRODUCT)" --title "$(TITLE)"

check:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/validate.py "products/$(PRODUCT)"

impact:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@test -n "$(CLAIM)$(CHAPTER)" || (echo "Cần CLAIM=<id> hoặc CHAPTER=<id>" && exit 1)
	@$(PYTHON) scripts/impact.py "products/$(PRODUCT)" $(if $(CLAIM),--claim "$(CLAIM)",--chapter "$(CHAPTER)")

assemble:
	@test -n "$(PRODUCT)" || (echo "Thiếu PRODUCT=<slug>" && exit 1)
	@$(PYTHON) scripts/assemble.py "products/$(PRODUCT)"

test:
	@$(PYTHON) -m unittest discover -s tests -v

