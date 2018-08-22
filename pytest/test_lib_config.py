import pytest
import util
import checkpackagelib.lib_config as m


attributes_order = [
    ('any', 'config BR2_PACKAGE_FOO\n'
            'bool "foo"\n'
            'default y\n'
            'depends on BR2_USE_BAR # runtime\n'
            'select BR2_PACKAGE_BAZ\n'
            'help\n'
            '\t  help text\n', []),
    ('any', 'config BR2_PACKAGE_FOO\n'
            'bool "foo"\n'
            'depends on BR2_USE_BAR\n'
            'default y\n',
            [['any:4: attributes order: type, default, depends on, select, help (url#_config_files)', 'default y\n']]),
    ('any', 'config BR2_PACKAGE_FOO\n'
            'bool "foo"\n'
            'help\n'
            '\t  help text\n'
            'select BR2_PACKAGE_BAZ\n',
            [['any:5: attributes order: type, default, depends on, select, help (url#_config_files)', 'select BR2_PACKAGE_BAZ\n']]),
    ('any', 'config BR2_PACKAGE_FOO_PLUGINS\n'
            'string "foo plugins"\n'
            'default "all"\n',
            []),
    ('any', 'config\tBR2_PACKAGE_FOO_PLUGINS\n'
            'default\t"all"\n'
            'string\t"foo plugins"\n',
            [['any:3: attributes order: type, default, depends on, select, help (url#_config_files)', 'string\t"foo plugins"\n']]),
    ('any', 'config BR2_PACKAGE_FOO\n'
            'bool "foo"\n'
            'if BR2_PACKAGE_FOO\n'
            '\n'
            'choice\n'
            'prompt "type of foo"\n'
            'default BR2_PACKAGE_FOO_STRING\n'
            '\n'
            'config BR2_PACKAGE_FOO_NONE\n'
            'bool "none"\n'
            '\n'
            'config BR2_PACKAGE_FOO_STRING\n'
            'bool "string"\n'
            '\n'
            'endchoice\n'
            '\n'
            'endif\n'
            '\n',
            []),
    ('any', 'config BR2_PACKAGE_FOO\n'
            'bool "foo"\n'
            'if BR2_PACKAGE_FOO\n'
            '\n'
            'choice\n'
            'default BR2_PACKAGE_FOO_STRING\n'
            'prompt "type of foo"\n',
            [['any:7: attributes order: type, default, depends on, select, help (url#_config_files)', 'prompt "type of foo"\n']]),
    ('any', 'menuconfig BR2_PACKAGE_FOO\n'
            'bool "foo"\n'
            'help\n'
            '\t  help text\n'
            '\t  help text\n'
            '\n'
            'if BR2_PACKAGE_FOO\n'
            '\n'
            'menu "foo plugins"\n'
            'config BR2_PACKAGE_FOO_COUNTER\n'
            'bool "counter"\n'
            '\n'
            'endmenu\n'
            '\n'
            'endif\n',
            []),
    ]


@pytest.mark.parametrize("filename,string,expected", attributes_order)
def test_attributes_order(filename, string, expected):
    warnings = util.check_file(m.AttributesOrder, filename, string)
    assert warnings == expected
