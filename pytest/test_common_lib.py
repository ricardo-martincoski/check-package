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
def test_empty_lines(filename, string, expected):
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
