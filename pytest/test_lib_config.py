import pytest
import util
import checkpackagelib.lib_config as m


attributes_order = [
    ('any',
     'config BR2_PACKAGE_FOO\n'
     'bool "foo"\n'
     'default y\n'
     'depends on BR2_USE_BAR # runtime\n'
     'select BR2_PACKAGE_BAZ\n'
     'help\n'
     '\t  help text\n',
     []),
    ('any',
     'config BR2_PACKAGE_FOO\n'
     'bool "foo"\n'
     'depends on BR2_USE_BAR\n'
     'default y\n',
     [['any:4: attributes order: type, default, depends on, select, help (url#_config_files)',
       'default y\n']]),
    ('any',
     'config BR2_PACKAGE_FOO\n'
     'bool "foo"\n'
     'help\n'
     '\t  help text\n'
     'select BR2_PACKAGE_BAZ\n',
     [['any:5: attributes order: type, default, depends on, select, help (url#_config_files)',
       'select BR2_PACKAGE_BAZ\n']]),
    ('any',
     'config BR2_PACKAGE_FOO_PLUGINS\n'
     'string "foo plugins"\n'
     'default "all"\n',
     []),
    ('any',
     'config\tBR2_PACKAGE_FOO_PLUGINS\n'
     'default\t"all"\n'
     'string\t"foo plugins"\n',
     [['any:3: attributes order: type, default, depends on, select, help (url#_config_files)',
       'string\t"foo plugins"\n']]),
    ('any',
     'config BR2_PACKAGE_FOO\n'
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
    ('any',
     'config BR2_PACKAGE_FOO\n'
     'bool "foo"\n'
     'if BR2_PACKAGE_FOO\n'
     '\n'
     'choice\n'
     'default BR2_PACKAGE_FOO_STRING\n'
     'prompt "type of foo"\n',
     [['any:7: attributes order: type, default, depends on, select, help (url#_config_files)',
       'prompt "type of foo"\n']]),
    ('any',
     'menuconfig BR2_PACKAGE_FOO\n'
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


comments_menus_packages_order = [
    ('package/Config.in',
     'menu "Target packages"\n'
     'source "package/busybox/Config.in"\n'
     'source "package/skeleton/Config.in"\n',
     []),
    ('package/Config.in',
     'source "package/skeleton/Config.in"\n'
     'source "package/busybox/Config.in"\n',
     [['package/Config.in:2: Packages in: ,\n'
       '                     are not alphabetically ordered;\n'
       "                     correct order: '-', '_', digits, capitals, lowercase;\n"
       '                     first incorrect package: busybox',
       'source "package/busybox/Config.in"\n']]),
    ('package/Config.in',
     'menu "Target packages"\n'
     'source "package/skeleton/Config.in"\n'
     'source "package/busybox/Config.in"\n',
     [['package/Config.in:3: Packages in: menu "Target packages",\n'
       '                     are not alphabetically ordered;\n'
       "                     correct order: '-', '_', digits, capitals, lowercase;\n"
       '                     first incorrect package: busybox',
       'source "package/busybox/Config.in"\n']]),
    ]


@pytest.mark.parametrize("filename,string,expected", comments_menus_packages_order)
def test_comments_menus_packages_order(filename, string, expected):
    warnings = util.check_file(m.CommentsMenusPackagesOrder, filename, string)
    assert warnings == expected


help_text = [
    ('any',
     'config BR2_PACKAGE_FOO\n'
     'bool "foo"\n'
     'default y\n'
     'depends on BR2_USE_BAR # runtime\n'
     'select BR2_PACKAGE_BAZ\n'
     'help\n'
     '\t  help text\n',
     []),
    ('any',
     'help\n'
     '\t  123456789 123456789 123456789 123456789 123456789 123456789 12\n'
     '\t  123456789 123456789 123456789 123456789 123456789 123456789 123\n'
     '\t  help text\n',
     [['any:3: help text: <tab><2 spaces><62 chars> (url#writing-rules-config-in)',
       '\t  123456789 123456789 123456789 123456789 123456789 123456789 123\n',
       '\t  123456789 123456789 123456789 123456789 123456789 123456789 12']]),
    ('any',
     'help\n'
     '\t  123456789 123456789 123456789 123456789 123456789 123456789 12\n'
     '\t  refer to http://url.that.is.longer.than.seventy.two.characthers/folder_name\n'
     '\n'
     '\t  http://url.that.is.longer.than.seventy.two.characthers/folder_name\n',
     [['any:3: help text: <tab><2 spaces><62 chars> (url#writing-rules-config-in)',
       '\t  refer to http://url.that.is.longer.than.seventy.two.characthers/folder_name\n',
       '\t  123456789 123456789 123456789 123456789 123456789 123456789 12']]),
    ('any',
     'help\n'
     '\t  123456789 123456789 123456789 123456789 123456789 123456789 12\n'
     '\t  http://url.that.is.longer.than.seventy.two.characthers/folder_name\n'
     '\t  https://url.that.is.longer.than.seventy.two.characthers/folder_name\n'
     '\t  git://url.that.is.longer.than.seventy.two.characthers/folder_name\n',
     []),
    ('any',
     'help\n'
     '\t  123456789 123456789 123456789 123456789 123456789 123456789 12\n'
     '\t  summary:\n'
     '\t    - enable that config\n'
     '\t    - built it\n',
     []),
    ]


@pytest.mark.parametrize("filename,string,expected", help_text)
def test_help_text(filename, string, expected):
    warnings = util.check_file(m.HelpText, filename, string)
    assert warnings == expected


indent = [
    ('any',
     'config BR2_PACKAGE_FOO\n'
     '\tbool "foo"\n'
     '\tdefault y\n'
     '\tdepends on BR2_TOOLCHAIN_HAS_THREADS\n'
     '\tdepends on BR2_INSTALL_LIBSTDCPP\n'
     '# very useful comment\n'
     '\tselect BR2_PACKAGE_BAZ\n'
     '\thelp\n'
     '\t  help text\n'
     '\n'
     'comment "foo needs toolchain w/ C++, threads"\n'
     '\tdepends on !BR2_INSTALL_LIBSTDCPP || \\\n'
     '\t\t!BR2_TOOLCHAIN_HAS_THREADS\n'
     '\n'
     'source "package/foo/bar/Config.in"\n',
     []),
    ('any',
     'config BR2_PACKAGE_FOO\n'
     '        bool "foo"\n',
     [['any:2: should be indented with one tab (url#_config_files)',
       '        bool "foo"\n']]),
    ('any',
     'config BR2_PACKAGE_FOO\n'
     'default y\n',
     [['any:2: should be indented with one tab (url#_config_files)',
       'default y\n']]),
    ('any',
     'config BR2_PACKAGE_FOO\n'
     '\t\tdepends on BR2_TOOLCHAIN_HAS_THREADS\n',
     [['any:2: should be indented with one tab (url#_config_files)',
       '\t\tdepends on BR2_TOOLCHAIN_HAS_THREADS\n']]),
    ('any',
     'config BR2_PACKAGE_FOO\n'
     '     help\n',
     [['any:2: should be indented with one tab (url#_config_files)',
       '     help\n']]),
    ('any',
     'comment "foo needs toolchain w/ C++, threads"\n'
     '\tdepends on !BR2_INSTALL_LIBSTDCPP || \\\n'
     '                !BR2_TOOLCHAIN_HAS_THREADS\n',
     [['any:3: continuation line should be indented using tabs',
       '                !BR2_TOOLCHAIN_HAS_THREADS\n']]),
    ('any',
     '\tcomment "foo needs toolchain w/ C++, threads"\n',
     [['any:1: should not be indented',
       '\tcomment "foo needs toolchain w/ C++, threads"\n']]),
    ('any',
     '  comment "foo needs toolchain w/ C++, threads"\n',
     [['any:1: should not be indented',
       '  comment "foo needs toolchain w/ C++, threads"\n']]),
    ]


@pytest.mark.parametrize("filename,string,expected", indent)
def test_indent(filename, string, expected):
    warnings = util.check_file(m.Indent, filename, string)
    assert warnings == expected
