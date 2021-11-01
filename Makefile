BR2_EXTERNAL_DIR := $(shell readlink -f .)
BUILDROOT_DIR := $(BR2_EXTERNAL_DIR)/buildroot
OUTPUT_DIR := $(BR2_EXTERNAL_DIR)/output

TARGETS = \
  check-check-package \
  update-reference-log \
  check-package-reference-log \
  check-package-python-version \
  unit-tests

.PHONY: default
default: check-check-package

.PHONY: submodules
submodules: $(BUILDROOT_DIR)/README
$(BUILDROOT_DIR)/README:
	git submodule init
	git submodule update

.PHONY: checkout
checkout: $(OUTPUT_DIR)/Makefile
$(OUTPUT_DIR)/Makefile: submodules
	make -C $(BUILDROOT_DIR) BR2_EXTERNAL=$(BR2_EXTERNAL_DIR) O=$(OUTPUT_DIR) defconfig

.PHONY: $(TARGETS)
$(TARGETS): checkout
	make -C $(OUTPUT_DIR) $@

.PHONY: clean
clean:
	rm -rf $(OUTPUT_DIR)

.PHONY: distclean
distclean: clean
	rm -rf $(BUILDROOT_DIR)
