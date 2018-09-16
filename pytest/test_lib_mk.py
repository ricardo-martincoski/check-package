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
