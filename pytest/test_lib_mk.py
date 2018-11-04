import pytest
import util
import checkpackagelib.lib_mk as m


indent = [
    ('any', '# very useful comment\n', []),
    ('any', ' # very useful comment\n', []),
    ('any', 'ifeq ($(BR2_TOOLCHAIN_HAS_THREADS),y)\n'
            'FOO_CONF_OPTS += something\n'
            'endef\n',
            []),
    ('any', 'ifeq ($(BR2_TOOLCHAIN_HAS_THREADS),y)\n'
            '\tFOO_CONF_OPTS += something\n'
            'endef\n',
            [['any:2: unexpected indent with tabs', '\tFOO_CONF_OPTS += something\n']]),
    ('any', 'FOO_CONF_OPTS += \\\n'
            'something\n',
            [['any:2: expected indent with tabs', 'something\n']]),
    ('any', 'FOO_CONF_OPTS += \\\n'
            '\tsomething\n',
            []),
    ('any', 'FOO_CONF_OPTS += \\\n'
            '\tsomething \\\n'
            '\tsomething_else\n',
            []),
    ('any', 'FOO_CONF_OPTS += \\\n'
            '\tsomething \\\n'
            '\tsomething_else \\\n'
            'FOO_CONF_OPTS += another_thing\n',
            [['any:4: expected indent with tabs', 'FOO_CONF_OPTS += another_thing\n']]),
    ('any', 'define FOO_SOMETHING\n'
            '\tcommand\n'
            '\tcommand \\\n'
            '\t\targuments\n'
            'endef\n'
            'FOO_POST_PATCH_HOOKS += FOO_SOMETHING\n',
            []),
    ('any', 'define FOO_SOMETHING\n'
            'command\n'
            'endef\n',
            [['any:2: expected indent with tabs', 'command\n']]),
    ('any', 'define FOO_SOMETHING\n'
            '        command\n'
            'endef\n',
            [['any:2: expected indent with tabs', '        command\n']]),
    ('any', 'make_target:\n'
            '\tcommand\n'
            '\n',
            []),
    ('any', 'make_target:\n'
            '        command\n'
            '\n',
            [['any:2: expected indent with tabs', '        command\n']]),
    ]


@pytest.mark.parametrize("filename,string,expected", indent)
def test_indent(filename, string, expected):
    warnings = util.check_file(m.Indent, filename, string)
    assert warnings == expected


package_header = [
    ('any', '# very useful comment\n',
     [['any:1: should be 80 hashes (url#writing-rules-mk)',
       '# very useful comment\n',
       80 * '#']]),
    ('any', 80 * '#' + '\n', []),
    ('any', 80 * '#' + '\n# package\n', [['any:2: should be 1 hash (url#writing-rules-mk)', '# package\n']]),
    ('any', 80 * '#' + '\n#\n# package\n', []),
    ('any', 80 * '#' + '\n#\n# package\n#\n', []),
    ('any', 80 * '#' + '\n#\n# package\n#\n' + 80 * '#' + '\n', []),
    ('any', 80 * '#' + '\n#\n# package\n#\n' + 80 * '#' + '\n\n', []),
    ('any', 80 * '#' + '\n#\n# package\n#\n' + 80 * '#' + '\nFOO_VERSION = 1\n',
     [['any:6: should be a blank line (url#writing-rules-mk)', 'FOO_VERSION = 1\n']]),
    ('any', 79 * '#' + '\n#\n# package\n#\n' + 81 * '#' + '\n\n',
     [['any:1: should be 80 hashes (url#writing-rules-mk)', 79 * '#' + '\n', 80 * '#'],
      ['any:5: should be 80 hashes (url#writing-rules-mk)', 81 * '#' + '\n', 80 * '#']]),
    ('any', 'include $(sort $(wildcard package/foo/*/*.mk))\n', []),
    ('any', 80 * '#' + '\n#\n# package\n#\n' + 80 * '#' + '\n\nFOO_VERSION = 1\n', []),
    ]


@pytest.mark.parametrize("filename,string,expected", package_header)
def test_package_header(filename, string, expected):
    warnings = util.check_file(m.PackageHeader, filename, string)
    assert warnings == expected


