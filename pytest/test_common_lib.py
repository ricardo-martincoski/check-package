import pytest
import util
import checkpackagelib.lib as m


consecutive_empty_lines = [
    ('any',
     '',
     []),
    ('any',
     '\n',
     []),
    ('any',
     '\n ',
     [['any:2: consecutive empty lines']]),
    ('any',
     '\n'
     '\n',
     [['any:2: consecutive empty lines']]),
    ('any',
     '\n'
     '\n'
     '\n',
     [['any:2: consecutive empty lines'],
      ['any:3: consecutive empty lines']]),
    ('any',
     ' \n'
     '\t\n',
     [['any:2: consecutive empty lines']]),
    ]


@pytest.mark.parametrize("filename,string,expected", consecutive_empty_lines)
def test_consecutive_empty_lines(filename, string, expected):
    warnings = util.check_file(m.ConsecutiveEmptyLines, filename, string)
    assert warnings == expected


empty_last_line = [
    ('any',
     '',
     []),
    ('any',
     '\n',
     [['any:1: empty line at end of file']]),
    ('any',
     ' \n',
     [['any:1: empty line at end of file']]),
    ('any',
     ' ',
     [['any:1: empty line at end of file']]),
    ('any',
     '\n'
     '\n',
     [['any:2: empty line at end of file']]),
    ('any',
     '\n'
     '\n'
     '\n',
     [['any:3: empty line at end of file']]),
    ('any',
     ' \n'
     '\t\n',
     [['any:2: empty line at end of file']]),
    ]


@pytest.mark.parametrize("filename,string,expected", empty_last_line)
def test_empty_last_line(filename, string, expected):
    warnings = util.check_file(m.EmptyLastLine, filename, string)
    assert warnings == expected


newline_at_eof = [
    ('any',
     'text\n',
     []),
    ('any',
     '\n'
     'text',
     [['any:2: missing newline at end of file',
       'text']]),
    ('any',
     '\n'
     ' ',
     [['any:2: missing newline at end of file',
       ' ']]),
    ('any',
     '\n'
     '\t',
     [['any:2: missing newline at end of file',
       '\t']]),
    ('any',
     ' ',
     [['any:1: missing newline at end of file',
       ' ']]),
    ]


@pytest.mark.parametrize("filename,string,expected", newline_at_eof)
def test_newline_at_eof(filename, string, expected):
    warnings = util.check_file(m.NewlineAtEof, filename, string)
    assert warnings == expected


trailing_space = [
    ('any',
     'text\n',
     []),
    ('any',
     '\ntext',
     []),
    ('any',
     'text  \n',
     [['any:1: line contains trailing whitespace',
       'text  \n']]),
    ('any',
     'text\t\t\n',
     [['any:1: line contains trailing whitespace',
       'text\t\t\n']]),
    ('any',
     ' \n'
     ' ',
     [['any:1: line contains trailing whitespace',
       ' \n'],
      ['any:2: line contains trailing whitespace',
       ' ']]),
    ('any',
     '\n'
     '\t',
     [['any:2: line contains trailing whitespace',
       '\t']]),
    ]


@pytest.mark.parametrize("filename,string,expected", trailing_space)
def test_trailing_space(filename, string, expected):
    warnings = util.check_file(m.TrailingSpace, filename, string)
    assert warnings == expected


utf8_characters = [
    ('any',
     'text\n',
     []),
    ('any',
     '\x60',
     []),
    ('any',
     '\x81',
     [['any:1: line contains UTF-8 characters',
       '\x81']]),
    ('any',
     'text\n'
     'text \xc8 text\n'
     '\xc9\n',
     [['any:2: line contains UTF-8 characters',
       'text \xc8 text\n'],
      ['any:3: line contains UTF-8 characters',
       '\xc9\n']]),
    ]


@pytest.mark.parametrize("filename,string,expected", utf8_characters)
def test_utf8_characters(filename, string, expected):
    warnings = util.check_file(m.Utf8Characters, filename, string)
    assert warnings == expected


def test_all_check_functions_are_used():
    import inspect
    import checkpackagelib.lib_config as lib_config
    import checkpackagelib.lib_hash as lib_hash
    import checkpackagelib.lib_mk as lib_mk
    import checkpackagelib.lib_patch as lib_patch
    c_config = [c[0] for c in inspect.getmembers(lib_config, inspect.isclass)]
    c_hash = [c[0] for c in inspect.getmembers(lib_hash, inspect.isclass)]
    c_mk = [c[0] for c in inspect.getmembers(lib_mk, inspect.isclass)]
    c_patch = [c[0] for c in inspect.getmembers(lib_patch, inspect.isclass)]
    c_all = c_config + c_hash + c_mk + c_patch
    c_common = [c[0] for c in inspect.getmembers(m, inspect.isclass)]
    assert set(c_common) <= set(c_all)
