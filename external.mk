include $(sort $(wildcard $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/package/*/*.mk))

check-check-package: check-package-reference-log check-package-python-version unit-tests

# FIXME: workaround for old versions of check-package
FLAKE8_IGNORE += --ignore=W605,E123
# FIXME: workaround for old versions of buildroot/.flake8
FLAKE8_IGNORE += --max-line-length=132

update-reference-log:
	$(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/utils/run.sh -b $(TOPDIR) -e $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH) -o $(BASE_DIR) -l $(BASE_DIR)/log.base.txt
	cp -f $(BASE_DIR)/log.base.txt $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/log.base.txt

check-package-reference-log:
	$(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/utils/run.sh -b $(TOPDIR) -e $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH) -o $(BASE_DIR) -l $(BASE_DIR)/log.default.txt
	$(foreach log,log.default.txt, \
		diff -U3 $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/log.base.txt $(BASE_DIR)/$(log) > $(BASE_DIR)/log.diff; \
	)

check-package-python-version:
	$(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/utils/run.sh -b $(TOPDIR) -e $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH) -o $(BASE_DIR) -p python2 -l $(BASE_DIR)/log.python2.txt
	$(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/utils/run.sh -b $(TOPDIR) -e $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH) -o $(BASE_DIR) -p python3 -l $(BASE_DIR)/log.python3.txt
	$(foreach log,log.python2.txt log.python3.txt, \
		diff -U3 $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/log.base.txt $(BASE_DIR)/$(log) > $(BASE_DIR)/log.diff; \
	)
	python2 -m flake8 $(FLAKE8_IGNORE) --stat $(TOPDIR)/{utils/checkpackagelib/*.py,utils/check-package}
	python3 -m flake8 $(FLAKE8_IGNORE) --stat $(TOPDIR)/{utils/checkpackagelib/*.py,utils/check-package}

unit-tests:
	rm -rf $(BASE_DIR)/pytest
	mkdir -p $(BASE_DIR)/pytest
	sed '/^__main__()/d' $(TOPDIR)/utils/check-package > $(BASE_DIR)/pytest/check_package.py
	ln -snf $(TOPDIR)/utils/checkpackagelib $(BASE_DIR)/pytest/checkpackagelib
	$(foreach file,$(wildcard $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/pytest/*), \
		ln -snf $(file) $(BASE_DIR)/pytest/ ;\
	)
	$(foreach file,$(wildcard $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/pytest/.f*), \
		ln -snf $(file) $(BASE_DIR)/pytest/ ;\
	)
	cd $(BASE_DIR)/pytest && pytest
	cd $(BASE_DIR)/pytest && python2 -m flake8 --stat
