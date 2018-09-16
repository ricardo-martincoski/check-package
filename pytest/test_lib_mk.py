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
