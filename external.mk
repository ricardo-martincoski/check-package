include $(sort $(wildcard $(BR2_EXTERNAL_CHECK_PACKAGE_BAD_EXAMPLES_PATH)/package/*/*.mk))

check-check-package: check-package-reference-log check-package-python-version

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
	python2 -m flake8 --stat $(TOPDIR)/{utils/checkpackagelib/*.py,utils/check-package}
	python3 -m flake8 --stat $(TOPDIR)/{utils/checkpackagelib/*.py,utils/check-package}
