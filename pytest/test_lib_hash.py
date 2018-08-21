import pytest
import util
import checkpackagelib.lib_hash as m


hash_number_of_fields = [
    ('any', '', []),
    ('any', '\n', []),
    ('any', '\t\n', []),
    ('any', '# text\n', []),
    ('any', 'field1\n', [['any:1: expected three fields (url#adding-packages-hash)', 'field1\n']]),
    ('any', 'field1 field2\n', [['any:1: expected three fields (url#adding-packages-hash)', 'field1 field2\n']]),
    ('any', 'field1 field2 field3 field4\n', [
     ['any:1: expected three fields (url#adding-packages-hash)', 'field1 field2 field3 field4\n']]),
    ('any', 'field1 field2 field3\n', []),
    ('any', '   field1   field2   field3\n', []),
    ('any', 'field1\tfield2\tfield3\n', []),
    ('any', '\tfield1\t field2\t field3 \n', []),
    ]


@pytest.mark.parametrize("filename,string,expected", hash_number_of_fields)
def test_hash_number_of_fields(filename, string, expected):
    warnings = util.check_file(m.HashNumberOfFields, filename, string)
    assert warnings == expected
