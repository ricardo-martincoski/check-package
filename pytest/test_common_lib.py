import pytest
import util
import checkpackagelib.lib as m


consecutive_empty_lines = [
    ('any', '', []),
    ('any', '\n', []),
    ('any', '\n\n', [['any:2: consecutive empty lines']]),
    ('any', '\n\n\n', [['any:2: consecutive empty lines'], ['any:3: consecutive empty lines']]),
    ('any', ' \n\t\n', [['any:2: consecutive empty lines']]),
    ]


@pytest.mark.parametrize("filename,string,expected", consecutive_empty_lines)
def test_consecutive_empty_lines(filename, string, expected):
    warnings = util.check_file(m.ConsecutiveEmptyLines, filename, string)
    assert warnings == expected


empty_last_line = [
    ('any', '', []),
    ('any', '\n', [['any:1: empty line at end of file']]),
    ('any', '\n\n', [['any:2: empty line at end of file']]),
    ('any', '\n\n\n', [['any:3: empty line at end of file']]),
    ('any', ' \n\t\n', [['any:2: empty line at end of file']]),
    ]


@pytest.mark.parametrize("filename,string,expected", empty_last_line)
def test_empty_last_line(filename, string, expected):
    warnings = util.check_file(m.EmptyLastLine, filename, string)
    assert warnings == expected


newline_at_eof = [
    ('any', 'text\n', []),
    ('any', '\ntext', [['any:2: missing newline at end of file', 'text']]),
    ('any', '\n ', [['any:2: missing newline at end of file', ' ']]),
    ('any', '\n\t', [['any:2: missing newline at end of file', '\t']]),
    ]


@pytest.mark.parametrize("filename,string,expected", newline_at_eof)
def test_newline_at_eof(filename, string, expected):
    warnings = util.check_file(m.NewlineAtEof, filename, string)
    assert warnings == expected


trailing_space = [
    ('any', 'text\n', []),
    ('any', '\ntext', []),
    ('any', 'text  \n', [['any:1: line contains trailing whitespace', 'text  \n']]),
    ('any', 'text\t\t\n', [['any:1: line contains trailing whitespace', 'text\t\t\n']]),
    ('any', ' \n ', [['any:1: line contains trailing whitespace', ' \n'], ['any:2: line contains trailing whitespace', ' ']]),
    ('any', '\n\t', [['any:2: line contains trailing whitespace', '\t']]),
    ]


@pytest.mark.parametrize("filename,string,expected", trailing_space)
def test_trailing_space(filename, string, expected):
    warnings = util.check_file(m.TrailingSpace, filename, string)
    assert warnings == expected
