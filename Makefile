BR2_EXTERNAL_DIR := $(shell readlink -f .)
BUILDROOT_DIR := $(BR2_EXTERNAL_DIR)/buildroot
OUTPUT_DIR := $(BR2_EXTERNAL_DIR)/output

INSIDE_DOCKER = /home/br-user
CURRENT_DIR = $(shell pwd)

TARGETS = \
  check-check-package \
  update-reference-log \
  check-package-reference-log \
  check-package-python-version \
  unit-tests \
  unit-tests-style

.PHONY: default
default: check-check-package

ifneq ($(CURRENT_DIR),$(INSIDE_DOCKER))

ALL_TARGETS = $(TARGETS) submodules checkout
.PHONY: $(ALL_TARGETS)
$(ALL_TARGETS):
	./docker-run make $@

else # ifneq ($(CURRENT_DIR),$(INSIDE_DOCKER))

.PHONY: submodules
submodules: $(BUILDROOT_DIR)/README
# FIXME: below 'sed' is a workaround for old versions of check-package
$(BUILDROOT_DIR)/README:
	git submodule init
	git submodule update
	sed 's,#!/usr/bin/env python$$,#!/usr/bin/env python3,g' -i $(BUILDROOT_DIR)/utils/check-package

.PHONY: checkout
checkout: $(OUTPUT_DIR)/Makefile
$(OUTPUT_DIR)/Makefile: submodules
# FIXME: avoid error when running the first time inside docker
# No rule to make target '/home/br-user/output/.br2-external.mk
	-make -C $(BUILDROOT_DIR) BR2_EXTERNAL=$(BR2_EXTERNAL_DIR) O=$(OUTPUT_DIR) defconfig
	make -C $(BUILDROOT_DIR) BR2_EXTERNAL=$(BR2_EXTERNAL_DIR) O=$(OUTPUT_DIR) defconfig

.PHONY: $(TARGETS)
$(TARGETS): checkout
	make -C $(OUTPUT_DIR) $@

endif # ifneq ($(CURRENT_DIR),$(INSIDE_DOCKER))

.PHONY: clean
clean:
	rm -rf $(OUTPUT_DIR)

.PHONY: distclean
distclean: clean
	rm -rf $(BUILDROOT_DIR)