remove_default_package_source_variable = [
    ('./any.mk', '\n', []),
    ('any/any.mk', '\n', []),
    ('./any/any.mk', '\n', []),
    ('package/any/any.mk', '\n', []),
    ('./package/any/any.mk', '\n', []),
    ('/tmp/any.mk', '\n', []),
    ('any.mk', '\n', []),  # catches https://bugs.busybox.net/show_bug.cgi?id=11271
    ('any.mk', 'ANY_SOURCE = any-$(ANY_VERSION).tar.gz\n',
     [['any.mk:1: remove default value of _SOURCE variable (url#generic-package-reference)',
       'ANY_SOURCE = any-$(ANY_VERSION).tar.gz\n']]),
    ('./any.mk', 'ANY_SOURCE = any-$(ANY_VERSION).tar.gz\n',
     [['./any.mk:1: remove default value of _SOURCE variable (url#generic-package-reference)',
       'ANY_SOURCE = any-$(ANY_VERSION).tar.gz\n']]),
    ('./any.mk', '\n\n\nANY_SOURCE = any-$(ANY_VERSION).tar.gz\n',
     [['./any.mk:4: remove default value of _SOURCE variable (url#generic-package-reference)',
       'ANY_SOURCE = any-$(ANY_VERSION).tar.gz\n']]),
    ('./any.mk', 'ANY_SOURCE=any-$(ANY_VERSION).tar.gz\n',
     [['./any.mk:1: remove default value of _SOURCE variable (url#generic-package-reference)',
       'ANY_SOURCE=any-$(ANY_VERSION).tar.gz\n']]),
    ('./any.mk', 'ANY_SOURCE = aNy-$(ANY_VERSION).tar.gz\n', []),
    ('gcc.mk', 'GCC_SOURCE = gcc-$(GCC_VERSION).tar.gz\n', []),
    ('./binutils.mk', 'BINUTILS_SOURCE = binutils-$(BINUTILS_VERSION).tar.gz\n', []),
    ('gdb/gdb.mk', 'GDB_SOURCE = gdb-$(GDB_VERSION).tar.gz\n', []),
    ('python-subprocess32.mk', 'PYTHON_SUBPROCESS32_SOURCE = python-subprocess32-$(PYTHON_SUBPROCESS32_VERSION).tar.gz\n',
     [['python-subprocess32.mk:1: remove default value of _SOURCE variable (url#generic-package-reference)',
       'PYTHON_SUBPROCESS32_SOURCE = python-subprocess32-$(PYTHON_SUBPROCESS32_VERSION).tar.gz\n']]),
    ]


@pytest.mark.parametrize("filename,string,expected", remove_default_package_source_variable)
def test_remove_default_package_source_variable(filename, string, expected):
    warnings = util.check_file(m.RemoveDefaultPackageSourceVariable, filename, string)
    assert warnings == expected


space_before_backslash = [
    ('any.mk', '\n', []),
    ('any.mk', 'define ANY_SOME_FIXUP\nfor i in $$(find $(STAGING_DIR)/usr/lib* -name "any*.la"); do \\\n', []),
    ('any.mk', 'ANY_CONF_ENV= \\\n\tap_cv_void_ptr_lt_long=no \\\n', []),
    ('any.mk', 'ANY = \\\n', []),
    ('any.mk', '\nANY = \\\n', []),
    ('any.mk', 'ANY =  \\\n', [['any.mk:1: use only one space before backslash', 'ANY =  \\\n']]),
    ('any.mk', '\nANY =  \\\n', [['any.mk:2: use only one space before backslash', 'ANY =  \\\n']]),
    ('any.mk', 'ANY =\t\\\n', [['any.mk:1: use only one space before backslash', 'ANY =\t\\\n']]),
    ('any.mk', 'ANY =\t\t\\\n', [['any.mk:1: use only one space before backslash', 'ANY =\t\t\\\n']]),
    ('any.mk', 'ANY =  \t\t\\\n', [['any.mk:1: use only one space before backslash', 'ANY =  \t\t\\\n']]),
    ('any.mk', 'ANY = \t \t\\\n', [['any.mk:1: use only one space before backslash', 'ANY = \t \t\\\n']]),
    ('any.mk', 'ANY = \t  \\\n', [['any.mk:1: use only one space before backslash', 'ANY = \t  \\\n']]),
    ]


@pytest.mark.parametrize("filename,string,expected", space_before_backslash)
def test_space_before_backslash(filename, string, expected):
    warnings = util.check_file(m.SpaceBeforeBackslash, filename, string)
    assert warnings == expected
