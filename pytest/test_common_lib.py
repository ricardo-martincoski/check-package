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
